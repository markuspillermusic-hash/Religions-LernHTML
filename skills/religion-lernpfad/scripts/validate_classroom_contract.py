from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from validate_learning_html import Inspector


CONFIG_RE = re.compile(
    r"window\.RELIGION_CLASSROOM_CONFIG\s*=\s*(\{.*?\})\s*;\s*</script>",
    re.DOTALL,
)
VIEW_RE = re.compile(r"window\.RELIGION_VIEW\s*=\s*[\"'](student|teacher|beamer)[\"']")
SCRIPT_SRC_RE = re.compile(r"<script\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
STYLE_HREF_RE = re.compile(r"<link\b[^>]*\bhref=[\"']([^\"']+)[\"'][^>]*>", re.I)
FEEDBACK_TASK_RE = re.compile(r"\bdata-feedback-task=[\"']([a-z0-9][a-z0-9._-]{2,99})[\"']", re.I)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def config_from(text: str, role: str, errors: list[str]) -> dict[str, Any]:
    match = CONFIG_RE.search(text)
    if not match:
        errors.append(f"{role}: RELIGION_CLASSROOM_CONFIG fehlt oder ist nicht als JSON eingebettet")
        return {}
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"{role}: Klassenraumkonfiguration ist kein gültiges JSON: {exc}")
        return {}
    return value if isinstance(value, dict) else {}


def local_asset(sources: list[str], suffix: str) -> str:
    for source in sources:
        clean = source.split("#", 1)[0]
        if clean.split("?", 1)[0].endswith(suffix):
            return source
    return ""


def require_tokens(label: str, text: str, tokens: list[str], errors: list[str]) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        errors.append(f"{label}: Vertragsmerkmale fehlen: {', '.join(missing)}")


