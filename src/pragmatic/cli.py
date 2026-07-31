from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from pragmatic.engine import next_action, status
from pragmatic.io import DocumentError, dump_yaml, load_method, load_template, load_yaml
from pragmatic.render import render_markdown
from pragmatic.validation import summary, validate_document, validate_method


def _slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "objetivo"


def _print_findings(findings: list, as_json: bool) -> None:
    if as_json:
        print(
            json.dumps(
                {"summary": summary(findings), "findings": [item.to_dict() for item in findings]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    counts = summary(findings)
    print(" ".join(f"{name}={count}" for name, count in counts.items()))
    for item in findings:
        print(f"[{item.severity}] {item.path}: {item.message} ({item.code})")


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    if target.exists():
        print(f"unchanged: {target}")
        return 0
    document = load_template()
    now = datetime.now(UTC).replace(microsecond=0).isoformat()
    document["metadata"].update(
        {
            "id": _slug(args.title or target.stem),
            "title": args.title,
            "created_at": now,
            "updated_at": now,
            "depth": args.depth,
            "host_workspace": str(Path(args.workspace).resolve()) if args.workspace else None,
        }
    )
    if args.title:
        document["gaps"] = [
            {
                "id": "resultado",
                "question": "Qual resultado deseja alcançar?",
                "blocking_phase": "definir",
                "status": "open",
            },
            {
                "id": "controle",
                "question": "Que esforço ou medida depende de você?",
                "blocking_phase": "definir",
                "status": "open",
            },
        ]
    else:
        document["gaps"] = [
            {
                "id": "titulo",
                "question": "Qual é o objetivo?",
                "blocking_phase": "definir",
                "status": "open",
            }
        ]
    dump_yaml(document, target)
    print(f"created: {target}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    method = load_method(args.method)
    findings = validate_method(method)
    if not findings:
        findings = validate_document(load_yaml(args.path), method)
    _print_findings(findings, args.json)
    return (
        1
        if any(item.severity == "structural_error" for item in findings)
        else 2
        if any(item.severity == "blocking_gap" for item in findings)
        else 0
    )


def cmd_status(args: argparse.Namespace) -> int:
    result = status(load_yaml(args.path), load_method(args.method))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"fase={result['phase']} estado={result['state']} profundidade={result['depth']}")
        blocked = "sim" if result["blocked"] else "não"
        print(
            f"completude={result['completion_percent']}% "
            f"bloqueado={blocked} evidências={result['evidence_count']}"
        )
        print(" ".join(f"{name}={count}" for name, count in result["counts"].items()))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    result = next_action(load_yaml(args.path), load_method(args.method))
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
        if args.json
        else f"{result['kind']}: {result['action']} [{result['path']}]"
    )
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    rendered = render_markdown(load_yaml(args.path), load_method(args.method))
    if args.output:
        target = Path(args.output).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print(f"rendered: {target}")
    else:
        print(rendered)
    return 0


def parser() -> argparse.ArgumentParser:
    main = argparse.ArgumentParser(
        prog="pragmatic", description="Inteligência Pragmática local-first"
    )
    sub = main.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="cria um objetivo sem inventar conteúdo")
    init.add_argument("path")
    init.add_argument("--title")
    init.add_argument("--workspace")
    init.add_argument("--depth", choices=["light", "standard", "deep"], default="standard")
    init.set_defaults(func=cmd_init)
    for name, function in (
        ("validate", cmd_validate),
        ("status", cmd_status),
        ("next", cmd_next),
        ("render", cmd_render),
    ):
        command = sub.add_parser(name)
        command.add_argument("path")
        command.add_argument("--method")
        if name in {"validate", "status", "next"}:
            command.add_argument("--json", action="store_true")
        if name == "render":
            command.add_argument("--output")
        command.set_defaults(func=function)
    return main


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return int(args.func(args))
    except (DocumentError, OSError, ValueError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
