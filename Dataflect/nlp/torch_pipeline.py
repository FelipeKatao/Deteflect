from typing import Dict, List, Optional, Tuple
import re

import torch

from .torch_tokenizer import is_email, is_url, normalize_text, split_sentences_simple, strip_accents, tokenize
from .model.heads import SyntaxCorrectnessHead, TokenRelevanceHead


_STOPWORDS_PT = {
    "a", "o", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "por", "para", "com", "sem", "sobre", "entre", "até", "e", "ou", "mas",
    "que", "se", "como", "quando", "onde", "porque", "porquê",
    "eu", "tu", "ele", "ela", "nós", "vos", "vós", "eles", "elas",
    "me", "te", "se", "nos", "vos", "lhe", "lhes",
    "este", "esta", "isto", "esse", "essa", "isso", "aquele", "aquela", "aquilo",
    "um", "uma", "ser", "estar", "ter", "haver",
}

_VERB_HINTS = {
    "criar", "gerar", "deletar", "remover", "buscar", "procurar", "atualizar",
    "inserir", "listar", "mostrar", "fazer", "executar", "rodar", "validar",
}

_ACTION_PREFIXES = (
    "cri",      
    "ger",      
    "dele",     
    "remo",     
    "busc",     
    "proc",     
    "atua",     
    "inse",     
    "list",     
    "most",     
    "faz",      
    "exec",     
    "rod",      
    "vald",     
)

_CONTEXT_ATTR_HINTS = (
    "pintad", "colorid", "cor", "cor:", "cor=", "cor-", "cor_", "corir",
)

_PREPS = {
    "de", "do", "da", "dos", "das",
    "com", "sem",
    "em", "no", "na", "nos", "nas",
    "para", "por", "sobre", "entre", "até",
}


STOPWORDS = {
    "quero",
    "preciso",
    "gostaria",
    "criar",
    "remover",
    "buscar",
    "tabela",
    "cliente"
}


ORG_HINTS = {
    "empresa",
    "escola",
    "universidade",
    "banco",
    "loja",
    "hospital"
}

_RE_HASHTAG = re.compile(r"#\w+")
_RE_MENTION = re.compile(r"@\w+")
_RE_NUMBER = re.compile(r"^\d+$")
_RE_MONEY = re.compile(r"^(R\$|\$|€)\s?\d+([.,]\d+)?$")
_RE_DATE = re.compile(r"\d{2}/\d{2}/\d{4}")
_RE_PHONE = re.compile(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}")


def _is_word(tok: str) -> bool:
    return any(ch.isalpha() for ch in tok)


def _token_features(tokens: List[str]) -> torch.Tensor:
    feats: List[List[float]] = []
    for i, t in enumerate(tokens):
        t_stripped = t.strip()
        lower = t_stripped.lower()
        length_norm = min(len(t_stripped), 20) / 20.0
        is_alpha = 1.0 if t_stripped.isalpha() else 0.0
        is_title = 1.0 if (t_stripped[:1].isupper() and t_stripped[1:].islower()) else 0.0
        is_upper = 1.0 if t_stripped.isupper() and _is_word(t_stripped) else 0.0
        is_stop = 1.0 if strip_accents(lower) in _STOPWORDS_PT else 0.0
        pos_norm = 0.0 if len(tokens) <= 1 else float(i) / float(len(tokens) - 1)
        feats.append([length_norm, is_alpha, is_title, is_upper, is_stop, pos_norm])
    return torch.tensor(feats, dtype=torch.float32)


def _syntax_features(text: str, tokens: List[str]) -> torch.Tensor:
    if not text:
        return torch.zeros(5, dtype=torch.float32)
    token_count = min(len(tokens), 40) / 40.0
    norm = strip_accents(text.lower())
    verb_signal = 1.0 if any(v in norm.split() for v in _VERB_HINTS) else 0.0
    has_end_punct = 1.0 if text.rstrip().endswith((".", "!", "?")) else 0.0
    has_alpha = 1.0 if any(ch.isalpha() for ch in text) else 0.0
    balanced_quotes = 1.0 if (text.count('"') % 2 == 0 and text.count("'") % 2 == 0) else 0.0
    return torch.tensor([token_count, verb_signal, has_end_punct, has_alpha, balanced_quotes], dtype=torch.float32)


