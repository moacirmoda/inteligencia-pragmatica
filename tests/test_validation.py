from pragmatic.validation import can_transition, summary, validate_document


def codes(findings):
    return {item.code for item in findings}


def test_four_cs(complete_document, method):
    complete_document["metadata"]["phase"] = "definir"
    complete_document["pgg"]["four_cs"]["courageous"]["status"] = "absent"
    findings = validate_document(complete_document, method)
    assert "four_c_absent" in codes(findings)
    assert summary(findings)["quality_warning"] >= 1


def test_eight_rs_by_depth(complete_document, method):
    complete_document["metadata"]["phase"] = "planejar"
    complete_document["pmv"]["resources"] = {
        "time": [],
        "money": [],
        "materials": [],
        "people": [],
        "information": [],
    }
    findings = validate_document(complete_document, method)
    assert any(
        item.code == "missing_8r_resources" and item.severity == "blocking_gap" for item in findings
    )


def test_light_does_not_force_all_8rs(complete_document, method):
    complete_document["metadata"].update({"phase": "planejar", "depth": "light"})
    complete_document["pmv"]["reference"] = {
        "principles": [],
        "examples": [],
        "guides": [],
        "experts": [],
    }
    complete_document["pmv"]["resources"] = {
        "time": [],
        "money": [],
        "materials": [],
        "people": [],
        "information": [],
    }
    findings = validate_document(complete_document, method)
    assert not any(
        item.code in {"missing_8r_reference", "missing_8r_resources"}
        and item.severity == "blocking_gap"
        for item in findings
    )


def test_transitions(complete_document, method):
    complete_document["metadata"]["phase"] = "planejar"
    allowed, findings = can_transition(complete_document, "executar", method)
    assert allowed and findings == []
    complete_document["pmv"]["responsibility"]["owner"] = None
    allowed, findings = can_transition(complete_document, "executar", method)
    assert not allowed and findings[0].severity == "blocking_gap"


def test_classification_and_incomplete_document(complete_document, method):
    complete_document["metadata"]["phase"] = "definir"
    complete_document["pgg"]["desired_outcome"] = None
    complete_document["pgg"]["deadline"] = None
    complete_document["pmv"]["resources"] = {}
    findings = validate_document(complete_document, method)
    counts = summary(findings)
    assert counts["blocking_gap"] >= 1
    assert counts["quality_warning"] >= 1
    assert counts["deferred"] >= 1


def test_unknown_fields(complete_document, method):
    complete_document["surprise"] = True
    findings = validate_document(complete_document, method)
    assert any(
        item.code == "unknown_field" and item.severity == "structural_error" for item in findings
    )


def test_deep_risk_requires_plan_b(complete_document, method):
    complete_document["metadata"]["depth"] = "deep"
    complete_document["pmv"]["risks"][0]["plan_b"] = None
    findings = validate_document(complete_document, method)
    assert any(
        item.code == "risk_missing_plan_b" and item.severity == "blocking_gap" for item in findings
    )


def test_execution_requires_tatt(complete_document, method):
    complete_document["execution"]["current_cycle"]["tatt"]["tangible"] = None
    findings = validate_document(complete_document, method)
    assert "missing_tatt_tangible" in codes(findings)


def test_completed_cycle_requires_dpa(complete_document, method):
    complete_document["execution"]["current_cycle"]["status"] = "completed"
    findings = validate_document(complete_document, method)
    assert "missing_dpa" in codes(findings)


def test_open_gap_is_classified_by_phase(complete_document, method):
    complete_document["metadata"]["phase"] = "planejar"
    complete_document["gaps"] = [
        {
            "id": "needed",
            "question": "Qual informação falta?",
            "blocking_phase": "planejar",
            "status": "open",
        },
        {
            "id": "later",
            "question": "Qual feedback será usado?",
            "blocking_phase": "revisar",
            "status": "open",
        },
    ]
    findings = validate_document(complete_document, method)
    assert any(item.path == "gaps.0" and item.severity == "blocking_gap" for item in findings)
    assert any(item.path == "gaps.1" and item.severity == "deferred" for item in findings)
