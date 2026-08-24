from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.template_ids: list[str] = []
        self.fragments: list[str] = []
        self.template_fragments: list[str] = []
        self.resources: list[str] = []
        self.links: list[str] = []
        self.handlers: list[str] = []
        self.images_without_alt: list[str] = []
        self.teacher_nodes = 0
        self.response_fields: list[str] = []
        self.steps: list[str] = []
        self.scripts: list[str] = []
        self._in_script = False
        self._script_parts: list[str] = []
        self._template_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        in_template = self._template_depth > 0
        if data.get("id"):
            (self.template_ids if in_template else self.ids).append(data["id"])
        href = data.get("href", "")
        if href.startswith("#") and len(href) > 1:
            (self.template_fragments if in_template else self.fragments).append(href[1:])
        for name in ("src", "poster"):
            value = data.get(name, "")
            if value:
                self.resources.append(value)
        if tag == "link" and href:
            self.resources.append(href)
        elif tag == "a" and href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
            self.links.append(href)
        for name, value in data.items():
            if name.startswith("on") and value:
                self.handlers.append(value)
        if tag == "img" and "alt" not in data:
            self.images_without_alt.append(data.get("src", "<ohne src>"))
        if data.get("data-rolle") == "lehrer":
            self.teacher_nodes += 1
        for step_name in ("data-beamer-step", "data-entry-beamer-step", "data-beamer-anchor", "data-step-id", "data-schritt"):
            if data.get(step_name):
                self.steps.append(f"{step_name}:{data[step_name]}")
        input_type = data.get("type", "text").lower()
        if not in_template and (
            tag in {"textarea", "select"}
            or (tag == "input" and input_type not in {"hidden", "range"})
            or data.get("contenteditable", "").lower() in {"", "true"} and "contenteditable" in data
        ):
            self.response_fields.append(data.get("id") or data.get("name") or f"<{tag}>")
        if tag == "script" and not data.get("src"):
            self._in_script = True
            self._script_parts = []
        if tag == "template":
            self._template_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_script:
            self.scripts.append("".join(self._script_parts))
            self._in_script = False
        if tag == "template" and self._template_depth:
            self._template_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_parts.append(data)


