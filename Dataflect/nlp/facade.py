from typing import Dict, List, Tuple

from .torch_pipeline import TorchNLP


class NLPFacade:
    def __init__(self) -> None:
        self._nlp = TorchNLP()

    def sistema_de_sintaxe_correta(self, text: str) -> str:
        return self._nlp.sistema_de_sintaxe_correta(text)

    def descobrir_palavras_relevantes(self, text: str) -> List[str]:
        return self._nlp.descobrir_palavras_relevantes(text)

    def palavras_chaves_da_sentenca(self, text: str, top_k: int = 6) -> List[str]:
        return self._nlp.palavras_chaves_da_sentenca(text, top_k=top_k)

    def entidades_da_frase(self, text: str) -> List[Dict[str, str]]:
        return self._nlp.entidades_da_frase(text)

    def classificador_palavras_relevantes(self, text: str) -> Tuple[List[str], List[float]]:
        return self._nlp.classificador_palavras_relevantes(text)

    def decompositor_de_frases(self, text: str) -> List[str]:
        return self._nlp.decompositor_de_frases(text)

    def palavras_fortes_contexto_objetos(self, text: str, top_k: int = 8) -> List[str]:
        return self._nlp.palavras_fortes_contexto_objetos(text, top_k=top_k)

    def analisar(self, text: str) -> Dict[str, object]:
        return self._nlp.analisar(text)
