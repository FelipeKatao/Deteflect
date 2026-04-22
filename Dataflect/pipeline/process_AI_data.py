from typing import Any, Dict, List, Optional

from nlp import NLPFacade
from nlp.intent import detect_intent_and_strip
from nlp.sentiment import get_sentiment

_facade: Optional[NLPFacade] = None


def _get_facade() -> NLPFacade:
    global _facade
    if _facade is None:
        _facade = NLPFacade()
    return _facade


def _context_fill(
    text: str,
    facade: NLPFacade,
    entities: List[Dict[str, str]],
    keywords: List[str],
) -> Dict[str, Any]:
    hints = facade.palavras_fortes_contexto_objetos(text)
    labels = {"ENTITY", "DB_OBJECT", "MISC", "PER", "ORG"}
    from_entities = [e["text"] for e in entities if e.get("label") in labels]
    merged: List[str] = []
    seen = set()
    for w in hints + from_entities + keywords:
        k = w.lower()
        if k in seen:
            continue
        seen.add(k)
        merged.append(w)
    return {"hints": hints, "entity_targets": from_entities, "keywords": keywords, "merged": merged}


def analyze(text: str) -> Dict[str, Any]:
    facade = _get_facade()
    keywords = facade.palavras_chaves_da_sentenca(text, top_k=3)
    entities = facade.entidades_da_frase(text)
    return {
        "MajorKeywords": keywords,
        "Entities": entities,
        "Sentiment": get_sentiment(text),
        "intent": detect_intent_and_strip(text),
        "sentences": facade.decompositor_de_frases(text),
        "context": _context_fill(text, facade, entities, keywords),
    }