def inspect_html(text: str) -> Inspector:
    inspector = Inspector()
    inspector.feed(text)
    return inspector


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prüft den statischen Klassenraumvertrag eines Schüler-/Lehrer-/Beamer-Builds."
    )
    parser.add_argument("student", type=Path)
    parser.add_argument("teacher", type=Path)
    parser.add_argument("beamer", type=Path)
    parser.add_argument("--api", type=Path, required=True)
    parser.add_argument("--classroom-js", type=Path, required=True)
    parser.add_argument("--presentation-js", type=Path, required=True)
    parser.add_argument("--classroom-css", type=Path)
    parser.add_argument("--qr-js", type=Path, required=True)
    parser.add_argument(
        "--canonical-dir",
        type=Path,
        help="Optionaler _shared/classroom-v1-Ordner; ausgelieferte Kerndateien müssen dann hashidentisch sein.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paths = {
        "student": args.student.resolve(),
        "teacher": args.teacher.resolve(),
        "beamer": args.beamer.resolve(),
        "api": args.api.resolve(),
        "classroom_js": args.classroom_js.resolve(),
        "presentation_js": args.presentation_js.resolve(),
        "qr_js": args.qr_js.resolve(),
    }
    if args.classroom_css:
        paths["classroom_css"] = args.classroom_css.resolve()

    errors: list[str] = []
    warnings: list[str] = []
    for label, path in paths.items():
        if not path.is_file():
            errors.append(f"{label}: Datei fehlt: {path}")
    if errors:
        report = {"files": {k: str(v) for k, v in paths.items()}, "errors": errors, "warnings": warnings, "ok": False}
        print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else "\n".join("FEHLER: " + item for item in errors))
        return 1

    views = {role: read(paths[role]) for role in ("student", "teacher", "beamer")}
    inspectors = {role: inspect_html(text) for role, text in views.items()}
    configs = {role: config_from(views[role], role, errors) for role in views}
    feedback_tasks = sorted(set(FEEDBACK_TASK_RE.findall(views["student"])))

    for role, text in views.items():
        view_match = VIEW_RE.search(text)
        actual_view = view_match.group(1) if view_match else ""
        if actual_view != role:
            errors.append(f"{role}: window.RELIGION_VIEW ist {actual_view or 'nicht gesetzt'}")
        config_view = str(configs[role].get("view", ""))
        if config_view != role:
            errors.append(f"{role}: config.view ist {config_view or 'nicht gesetzt'}")

        scripts = SCRIPT_SRC_RE.findall(text)
        qr_src = local_asset(scripts, "qrcode-generator.js")
        classroom_src = local_asset(scripts, "live.js")
        presentation_src = local_asset(scripts, "presentation.js")
        required_assets = (("Klassenraumkern", classroom_src), ("Präsentationskern", presentation_src))
        for asset, source in required_assets:
            if not source:
                errors.append(f"{role}: {asset} wird nicht geladen")
            elif re.match(r"https?://", source, re.I):
                errors.append(f"{role}: {asset} wird remote statt lokal geladen: {source}")
        # Der QR-Code wird ausschließlich dort benötigt, wo Beitrittsdaten
        # erzeugt bzw. präsentiert werden. Die Schüleransicht soll dafür keine
        # unnötige Bibliothek laden müssen.
        if role == "teacher" and not qr_src:
            errors.append("teacher: QR-Bibliothek wird nicht geladen")
        if qr_src and re.match(r"https?://", qr_src, re.I):
            errors.append(f"{role}: QR wird remote statt lokal geladen: {qr_src}")
        ordered_sources = [source for source in (qr_src, classroom_src, presentation_src) if source]
        if classroom_src and presentation_src:
            positions = [text.find(source) for source in ordered_sources]
            if positions != sorted(positions):
                errors.append(f"{role}: Scriptreihenfolge muss QR (falls vorhanden) → Klassenraum → Präsentation sein")

    module_ids = {str(config.get("moduleId", "")) for config in configs.values()}
    if len(module_ids) != 1 or not next(iter(module_ids), ""):
        errors.append("Rollen verwenden keine identische, nichtleere moduleId")
    module_slugs = {str(config.get("moduleSlug", "")) for config in configs.values()}
    if len(module_slugs) != 1 or not next(iter(module_slugs), ""):
        message = "Rollen verwenden keine identische, nichtleere moduleSlug für die zentrale Plattform"
        (errors if feedback_tasks else warnings).append(message)
    release_sets = {tuple(config.get("releaseStages", [])) for config in configs.values()}
    if len(release_sets) != 1 or len(next(iter(release_sets), ())) < 2:
        errors.append("Rollen verwenden keine identische Freigabefolge mit mindestens zwei Stufen")
    presentation_configs = {json.dumps(config.get("presentation", {}), ensure_ascii=False, sort_keys=True) for config in configs.values()}
    if len(presentation_configs) != 1:
        errors.append("Präsentationskonfiguration weicht zwischen den Rollen ab")

    for public_role in ("student", "beamer"):
        if inspectors[public_role].teacher_nodes:
            errors.append(f"{public_role}: Lehrerinhalt ist im ausgelieferten DOM vorhanden")
    if inspectors["beamer"].response_fields:
        errors.append("beamer: Antwort- oder Eingabefelder sind vorhanden")
    if paths["teacher"].suffix.lower() != ".php":
        warnings.append("teacher: Dateiendung ist nicht .php; serverseitigen Schutz gesondert nachweisen")
    if "RELIGION_CLASSROOM_CONFIG" not in views["teacher"]:
        errors.append("teacher: Klassenraumkonfiguration fehlt")
    central_auth = "Auth::currentUser" in views["teacher"] and "teacher-platform" in views["teacher"]
    legacy_auth = "password_verify" in views["teacher"] or ("hash_pbkdf2" in views["teacher"] and "hash_equals" in views["teacher"])
    if not central_auth and not legacy_auth:
        errors.append("teacher: serverseitige Passwortprüfung wurde nicht erkannt")

    if feedback_tasks:
        feedback_endpoints = {str(config.get("feedbackEndpoint", "")) for config in configs.values()}
        endpoint = next(iter(feedback_endpoints), "")
        if len(feedback_endpoints) != 1 or not endpoint.startswith("/api/"):
            errors.append("KI-Feedback: Rollen verwenden keinen identischen relativen Plattform-Endpunkt unter /api/")
        student_scripts = SCRIPT_SRC_RE.findall(views["student"])
        feedback_src = local_asset(student_scripts, "feedback-client.js")
        if not feedback_src:
            errors.append("student: lokaler feedback-client.js fehlt trotz data-feedback-task")
        elif re.match(r"https?://", feedback_src, re.I):
            errors.append("student: Feedback-Client wird remote statt lokal geladen")

    api = read(paths["api"])
    require_tokens(
        "api",
        api,
        [
            "list_rooms",
            "set_release",
            "releasedStage",
            "set_presentation",
            "beamer_heartbeat",
            "start_timer",
            "pause_timer",
            "resume_timer",
            "add_timer",
            "reset_timer",
        ],
        errors,
    )
    if feedback_tasks:
        require_tokens("api", api, ["set_feedback", "aiFeedbackEnabled"], errors)
    if not re.search(r"(?:===|==)\s*['\"]create['\"]|['\"]create_room['\"]", api):
        errors.append("api: Aktion zum Erstellen eines Raums wurde nicht erkannt")
    if "10800" not in api and "180 * 60" not in api and "180*60" not in api:
        warnings.append("api: 180-Minuten-Obergrenze des Timers nicht statisch erkannt")

    classroom_js = read(paths["classroom_js"])
    require_tokens(
        "classroom_js",
        classroom_js,
        [
            "releaseForNode",
            "qrState",
            "Gemeinsamer Timer",
            "start_timer",
            "pause_timer",
            "resume_timer",
            "add_timer",
            "reset_timer",
            "180",
        ],
        errors,
    )

    presentation_js = read(paths["presentation_js"])
    require_tokens(
        "presentation_js",
        presentation_js,
        [
            'version: "1.2.4"',
            "persistentQueue",
            "_classroom",
            "presenterState.details",
            "presenterState.controls",
            "presenterState.media",
            "presenterState.youtube",
            "presenterState.image",
            "classroom-header-collapse-toggle",
            "prepareBeamerStages",
            "data-classroom-control-group",
            ".media-load",
        ],
        errors,
    )
    if paths["qr_js"].stat().st_size < 10_000:
        errors.append("qr_js: Datei ist unerwartet klein; vollständige lokale Bibliothek fehlt vermutlich")

    if args.canonical_dir:
        canonical_dir = args.canonical_dir.resolve()
        canonical_pairs = {
            "classroom_js": canonical_dir / "classroom-core.js",
            "presentation_js": canonical_dir / "presentation-core.js",
            "qr_js": canonical_dir / "qrcode-generator.js",
        }
        if "classroom_css" in paths:
            canonical_pairs["classroom_css"] = canonical_dir / "classroom.css"
        for label, canonical in canonical_pairs.items():
            if not canonical.is_file():
                errors.append(f"canonical: Datei fehlt: {canonical}")
            elif sha256(paths[label]) != sha256(canonical):
                errors.append(f"{label}: ausgelieferte Datei weicht vom gemeinsamen Kern ab")

    cache_contract: dict[str, list[str]] = {}
    for role, text in views.items():
        assets = SCRIPT_SRC_RE.findall(text) + STYLE_HREF_RE.findall(text)
        cache_contract[role] = sorted(
            source.split("?", 1)[1]
            for source in assets
            if any(name in source for name in ("qrcode-generator.js", "live.js", "presentation.js", "live.css")) and "?" in source
        )
        if len(cache_contract[role]) < 3:
            warnings.append(f"{role}: nicht alle gemeinsamen Assets tragen eine Cache-Version")

    report = {
        "files": {label: str(path) for label, path in paths.items()},
        "module_id": next(iter(module_ids), ""),
        "module_slug": next(iter(module_slugs), ""),
        "feedback_tasks": feedback_tasks,
        "release_stages": list(next(iter(release_sets), ())),
        "cache_tokens": cache_contract,
        "warnings": warnings,
        "errors": errors,
        "ok": not errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Klassenraumvertrag: " + ("BESTANDEN" if report["ok"] else "NICHT BESTANDEN"))
        for warning in warnings:
            print("WARNUNG: " + warning)
        for error in errors:
            print("FEHLER: " + error)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
