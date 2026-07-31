from pathlib import Path

import yaml

from pragmatic.routing import detect_mode, recommend_depth


def test_behavioral_eval_routing_and_depth():
    cases = yaml.safe_load(Path("evals/cases.yaml").read_text(encoding="utf-8"))["cases"]
    for case in cases:
        assert detect_mode(case["request"]) == case["expected_mode"], case["id"]
        depth = recommend_depth(
            case["impact"],
            case["reversibility"],
            short_task=case.get("short_task", False),
        )
        assert depth == case["expected_depth"], case["id"]


def test_short_execution_does_not_request_full_plan():
    cases = yaml.safe_load(Path("evals/cases.yaml").read_text(encoding="utf-8"))["cases"]
    short = next(case for case in cases if case["id"] == "short-session")
    assert "force_all_8Rs" in short["forbidden"]
    assert short["must_use"] == ["TATT", "DPA"]
