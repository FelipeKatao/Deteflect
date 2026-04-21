from .torch_tokenizer import strip_accents, tokenize


_POS = {
    "bom", "boa", "otimo", "ótimo", "excelente", "legal", "feliz", "gostei",
    "perfeito", "sucesso", "maravilhoso", "top", "obrigado", "obrigada",
    "amei", "adoro", "incrivel", "incrível", "show",
}
_NEG = {
    "ruim", "péssimo", "pessimo", "horrivel", "horrível", "triste", "odeio",
    "erro", "falha", "problema", "lento", "quebrado", "bug",
    "pior", "chato", "raiva", "horrendo",
}
_NEGATORS = {"nao", "não", "nunca", "jamais", "sem"}


def get_sentiment(text: str) -> str:
    toks = [strip_accents(t.lower()) for t in tokenize(text) if any(ch.isalpha() for ch in t)]
    score = 0
    for i, t in enumerate(toks):
        prev1 = toks[i - 1] if i - 1 >= 0 else ""
        prev2 = toks[i - 2] if i - 2 >= 0 else ""
        neg = (prev1 in _NEGATORS) or (prev2 in _NEGATORS)
        if t in _POS:
            score += -1 if neg else 1
        elif t in _NEG:
            score += 1 if neg else -1
    if score > 0:
        return "POSITIVE"
    if score < 0:
        return "NEGATIVE"
    return "NEUTRAL"

