import re
from typing import Dict, Tuple

from .torch_tokenizer import normalize_text, strip_accents, tokenize


CRUD_INTENTS: Dict[str, str] = {
    "criar": "CREATE",
    "crie": "CREATE",
    "gerar": "CREATE",
    "gere": "CREATE",
    "inserir": "CREATE",
    "inserir": "CREATE",
    "adicionar": "CREATE",
    "add": "CREATE",
    "buscar": "READ",
    "procurar": "READ",
    "listar": "READ",
    "mostrar": "READ",
    "ler": "READ",
    "consultar": "READ",
    "atualizar": "UPDATE",
    "alterar": "UPDATE",
    "editar": "UPDATE",
    "modificar": "UPDATE",
    "remover": "DELETE",
    "deletar": "DELETE",
    "apagar": "DELETE",
    "excluir": "DELETE",
}


def _is_word(tok: str) -> bool:
    return any(ch.isalpha() for ch in tok)


def detect_intent_and_strip(text: str) -> Tuple[str, str]:
    text = normalize_text(text)
    toks = tokenize(text)
    if not toks:
        return "UNKNOWN", ""

    norm = [strip_accents(t.lower()) for t in toks]
    idx = None
    intent = "UNKNOWN"
    for i, nt in enumerate(norm):
        if not _is_word(toks[i]):
            continue
        if nt in CRUD_INTENTS:
            idx = i
            intent = CRUD_INTENTS[nt]
            break

    if idx is None:
        return intent, text

    kept = [t for j, t in enumerate(toks) if j != idx]
    out = " ".join(kept)
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    out = re.sub(r"\(\s+", "(", out)
    out = re.sub(r"\s+\)", ")", out)
    out = re.sub(r"\s+", " ", out).strip()
    return intent, out


def detect_intent(text: str) -> str:
    return detect_intent_and_strip(text)[0]