def is_remote(value: str) -> bool:
    return value.startswith("//") or urlparse(value).scheme in {"http", "https"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prüft eine interaktive Lern-HTML konservativ.")
    parser.add_argument("html", type=Path)
    parser.add_argument("--public", action="store_true", help="Öffentliche Schülerdatei: Lehrerblöcke sind Fehler.")
    parser.add_argument("--beamer", action="store_true", help="Beamerdatei: Lehrerblöcke und Antwortfelder sind Fehler.")
    parser.add_argument("--allow-remote", action="store_true", help="Remote-Ressourcen nur melden, nicht als Fehler werten.")
    args = parser.parse_args()

    path = args.html.resolve()
    text = path.read_text(encoding="utf-8")
    inspector = Inspector()
    inspector.feed(text)

    errors: list[str] = []
    warnings: list[str] = []
    duplicate_ids = sorted(key for key, count in Counter(inspector.ids).items() if count > 1)
    if duplicate_ids:
        errors.append("Doppelte IDs: " + ", ".join(duplicate_ids))
    missing_fragments = sorted(set(inspector.fragments) - set(inspector.ids))
    if missing_fragments:
        errors.append("Fehlende Sprungziele: " + ", ".join(missing_fragments))
    if inspector.images_without_alt:
        errors.append("Bilder ohne alt: " + ", ".join(inspector.images_without_alt[:10]))
    missing_template_fragments = sorted(
        set(inspector.template_fragments) - set(inspector.ids) - set(inspector.template_ids)
    )
    if missing_template_fragments:
        errors.append("Fehlende Sprungziele in Templates: " + ", ".join(missing_template_fragments))
    duplicate_template_ids = sorted(
        key for key, count in Counter(inspector.template_ids).items() if count > 1
    )
    if duplicate_template_ids:
        warnings.append(
            "IDs kommen in mehreren inerten Template-Inhalten vor; aktive Modi im Browser getrennt prüfen: "
            + ", ".join(duplicate_template_ids)
        )
    if (args.public or args.beamer) and inspector.teacher_nodes:
        errors.append(f"Öffentliche Datei enthält {inspector.teacher_nodes} Lehrerblöcke.")
    elif inspector.teacher_nodes:
        warnings.append(f"Autorenentwurf enthält {inspector.teacher_nodes} Lehrerblöcke.")
    if args.beamer and inspector.response_fields:
        errors.append(
            "Beamerdatei enthält Antwortfelder: " + ", ".join(inspector.response_fields[:10])
        )
    if inspector.template_ids:
        warnings.append(
            f"{len(inspector.template_ids)} IDs liegen in inerten Templates; Eindeutigkeit nach der Modus-Instanziierung per Browser-QA prüfen."
        )

    remote = sorted({source for source in inspector.resources if is_remote(source)})
    if remote:
        message = "Remote-Ressourcen prüfen: " + ", ".join(remote[:10])
        (warnings if args.allow_remote else errors).append(message)

    remote_links = sorted({link for link in inspector.links if is_remote(link)})
    if remote_links:
        warnings.append("Externe Verweise fachlich und rechtlich prüfen: " + ", ".join(remote_links[:10]))

    missing_local: list[str] = []
    for source in inspector.resources:
        parsed = urlparse(source)
        if parsed.scheme or source.startswith(("//", "/")):
            continue
        candidate = (path.parent / parsed.path).resolve()
        if parsed.path and not candidate.exists():
            missing_local.append(source)
    if missing_local:
        errors.append("Fehlende lokale Ressourcen: " + ", ".join(sorted(set(missing_local))[:10]))

    combined_script = "\n".join(inspector.scripts)
    definitions = set(re.findall(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(", combined_script))
    definitions.update(re.findall(r"\b(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function|\([^)]*\)\s*=>)", combined_script))
    calls = set()
    for handler in inspector.handlers:
        calls.update(re.findall(r"\b([A-Za-z_$][\w$]*)\s*\(", handler))
    builtins = {"alert", "confirm", "prompt", "print", "setTimeout", "clearTimeout"}
    undefined = sorted(calls - definitions - builtins)
    if undefined:
        warnings.append("Inline-Handler möglicherweise ohne Definition: " + ", ".join(undefined))

    password_patterns = [
        r"LEHRER_PASS\s*=\s*['\"](?!\[|VOR_|PLACEHOLDER|CHANGEME)([^'\"]{4,})",
        r"password\s*[:=]\s*['\"]([^'\"]{4,})",
    ]
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in password_patterns):
        errors.append("Mögliches Klartextpasswort im HTML/JavaScript gefunden.")

    node = shutil.which("node")
    if node:
        for index, script in enumerate(inspector.scripts, 1):
            if not script.strip():
                continue
            try:
                check = subprocess.run(
                    [node, "--check", "-"],
                    input=script,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=20,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"JavaScript-Prüfung in Inline-Skript {index} hat das Zeitlimit überschritten.")
                continue
            if check.returncode:
                errors.append(f"JavaScript-Syntaxfehler in Inline-Skript {index}: {check.stderr.strip()}")
    else:
        warnings.append("Node.js nicht gefunden; JavaScript-Syntax nicht geprüft.")

    print(f"Datei: {path}")
    print(
        f"Aktive IDs: {len(inspector.ids)} | Template-IDs: {len(inspector.template_ids)} | "
        f"Skripte: {len(inspector.scripts)} | Lehrerblöcke: {inspector.teacher_nodes}"
    )
    for item in warnings:
        print("WARNUNG: " + item)
    for item in errors:
        print("FEHLER: " + item)
    print("ERGEBNIS: " + ("NICHT BESTANDEN" if errors else "BESTANDEN"))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