class TorchNLP:
    """
    Classe final para uso no projeto: passe apenas `text` e receba tudo.
    """

    def __init__(self, device: Optional[str] = None):
        self.device = torch.device(device) if device else torch.device("cpu")
        self.syntax_head = SyntaxCorrectnessHead().to(self.device).eval()
        self.relevance_head = TokenRelevanceHead().to(self.device).eval()

    def sistema_de_sintaxe_correta(self, text: str) -> str:
        text = normalize_text(text)
        toks = tokenize(text)
        feats = _syntax_features(text, toks).to(self.device)
        with torch.no_grad():
            logits = self.syntax_head(feats)
            pred = int(torch.argmax(logits).item())
        return "sistema de sintaxe correta" if pred == 1 else "sistema de sintaxe incorreta"

    def descobrir_palavras_relevantes(self, text: str) -> List[str]:
        tokens, scores = self.classificador_palavras_relevantes(text)
        pairs = [(t, s) for t, s in zip(tokens, scores) if _is_word(t)]
        pairs.sort(key=lambda x: x[1], reverse=True)
        out: List[str] = []
        seen = set()
        for t, s in pairs:
            key = strip_accents(t.lower())
            if key in seen or key in _STOPWORDS_PT:
                continue
            if s < 0.5:
                continue
            out.append(t)
            seen.add(key)
        return out

    def palavras_chaves_da_sentenca(self, text: str, top_k: int = 6) -> List[str]:
        rel = self.descobrir_palavras_relevantes(text)
        return rel[: max(0, int(top_k))]

    def entidades_da_frase(self, text: str) -> List[Dict[str, str]]:

        text = normalize_text(text)

        tokens = tokenize(text)

        entities: List[Dict[str, str]] = []

        def push_entity(txt: str, label: str):

            txt = txt.strip()

            if not txt:
                return

            entities.append({
                "text": txt,
                "label": label
            })

        # -----------------------------
        # 1) Regex-based entities
        # -----------------------------

        for t in tokens:

            t_clean = t.replace(" ", "")

            if is_url(t):

                push_entity(t, "URL")

            elif is_email(t):

                push_entity(t, "EMAIL")

            elif _RE_PHONE.match(t):

                push_entity(t, "PHONE")

            elif _RE_HASHTAG.match(t):

                push_entity(t, "HASHTAG")

            elif _RE_MENTION.match(t):

                push_entity(t, "MENTION")

            elif _RE_MONEY.match(t_clean):

                push_entity(t, "MONEY")

            elif _RE_DATE.match(t):

                push_entity(t, "DATE")

            elif _RE_NUMBER.match(t):

                push_entity(t, "NUMBER")

        # -----------------------------
        # 2) Detectar nomes compostos
        # -----------------------------

        current: List[str] = []

        for i, t in enumerate(tokens + ["<END>"]):

            is_title = (
                t[:1].isupper()
                and t[1:].islower()
                and _is_word(t)
                and t.lower() not in STOPWORDS
            )

            if is_title:

                current.append(t)

                continue

            if current:

                joined = " ".join(current)

                label = "PER"

                if len(current) == 1:

                    label = "MISC"

                push_entity(joined, label)

                current = []

        # -----------------------------
        # 3) Detectar organizações
        # -----------------------------

        for i in range(len(tokens) - 1):

            word = tokens[i].lower()

            if word in ORG_HINTS:

                name = []

                j = i + 1

                while j < len(tokens):

                    t = tokens[j]

                    if not t[:1].isupper():

                        break

                    name.append(t)

                    j += 1

                if name:

                    push_entity(
                        word + " " + " ".join(name),
                        "ORG"
                    )

        # -----------------------------
        # 4) Detectar entidades de domínio
        # -----------------------------

        DOMAIN_OBJECTS = {

            "cliente": "ENTITY",

            "pedido": "ENTITY",

            "produto": "ENTITY",

            "tabela": "DB_OBJECT",

            "usuario": "ENTITY",

            "aluno": "ENTITY"

        }

        for t in tokens:

            if t.lower() in DOMAIN_OBJECTS:

                push_entity(
                    t,
                    DOMAIN_OBJECTS[t.lower()]
                )

        # -----------------------------
        # 5) Deduplicação otimizada
        # -----------------------------

        uniq: List[Dict[str, str]] = []

        seen = set()

        for e in entities:

            key = (
                e["text"].lower(),
                e["label"]
            )

            if key in seen:

                continue

            seen.add(key)

            uniq.append(e)

        return uniq

    def classificador_palavras_relevantes(self, text: str) -> Tuple[List[str], List[float]]:
        text = normalize_text(text)
        tokens = tokenize(text)
        if not tokens:
            return [], []
        feats = _token_features(tokens).to(self.device)
        with torch.no_grad():
            logits = self.relevance_head(feats)
            probs = torch.sigmoid(logits).cpu().tolist()
        return tokens, [float(p) for p in probs]

    def decompositor_de_frases(self, text: str) -> List[str]:
        return split_sentences_simple(text)

    def palavras_fortes_contexto_objetos(self, text: str, top_k: int = 8) -> List[str]:

        text = normalize_text(text)
        tokens, scores = self.classificador_palavras_relevantes(text)
        if not tokens:
            return []

        norm_tokens = [strip_accents(t.lower()) for t in tokens]


        action_idx = None
        for i, nt in enumerate(norm_tokens):
            if not nt or not _is_word(tokens[i]):
                continue
            if nt in _VERB_HINTS or any(nt.startswith(p) for p in _ACTION_PREFIXES):
                action_idx = i
                break

        candidates: List[Tuple[str, float, int]] = []
        for i, (t, s, nt) in enumerate(zip(tokens, scores, norm_tokens)):
            if not _is_word(t):
                continue
            if nt in _STOPWORDS_PT:
                continue
            # Avoid returning action verbs as keywords
            if nt in _VERB_HINTS or any(nt.startswith(p) for p in _ACTION_PREFIXES):
                continue
            candidates.append((t, float(s), i))


        obj = None
        if action_idx is not None:

            for j in range(action_idx + 1, len(tokens)):
                t = tokens[j]
                nt = norm_tokens[j]
                if not _is_word(t):
                    continue
                if nt in _STOPWORDS_PT:
                    continue
                if nt in _VERB_HINTS or any(nt.startswith(p) for p in _ACTION_PREFIXES):
                    continue
                obj = t
                break

            if obj is None:
                for t, s, i in candidates:
                    if i <= action_idx:
                        continue
                    if s < 0.35:
                        continue
                    obj = t
                    break

        if obj is None and candidates:
            best = max(candidates, key=lambda x: x[1])
            if best[1] >= 0.45:
                obj = best[0]

       
        attrs: List[str] = []
        for i in range(len(norm_tokens)):
            nt = norm_tokens[i]

            tok = tokens[i]
            if tok.isupper() and _is_word(tok) and 2 <= len(tok) <= 6:
                if nt not in _STOPWORDS_PT:
                    attrs.append(tok)

            if i + 2 < len(norm_tokens):
                if any(nt.startswith(h) for h in ("pintad", "colorid")) and norm_tokens[i + 1] in {"de", "do", "da", "dos", "das"}:
                    nxt = tokens[i + 2]
                    nxt_norm = norm_tokens[i + 2]
                    if _is_word(nxt) and nxt_norm not in _STOPWORDS_PT:
                        attrs.append(nxt)

            # "cor de X" / "cor: X"
            if i + 2 < len(norm_tokens) and nt.startswith("cor") and norm_tokens[i + 1] in {"de", "do", "da", "dos", "das"}:
                nxt = tokens[i + 2]
                nxt_norm = norm_tokens[i + 2]
                if _is_word(nxt) and nxt_norm not in _STOPWORDS_PT:
                    attrs.append(nxt)

            # Generic preposition capture: "de X", "com X", "em X"...
            if i + 1 < len(norm_tokens) and nt in _PREPS:
                nxt = tokens[i + 1]
                nxt_norm = norm_tokens[i + 1]
                if _is_word(nxt) and nxt_norm not in _STOPWORDS_PT:
                    attrs.append(nxt)
                # If "com capa azul" => capture azul too (next-next word)
                if i + 2 < len(norm_tokens):
                    nxt2 = tokens[i + 2]
                    nxt2_norm = norm_tokens[i + 2]
                    if _is_word(nxt2) and nxt2_norm not in _STOPWORDS_PT:
                        # Only add if it looks like an adjective/modifier (lowercase) and not too far.
                        if nxt2[:1].islower():
                            attrs.append(nxt2)

        # 3) Se ainda não achou atributos, pega as melhores relevantes (dinâmico)
        candidates_sorted = sorted(candidates, key=lambda x: x[1], reverse=True)
        fallback: List[str] = []
        for t, s, _i in candidates_sorted:
            if s < 0.55:
                continue
            fallback.append(t)
            if len(fallback) >= max(0, int(top_k)):
                break

        out: List[str] = []
        seen = set()

        def push(w: str) -> None:
            k = strip_accents(w.lower())
            if k in seen or k in _STOPWORDS_PT:
                return
            seen.add(k)
            out.append(w)

        if obj:
            push(obj)
        for a in attrs:
            push(a)
        for w in fallback:
            if len(out) >= max(0, int(top_k)):
                break
            push(w)

        return out

    # ---- Conveniência: tudo de uma vez ----
    def analisar(self, text: str) -> Dict[str, object]:
        return {
            "sintaxe": self.sistema_de_sintaxe_correta(text),
            "relevantes": self.descobrir_palavras_relevantes(text),
            "keywords": self.palavras_chaves_da_sentenca(text),
            "entidades": self.entidades_da_frase(text),
            "frases": self.decompositor_de_frases(text),
            "fortes_contexto_objetos": self.palavras_fortes_contexto_objetos(text),
        }

