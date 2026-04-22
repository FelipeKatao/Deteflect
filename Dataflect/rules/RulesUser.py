import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Set, Tuple

STOPWORDS = {
    "um", "uma", "o", "a", "de", "do", "da", "quero", "preciso", "gostaria",
}


class RulesSintaxe:
    def __init__(self) -> None:
        self.rules: Dict[Tuple[str, ...], Dict[str, Any]] = {}
        self.Memory: Dict[str, Dict[str, Any]] = {}
        self.similarity_threshold = 0.6
        self.assimilation_ratio = 0.82
        self.assimilation_coverage = 0.65

    def __str__(self) -> str:
        return "RulesSintaxe"

    def normalize(self, text: object) -> Set[str]:
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", "", text)
        tokens = [t for t in text.split() if t not in STOPWORDS]
        return set(tokens)

    def _message_tokens(self, message: str, keywords: Optional[List[str]]) -> Set[str]:
        merged = self.normalize(message)
        if keywords:
            merged = merged | self.normalize(" ".join(str(w) for w in keywords))
        return merged

    def similarity(self, tokens1: Set[str], tokens2: Set[str]) -> float:
        union = tokens1.union(tokens2)
        if not union:
            return 0.0
        return len(tokens1.intersection(tokens2)) / len(union)

    def _fuzzy_rule_word_in_message(self, rule_word: str, msg_tokens: Set[str]) -> bool:
        for mt in msg_tokens:
            if rule_word == mt:
                return True
            if len(rule_word) >= 4 and len(mt) >= 4:
                if SequenceMatcher(None, rule_word, mt).ratio() >= self.assimilation_ratio:
                    return True
        return False

    def _assimilation_coverage(self, rule_words: Tuple[str, ...], msg_tokens: Set[str]) -> float:
        if not rule_words:
            return 0.0
        hit = sum(1 for rw in rule_words if self._fuzzy_rule_word_in_message(rw, msg_tokens))
        return hit / len(rule_words)

    def MemoryData(self, Memory: str, Rule: Any) -> None:
        self.Memory[Memory] = {"tokens": self.normalize(Memory), "rule": Rule}

    def GetMemory(self, Memory: str) -> Optional[Dict[str, Any]]:
        new_tokens = self.normalize(Memory)
        best_match: Optional[Dict[str, Any]] = None
        best_score = 0.0
        for _old_text, data in self.Memory.items():
            old_tokens = data["tokens"]
            score = self.similarity(new_tokens, old_tokens)
            if score > best_score:
                best_score = score
                best_match = data
        if best_score >= self.similarity_threshold and best_match:
            return {
                "status": "memory_match",
                "similarity": best_score,
                "action": best_match["rule"],
            }
        return None

    def NewRule(self, rule: Tuple[str, ...], intent: str, action: Any) -> None:
        palavras = tuple(p.strip().lower() for p in rule)
        self.rules[palavras] = {"intent": intent, "action": action}

    def ResponseRule(
        self,
        message_text: str,
        intent: str,
        keywords: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        msg_tokens = self._message_tokens(message_text, keywords)
        for palavras_regra, dados in self.rules.items():
            rule_set = set(palavras_regra)
            if rule_set.issubset(msg_tokens):
                self.MemoryData(str(message_text), dados["action"])
                return {"intent": dados["intent"], "action": dados["action"], "match": "exact"}
        best: Optional[Dict[str, Any]] = None
        best_cov = 0.0
        best_intent_bonus = False
        for palavras_regra, dados in self.rules.items():
            cov = self._assimilation_coverage(palavras_regra, msg_tokens)
            if cov < self.assimilation_coverage:
                continue
            intent_ok = dados["intent"] == intent
            better = cov > best_cov or (cov == best_cov and intent_ok and not best_intent_bonus)
            if better:
                best_cov = cov
                best_intent_bonus = intent_ok
                best = dados
        if best:
            self.MemoryData(str(message_text), best["action"])
            return {
                "intent": best["intent"],
                "action": best["action"],
                "match": "assimilation",
                "coverage": best_cov,
            }
        memory_result = self.GetMemory(message_text)
        if memory_result:
            return {
                "intent": intent,
                "action": memory_result["action"],
                "source": "memory",
                "similarity": memory_result["similarity"],
            }
        return None
