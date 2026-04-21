try:
    import torch
except ModuleNotFoundError:
    raise

from nlp import NLPFacade
from nlp.intent import detect_intent_and_strip
from nlp.sentiment import get_sentiment

def _assert_contains_all(got, expected_set):
    got_set = {w.lower() for w in got}
    missing = {w.lower() for w in expected_set} - got_set
    assert not missing, f"Missing {missing} in {got}"


def test_palavras_fortes_contexto_objetos_exemplo():
    nlp = NLPFacade()
    text = "crie uma casa pintada de rosa"
    got = nlp.palavras_fortes_contexto_objetos(text)
    _assert_contains_all(got, {"casa", "rosa"})


def test_palavras_fortes_contexto_objetos_outro():
    nlp = NLPFacade()
    text = "gerar um relatório PDF com capa azul"
    got = nlp.palavras_fortes_contexto_objetos(text)
    _assert_contains_all(got, {"relatório", "pdf", "azul"})


def test_varios_contextos_nao_quebra():
    nlp = NLPFacade()
    textos = [
        "buscar pedidos do cliente Maria",
        "remover usuário com email teste@exemplo.com",
        "atualizar endereço para rua das flores 123",
        "quero uma maçã verde",
        "exportar dados em csv separado por vírgula",
        "criar tabela produtos com coluna preço",
        "gerar gráfico de vendas por mês",
    ]
    for t in textos:
        got = nlp.palavras_fortes_contexto_objetos(t)
        assert isinstance(got, list)


def test_intent_crud_strip():
    intent, stripped = detect_intent_and_strip("criar uma coluna")
    assert intent == "CREATE"
    assert stripped.lower() == "uma coluna"

    intent, stripped = detect_intent_and_strip("buscar pedidos do cliente Maria")
    assert intent == "READ"
    assert "buscar" not in stripped.lower()

    intent, stripped = detect_intent_and_strip("remover usuário com email teste@exemplo.com")
    assert intent == "DELETE"
    assert "remover" not in stripped.lower()

    intent, stripped = detect_intent_and_strip("atualizar endereço para rua das flores 123")
    assert intent == "UPDATE"
    assert "atualizar" not in stripped.lower()


def test_sentiment():
    assert get_sentiment("isso é excelente, gostei muito") == "POSITIVE"
    assert get_sentiment("isso é horrível, odeio") == "NEGATIVE"
    assert get_sentiment("isso é um texto qualquer") == "NEUTRAL"
    assert get_sentiment("não é bom") == "NEGATIVE"
    assert get_sentiment("não é ruim") == "POSITIVE"


if __name__ == "__main__":
    test_palavras_fortes_contexto_objetos_exemplo()
    test_palavras_fortes_contexto_objetos_outro()
    test_varios_contextos_nao_quebra()
    test_intent_crud_strip()
    test_sentiment()
    print("OK")


print(detect_intent_and_strip("excluir a cliente Maria"))