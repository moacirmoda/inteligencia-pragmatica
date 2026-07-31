from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

from pragmatic.io import load_template

PHASE_ORDER = ["definir", "planejar", "executar", "revisar", "arquivado"]
VALID_DEPTHS = {"light", "standard", "deep"}
VALID_4C_STATUS = {"unknown", "present", "absent", "not_applicable"}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def get_path(document: dict[str, Any], path: str) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_missing(value: Any) -> bool:
    if value is None or value == "":
        return True
    if isinstance(value, list):
        return not value or all(is_missing(item) for item in value)
    if isinstance(value, dict):
        return not value or all(is_missing(item) for item in value.values())
    return False


def _unknown_fields(value: Any, template: Any, path: str = "") -> Iterable[Finding]:
    if isinstance(value, dict) and isinstance(template, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key not in template:
                yield Finding(
                    "structural_error",
                    "unknown_field",
                    child_path,
                    "Campo desconhecido; preserve extensões em evidências ou notas, não no schema.",
                )
            else:
                yield from _unknown_fields(child, template[key], child_path)


def validate_method(method: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    required = {
        "method",
        "severities",
        "phases",
        "transitions",
        "artifacts",
        "execution_skills",
        "routing",
        "quality_criteria",
    }
    for key in sorted(required - method.keys()):
        findings.append(
            Finding("structural_error", "method_missing_key", key, "Chave obrigatória.")
        )
    phases = method.get("phases")
    if isinstance(phases, dict):
        for phase in PHASE_ORDER:
            if phase not in phases:
                findings.append(
                    Finding(
                        "structural_error",
                        "method_missing_phase",
                        f"phases.{phase}",
                        "Fase ausente.",
                    )
                )
    else:
        findings.append(
            Finding("structural_error", "method_phases_type", "phases", "Deve ser objeto.")
        )
    return findings


def _validate_structure(document: dict[str, Any]) -> list[Finding]:
    findings = list(_unknown_fields(document, load_template()))
    required = {
        "schema_version",
        "metadata",
        "pgg",
        "pmv",
        "gaps",
        "hypotheses",
        "decisions",
        "facts",
        "metrics",
        "execution",
        "review_history",
    }
    for key in sorted(required - document.keys()):
        findings.append(
            Finding("structural_error", "missing_root_field", key, "Campo raiz obrigatório.")
        )
    if document.get("schema_version") != 1:
        findings.append(
            Finding("structural_error", "schema_version", "schema_version", "Versão suportada: 1.")
        )
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        findings.append(
            Finding("structural_error", "metadata_type", "metadata", "Deve ser objeto.")
        )
        return findings
    phase = metadata.get("phase")
    if phase not in PHASE_ORDER:
        findings.append(
            Finding("structural_error", "invalid_phase", "metadata.phase", "Fase inválida.")
        )
    depth = metadata.get("depth")
    if depth not in VALID_DEPTHS:
        findings.append(
            Finding("structural_error", "invalid_depth", "metadata.depth", "Profundidade inválida.")
        )
    for path in ("gaps", "hypotheses", "decisions", "facts", "review_history"):
        if not isinstance(document.get(path), list):
            findings.append(
                Finding("structural_error", "invalid_collection", path, "Deve ser lista.")
            )
    return findings


def _validate_four_cs(document: dict[str, Any], phase: str) -> list[Finding]:
    findings: list[Finding] = []
    four_cs = get_path(document, "pgg.four_cs")
    if not isinstance(four_cs, dict):
        return [Finding("structural_error", "four_cs_type", "pgg.four_cs", "Deve ser objeto.")]
    for key in ("concise", "courageous", "controllable", "committed"):
        entry = four_cs.get(key)
        path = f"pgg.four_cs.{key}"
        if not isinstance(entry, dict):
            findings.append(Finding("structural_error", "four_c_type", path, "Deve ser objeto."))
            continue
        status = entry.get("status")
        if status not in VALID_4C_STATUS:
            findings.append(
                Finding("structural_error", "four_c_status", f"{path}.status", "Status inválido.")
            )
        elif status == "absent":
            findings.append(
                Finding("quality_warning", "four_c_absent", path, f"4C '{key}' não atendido.")
            )
        elif status == "unknown":
            severity = (
                "blocking_gap" if phase == "definir" and key == "controllable" else "recommendation"
            )
            findings.append(Finding(severity, "four_c_unknown", path, f"Avaliar o 4C '{key}'."))
    if is_missing(get_path(document, "pgg.deadline")):
        findings.append(
            Finding(
                "quality_warning",
                "missing_deadline",
                "pgg.deadline",
                "Objetivo ainda não é conciso.",
            )
        )
    if is_missing(get_path(document, "pgg.desired_outcome")):
        findings.append(
            Finding(
                "blocking_gap",
                "missing_outcome",
                "pgg.desired_outcome",
                "Definir o resultado desejado.",
            )
        )
    if is_missing(get_path(document, "pgg.controllable_measure")):
        findings.append(
            Finding(
                "blocking_gap",
                "missing_controllable",
                "pgg.controllable_measure",
                "Definir esforço ou medida controlável.",
            )
        )
    return findings


PMV_PATHS = {
    "result": "pmv.result",
    "reason": "pmv.reason",
    "reference": "pmv.reference",
    "direction": "pmv.direction",
    "resources": "pmv.resources",
    "constraints": "pmv.constraints",
    "risks": "pmv.risks",
    "responsibility": "pmv.responsibility.owner",
}


def _validate_pmvs(document: dict[str, Any], phase: str, depth: str) -> list[Finding]:
    findings: list[Finding] = []
    required = {"result", "reason", "direction", "responsibility"}
    if depth in {"standard", "deep"}:
        required = set(PMV_PATHS)
    for name, path in PMV_PATHS.items():
        if not is_missing(get_path(document, path)):
            continue
        if phase == "definir":
            severity = "deferred"
        elif name in required and phase in {"planejar", "executar", "revisar"}:
            severity = "blocking_gap"
        else:
            severity = "deferred"
        findings.append(
            Finding(severity, f"missing_8r_{name}", path, f"8R '{name}' não preenchido.")
        )

    risks = get_path(document, "pmv.risks")
    if isinstance(risks, list):
        for index, risk in enumerate(risks):
            if not isinstance(risk, dict):
                findings.append(
                    Finding(
                        "structural_error",
                        "risk_type",
                        f"pmv.risks.{index}",
                        "Risco deve ser objeto.",
                    )
                )
                continue
            for field in ("description", "threat", "vulnerability"):
                if is_missing(risk.get(field)):
                    findings.append(
                        Finding(
                            "quality_warning",
                            f"risk_missing_{field}",
                            f"pmv.risks.{index}.{field}",
                            "Detalhar o risco.",
                        )
                    )
            for field in ("mitigation", "plan_b"):
                if is_missing(risk.get(field)):
                    severity = "blocking_gap" if depth == "deep" else "quality_warning"
                    findings.append(
                        Finding(
                            severity,
                            f"risk_missing_{field}",
                            f"pmv.risks.{index}.{field}",
                            "Definir resposta.",
                        )
                    )
    return findings


def _validate_records(document: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for collection in ("facts", "hypotheses", "decisions"):
        values = document.get(collection)
        if not isinstance(values, list):
            continue
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                findings.append(
                    Finding(
                        "structural_error",
                        "record_type",
                        f"{collection}.{index}",
                        "Registro deve ser objeto.",
                    )
                )
                continue
            if is_missing(item.get("statement")):
                findings.append(
                    Finding(
                        "quality_warning",
                        "record_statement",
                        f"{collection}.{index}.statement",
                        "Registro sem enunciado.",
                    )
                )
            if collection == "facts" and is_missing(item.get("evidence")):
                findings.append(
                    Finding(
                        "quality_warning",
                        "fact_without_evidence",
                        f"facts.{index}.evidence",
                        "Fato material sem evidência.",
                    )
                )
    return findings


def _validate_gaps(document: dict[str, Any], phase: str) -> list[Finding]:
    findings: list[Finding] = []
    gaps = document.get("gaps")
    if not isinstance(gaps, list):
        return findings
    current_index = PHASE_ORDER.index(phase)
    for index, gap in enumerate(gaps):
        path = f"gaps.{index}"
        if not isinstance(gap, dict):
            findings.append(
                Finding("structural_error", "gap_type", path, "Lacuna deve ser objeto.")
            )
            continue
        if gap.get("status", "open") not in {"open", "resolved", "dismissed"}:
            findings.append(
                Finding("structural_error", "gap_status", f"{path}.status", "Status inválido.")
            )
            continue
        if gap.get("status", "open") != "open":
            continue
        question = gap.get("question") or "Resolver a lacuna registrada."
        blocking_phase = gap.get("blocking_phase")
        if blocking_phase not in PHASE_ORDER:
            findings.append(
                Finding(
                    "structural_error",
                    "gap_blocking_phase",
                    f"{path}.blocking_phase",
                    "Fase bloqueada inválida.",
                )
            )
            continue
        severity = (
            "blocking_gap"
            if phase != "arquivado" and PHASE_ORDER.index(blocking_phase) <= current_index
            else "deferred"
        )
        findings.append(Finding(severity, "open_gap", path, question))
    return findings


def _validate_execution(document: dict[str, Any], phase: str) -> list[Finding]:
    findings: list[Finding] = []
    if phase not in {"executar", "revisar"}:
        return findings
    for field in ("task", "tangible", "timebox_minutes"):
        path = f"execution.current_cycle.tatt.{field}"
        if is_missing(get_path(document, path)):
            findings.append(
                Finding(
                    "blocking_gap", f"missing_tatt_{field}", path, "Completar a Sessão Pragmática."
                )
            )
    dpa = get_path(document, "execution.current_cycle.dpa.kind")
    status = get_path(document, "execution.current_cycle.status")
    if status == "completed" and dpa not in {"decision", "next_action", "archive"}:
        findings.append(
            Finding(
                "blocking_gap",
                "missing_dpa",
                "execution.current_cycle.dpa.kind",
                "Fechar o ciclo em DPA.",
            )
        )
    if dpa == "next_action":
        for field in ("description", "owner", "due"):
            path = f"execution.current_cycle.next_action.{field}"
            if is_missing(get_path(document, path)):
                findings.append(
                    Finding(
                        "blocking_gap",
                        f"next_action_{field}",
                        path,
                        "Próxima ação exige conteúdo, dono e prazo.",
                    )
                )
    return findings


def validate_document(
    document: dict[str, Any], method: dict[str, Any] | None = None
) -> list[Finding]:
    findings = _validate_structure(document)
    if any(item.severity == "structural_error" for item in findings):
        return sorted(findings, key=lambda item: (item.severity, item.path, item.code))
    phase = get_path(document, "metadata.phase")
    depth = get_path(document, "metadata.depth")
    findings.extend(_validate_four_cs(document, phase))
    findings.extend(_validate_pmvs(document, phase, depth))
    findings.extend(_validate_records(document))
    findings.extend(_validate_gaps(document, phase))
    findings.extend(_validate_execution(document, phase))
    return sorted(findings, key=lambda item: (item.severity, item.path, item.code))


def can_transition(
    document: dict[str, Any], target: str, method: dict[str, Any]
) -> tuple[bool, list[Finding]]:
    source = get_path(document, "metadata.phase")
    match = next(
        (
            item
            for item in method.get("transitions", [])
            if item.get("from") == source and item.get("to") == target
        ),
        None,
    )
    if match is None:
        return False, [
            Finding(
                "structural_error",
                "transition_not_allowed",
                "metadata.phase",
                f"Transição {source} -> {target} não permitida.",
            )
        ]
    missing = [path for path in match.get("requires", []) if is_missing(get_path(document, path))]
    return not missing, [
        Finding(
            "blocking_gap", "transition_requirement", path, f"Necessário para avançar a {target}."
        )
        for path in missing
    ]


def summary(findings: list[Finding]) -> dict[str, int]:
    result = {
        name: 0
        for name in (
            "structural_error",
            "blocking_gap",
            "quality_warning",
            "recommendation",
            "deferred",
        )
    }
    for finding in findings:
        result[finding.severity] = result.get(finding.severity, 0) + 1
    return result
