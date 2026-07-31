from pragmatic.routing import detect_mode, recommend_depth
from pragmatic.validation import validate_method


def test_method_parsing(method):
    assert validate_method(method) == []
    assert set(method["phases"]) == {"definir", "planejar", "executar", "revisar", "arquivado"}
    assert method["execution_skills"]["research"]["models"]["PERG"] == [
        "pergunte",
        "explore",
        "revise",
        "guarde",
    ]
    assert len(method["artifacts"]["pmv"]["components"]) == 8


def test_routing_modes():
    assert detect_mode("Transforme este objetivo em um PGG") == "definir"
    assert detect_mode("Monte o PMV deste objetivo") == "planejar"
    assert detect_mode("Qual é a próxima sessão pragmática?") == "executar"
    assert detect_mode("Revise meu progresso e atualize o plano") == "revisar"


def test_depth_routing_spec():
    assert recommend_depth("low", "high", short_task=True) == "light"
    assert recommend_depth("medium", "medium") == "standard"
    assert recommend_depth("high", "low") == "deep"
