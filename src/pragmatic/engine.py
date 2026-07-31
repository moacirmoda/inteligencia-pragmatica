from __future__ import annotations

from typing import Any

from pragmatic.validation import Finding, get_path, is_missing, summary, validate_document


def completion(document: dict[str, Any]) -> int:
    phase = get_path(document, "metadata.phase")
    paths = ["metadata.title", "pgg.desired_outcome", "pgg.controllable_measure"]
    if phase in {"planejar", "executar", "revisar"}:
        paths.extend(
            [
                "pmv.result",
                "pmv.reason",
                "pmv.direction",
                "pmv.constraints",
                "pmv.risks",
                "pmv.responsibility.owner",
            ]
        )
    if phase in {"executar", "revisar"}:
        paths.extend(
            [
                "execution.current_cycle.tatt.task",
                "execution.current_cycle.tatt.tangible",
                "execution.current_cycle.tatt.timebox_minutes",
            ]
        )
    present = sum(not is_missing(get_path(document, path)) for path in paths)
    return round(100 * present / len(paths)) if paths else 100


def status(document: dict[str, Any], method: dict[str, Any]) -> dict[str, Any]:
    findings = validate_document(document, method)
    evidence = []
    for path in ("facts", "execution.current_cycle.evidence", "review_history"):
        value = get_path(document, path)
        if isinstance(value, list):
            evidence.extend(value)
    return {
        "phase": get_path(document, "metadata.phase"),
        "state": get_path(document, "metadata.state"),
        "depth": get_path(document, "metadata.depth"),
        "completion_percent": completion(document),
        "counts": summary(findings),
        "blocked": any(item.severity in {"structural_error", "blocking_gap"} for item in findings),
        "evidence_count": len(evidence),
    }


def _first(findings: list[Finding], severity: str) -> Finding | None:
    return next((item for item in findings if item.severity == severity), None)


def next_action(document: dict[str, Any], method: dict[str, Any]) -> dict[str, str]:
    findings = validate_document(document, method)
    structural = _first(findings, "structural_error")
    if structural:
        return {"kind": "repair", "path": structural.path, "action": structural.message}

    phase = get_path(document, "metadata.phase")
    explicit_gaps = document.get("gaps", [])
    for gap in explicit_gaps if isinstance(explicit_gaps, list) else []:
        if not isinstance(gap, dict) or gap.get("status", "open") != "open":
            continue
        if gap.get("blocking_phase") in {None, phase}:
            return {
                "kind": "answer_gap",
                "path": f"gaps.{gap.get('id', '?')}",
                "action": gap.get("question") or "Resolver a lacuna registrada.",
            }

    blocking = _first(findings, "blocking_gap")
    if blocking:
        return {"kind": "fill_gap", "path": blocking.path, "action": blocking.message}

    if phase == "definir":
        return {
            "kind": "checkpoint",
            "path": "pgg",
            "action": "Confirmar o PGG e avançar para Planejar.",
        }
    if phase == "planejar":
        return {
            "kind": "checkpoint",
            "path": "pmv",
            "action": "Confirmar o PMV e preparar uma Sessão Pragmática.",
        }
    if phase == "executar":
        status_value = get_path(document, "execution.current_cycle.status")
        if status_value == "not_started":
            return {
                "kind": "execute",
                "path": "execution.current_cycle",
                "action": "Iniciar a Sessão Pragmática definida.",
            }
        if status_value == "completed":
            return {
                "kind": "review",
                "path": "execution.current_cycle",
                "action": "Registrar feedback e revisar o plano.",
            }
        return {
            "kind": "produce",
            "path": "execution.current_cycle.tatt.tangible",
            "action": "Produzir o tangível da sessão e fechar em DPA.",
        }
    if phase == "revisar":
        return {
            "kind": "review",
            "path": "review_history",
            "action": "Registrar revisão e definir próxima ação com dono e prazo, ou arquivar.",
        }
    return {
        "kind": "archive",
        "path": "metadata.phase",
        "action": "Objetivo arquivado; nenhuma ação pendente.",
    }
