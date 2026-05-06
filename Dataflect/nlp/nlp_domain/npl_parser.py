import re

class DataParser:

    def __init__(self):
        self.verbs = {
            "criar", "adicionar", "inserir",
            "deletar", "remover",
            "atualizar", "editar", "alterar",
            "buscar", "consultar"
        }

    def preprocess(self, text):
        text = text.lower()

        # remove ruído comum
        text = re.sub(r"\b(com|e)\b", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_object(self, text):
        words = text.split()

        for w in words:
            if w not in self.verbs:
                return w

        return None

    def extract_pairs(self, text):
        """
        Captura:
        nome Marcos idade 34 matricula 1234
        """
        pattern = r"(\w+)\s+([^0-9]+?|\d+[\d.,]*)\s*(?=\s\w+\s|$)"

        matches = re.findall(pattern, text)

        data = {}
        for key, value in matches:
            value = value.strip()

            # limpa excesso tipo "marcos com"
            value = re.sub(r"\b(com|e)\b.*", "", value).strip()

            data[key] = value

        return data

    def parse(self, text):
        text = self.preprocess(text)

        result = {
            "objeto": self.extract_object(text),
            "dados": {}
        }

        # remove comando inicial
        parts = text.split(result["objeto"], 1)

        if len(parts) > 1:
            data_part = parts[1]
        else:
            data_part = text

        result["dados"] = self.extract_pairs(data_part)

        return result