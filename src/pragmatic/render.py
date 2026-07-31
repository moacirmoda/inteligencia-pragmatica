from __future__ import annotations

from typing import Any

from pragmatic.engine import next_action, status
from pragmatic.validation import get_path


def _value(value: Any) -> str:
    if value is None or value == "" or value == []:
        return "_lacuna_"
    if isinstance(value, list):
        return ", ".join(
            _value(item) if not isinstance(item, dict) else str(item) for item in value
        )
    return str(value)


def _bullets(values: Any) -> list[str]:
    if not isinstance(values, list) or not values:
        return ["- _lacuna_"]
    rendered = []
    for value in values:
        if isinstance(value, dict):
            main = (
                value.get("description")
                or value.get("statement")
                or value.get("name")
                or str(value)
            )
            rendered.append(f"- {main}")
        else:
            rendered.append(f"- {value}")
    return rendered


def render_markdown(document: dict[str, Any], method: dict[str, Any]) -> str:
    current = status(document, method)
    upcoming = next_action(document, method)
    title = get_path(document, "metadata.title") or "Objetivo sem título"
    blocked = "sim" if current["blocked"] else "não"
    lines = [
        f"# {title}",
        "",
        f"**Fase:** {current['phase']} · **Estado:** {current['state']} · "
        f"**Profundidade:** {current['depth']}",
        f"**Completude:** {current['completion_percent']}% · **Bloqueado:** {blocked}",
        "",
        "## PGG",
        "",
        f"- Formulação: {_value(get_path(document, 'pgg.statement'))}",
        f"- Resultado desejado: {_value(get_path(document, 'pgg.desired_outcome'))}",
        f"- Medida controlável: {_value(get_path(document, 'pgg.controllable_measure'))}",
        f"- Prazo: {_value(get_path(document, 'pgg.deadline'))}",
        f"- Ganho mesmo se falhar: {_value(get_path(document, 'pgg.win_even_if_fail'))}",
        "",
        "### 4Cs",
        "",
    ]
    for key, label in (
        ("concise", "Conciso"),
        ("courageous", "Corajoso"),
        ("controllable", "Controlável"),
        ("committed", "Comprometido"),
    ):
        status_value = _value(get_path(document, f"pgg.four_cs.{key}.status"))
        rationale = _value(get_path(document, f"pgg.four_cs.{key}.rationale"))
        lines.append(f"- {label}: {status_value} — {rationale}")
    lines.extend(["", "## PMV — 8Rs", ""])
    labels = (
        ("result", "Resultado"),
        ("reason", "Razão"),
        ("reference", "Referência (PEGE)"),
        ("direction", "Rumo"),
        ("resources", "Recursos"),
        ("constraints", "Restrições"),
        ("risks", "Riscos"),
        ("responsibility", "Responsabilidade"),
    )
    for key, label in labels:
        lines.append(f"### {label}")
        lines.append("")
        value = get_path(document, f"pmv.{key}")
        if isinstance(value, list):
            lines.extend(_bullets(value))
        elif isinstance(value, dict):
            nonempty = {name: item for name, item in value.items() if item not in (None, [], {})}
            lines.extend(
                [f"- {name}: {_value(item)}" for name, item in nonempty.items()] or ["- _lacuna_"]
            )
        else:
            lines.append(_value(value))
        lines.append("")
    lines.extend(
        [
            "## Lacunas",
            "",
            *_bullets(document.get("gaps")),
            "",
            "## Hipóteses",
            "",
            *_bullets(document.get("hypotheses")),
            "",
            "## Decisões",
            "",
            *_bullets(document.get("decisions")),
            "",
            "## Ciclo atual",
            "",
        ]
    )
    tatt = get_path(document, "execution.current_cycle.tatt") or {}
    lines.extend(
        [
            f"- Tarefa: {_value(tatt.get('task'))}",
            f"- Alvo: {_value(tatt.get('target'))}",
            f"- Tangível: {_value(tatt.get('tangible'))}",
            f"- Tempo: {_value(tatt.get('timebox_minutes'))} minutos",
            "",
            "## Próxima ação coerente",
            "",
            f"**{upcoming['kind']}:** {upcoming['action']} (`{upcoming['path']}`)",
            "",
            "## Histórico de revisões",
            "",
            *_bullets(document.get("review_history")),
            "",
        ]
    )
    return "\n".join(lines)
