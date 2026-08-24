from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from validate_learning_html import Inspector


def inspect(path: Path) -> Inspector:
    parser = Inspector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prüft die Rollentrennung und Schrittidentität eines Schüler-/Lehrer-/Beamer-Builds."
    )
    parser.add_argument("student", type=Path)
    parser.add_argument("teacher", type=Path)
    parser.add_argument("beamer", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paths = {
        "student": args.student.resolve(),
        "teacher": args.teacher.resolve(),
        "beamer": args.beamer.resolve(),
    }
    for role, path in paths.items():
        if not path.is_file():
            raise SystemExit(f"{role}: Datei fehlt: {path}")

    views = {role: inspect(path) for role, path in paths.items()}
    errors: list[str] = []
    warnings: list[str] = []

    for role, view in views.items():
        duplicate_ids = duplicates(view.ids)
        if duplicate_ids:
            errors.append(f"{role}: doppelte aktive IDs: {', '.join(duplicate_ids[:20])}")

    if views["student"].teacher_nodes:
        errors.append(f"student: {views['student'].teacher_nodes} Lehrerblöcke ausgeliefert")
    if views["beamer"].teacher_nodes:
        errors.append(f"beamer: {views['beamer'].teacher_nodes} Lehrerblöcke ausgeliefert")
    if views["beamer"].response_fields:
        errors.append(
            "beamer: Antwortfelder ausgeliefert: "
            + ", ".join(views["beamer"].response_fields[:20])
        )
    if not views["teacher"].teacher_nodes:
        warnings.append("teacher: keine markierten Lehrerblöcke gefunden")

    student_steps = set(views["student"].steps)
    teacher_steps = set(views["teacher"].steps)
    beamer_steps = set(views["beamer"].steps)
    if student_steps or teacher_steps or beamer_steps:
        if student_steps != beamer_steps:
            missing = sorted(student_steps - beamer_steps)
            extra = sorted(beamer_steps - student_steps)
            errors.append(
                "Schüler-/Beamerschritte weichen ab"
                + (f"; fehlen am Beamer: {', '.join(missing[:10])}" if missing else "")
                + (f"; zusätzlich am Beamer: {', '.join(extra[:10])}" if extra else "")
            )
        if not student_steps.issubset(teacher_steps):
            errors.append(
                "Lehreransicht kennt nicht alle Schülerschritte: "
                + ", ".join(sorted(student_steps - teacher_steps)[:10])
            )
    else:
        warnings.append("Keine stabilen Beamer-/Schritt-IDs gefunden; Scrollkopplung nicht prüfbar")

    report = {
        "files": {role: str(path) for role, path in paths.items()},
        "active_ids": {role: len(view.ids) for role, view in views.items()},
        "template_ids": {role: len(view.template_ids) for role, view in views.items()},
        "steps": {role: len(view.steps) for role, view in views.items()},
        "teacher_nodes": {role: view.teacher_nodes for role, view in views.items()},
        "beamer_response_fields": views["beamer"].response_fields,
        "warnings": warnings,
        "errors": errors,
        "ok": not errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Rollentrennung: " + ("BESTANDEN" if report["ok"] else "NICHT BESTANDEN"))
        for warning in warnings:
            print("WARNUNG: " + warning)
        for error in errors:
            print("FEHLER: " + error)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
