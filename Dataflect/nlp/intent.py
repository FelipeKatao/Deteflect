import re
from typing import Dict, List, Optional, Tuple

from .torch_tokenizer import normalize_text, strip_accents, tokenize

CRUD_INTENTS: Dict[str, str] = {
    "criar": "CREATE",
    "crie": "CREATE",
    "gerar": "CREATE",
    "gere": "CREATE",
    "inserir": "CREATE",
    "adicionar": "CREATE",
    "add": "CREATE",
    "buscar": "READ",
    "procurar": "READ",
    "listar": "READ",
    "mostrar": "READ",
    "exibir": "READ",
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
    "liste": "READ",
    "lista": "READ",
}

_PREFIX_INTENTS: List[Tuple[str, str]] = [
    ("cri", "CREATE"),
    ("ger", "CREATE"),
    ("inser", "CREATE"),
    ("adicion", "CREATE"),
    ("add", "CREATE"),
    ("busc", "READ"),
    ("procur", "READ"),
    ("list", "READ"),
    ("mostr", "READ"),
    ("exib", "READ"),
    ("consult", "READ"),
    ("ler", "READ"),
    ("atualiz", "UPDATE"),
    ("alter", "UPDATE"),
    ("edit", "UPDATE"),
    ("modific", "UPDATE"),
    ("remov", "DELETE"),
    ("delet", "DELETE"),
    ("apag", "DELETE"),
    ("exclu", "DELETE"),
    ("remo", "DELETE"),
    ("cria", "CREATE"),
    ("gera", "CREATE"),
]

def _is_word(tok: str) -> bool:
    return any(ch.isalpha() for ch in tok)


def _intent_from_prefix(nt: str) -> Optional[str]:
    if len(nt) < 3:
        return None
    for prefix, intent in _PREFIX_INTENTS:
        if nt.startswith(prefix):
            return intent
    return None


def _strip_intent_token(toks: List[str], idx: int) -> str:
    kept = [t for j, t in enumerate(toks) if j != idx]
    out = " ".join(kept)
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    out = re.sub(r"\(\s+", "(", out)
    out = re.sub(r"\s+\)", ")", out)
    return re.sub(r"\s+", " ", out).strip()

def detect_intent_and_strip(text: str) -> Tuple[str, str]:
    text = normalize_text(text)
    toks = tokenize(text)
    if not toks:
        return "UNKNOWN", ""
    norm = [strip_accents(t.lower()) for t in toks]
    idx: Optional[int] = None
    intent = "UNKNOWN"
    for i, nt in enumerate(norm):
        if not _is_word(toks[i]):
            continue
        if nt in CRUD_INTENTS:
            idx, intent = i, CRUD_INTENTS[nt]
            break
    if idx is None:
        for i, nt in enumerate(norm):
            if not _is_word(toks[i]) or len(nt) < 3:
                continue
            guess = _intent_from_prefix(nt)
            if guess:
                return guess, _strip_intent_token(toks, i)
        return intent, text
    return intent, _strip_intent_token(toks, idx)


def detect_intent(text: str) -> str:
    return detect_intent_and_strip(text)[0]
