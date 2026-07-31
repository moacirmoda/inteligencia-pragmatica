from copy import deepcopy
from pathlib import Path

import yaml

from pragmatic.cli import main
from pragmatic.engine import next_action
from pragmatic.render import render_markdown


def test_next_action(complete_document, method):
    assert next_action(complete_document, method)["kind"] == "execute"
    complete_document["execution"]["current_cycle"]["tatt"]["task"] = None
    assert next_action(complete_document, method)["path"] == "execution.current_cycle.tatt.task"


def test_render_markdown(complete_document, method):
    rendered = render_markdown(complete_document, method)
    assert "# Aprender piano" in rendered
    assert "## PMV — 8Rs" in rendered
    assert "## Próxima ação coerente" in rendered


def test_render_idempotent(complete_document, method):
    assert render_markdown(complete_document, method) == render_markdown(
        deepcopy(complete_document), method
    )


def test_init_idempotent(tmp_path, capsys):
    target = tmp_path / "goal.yaml"
    assert main(["init", str(target), "--title", "Meta teste"]) == 0
    first = target.read_bytes()
    assert main(["init", str(target), "--title", "Outro título"]) == 0
    assert target.read_bytes() == first
    assert "unchanged" in capsys.readouterr().out


def test_all_eval_contexts_exist():
    cases = yaml.safe_load(Path("evals/cases.yaml").read_text(encoding="utf-8"))["cases"]
    assert {case["id"] for case in cases} == {
        "double-recurring-revenue",
        "executive-hire",
        "learn-piano",
        "write-book",
        "choose-city",
        "short-session",
        "stalled-review",
    }
