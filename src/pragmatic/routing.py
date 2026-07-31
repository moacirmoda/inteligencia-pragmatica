from __future__ import annotations

MODE_TERMS = {
    "definir": ("pgg", "definir objetivo", "transforme este objetivo"),
    "planejar": ("pmv", "8rs", "planejar", "monte o plano"),
    "executar": ("próxima sessão", "sessão pragmática", "próxima ação", "executar"),
    "revisar": ("revisar", "revise", "não está avançando", "atualize o plano"),
    "completo": ("aplique inteligência pragmática", "método completo", "framework completo"),
}


def detect_mode(request: str) -> str:
    normalized = request.casefold()
    for mode in ("definir", "planejar", "executar", "revisar", "completo"):
        if any(term in normalized for term in MODE_TERMS[mode]):
            return mode
    return "completo"


def recommend_depth(impact: str, reversibility: str, short_task: bool = False) -> str:
    if short_task:
        return "light"
    score = {"low": 0, "medium": 1, "high": 2}
    impact_score = score.get(impact, 1)
    irreversible_score = {"high": 0, "medium": 1, "low": 2}.get(reversibility, 1)
    combined = max(impact_score, irreversible_score)
    return ("light", "standard", "deep")[combined]
