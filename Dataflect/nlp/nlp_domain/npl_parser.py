import re

class DataParser:

    def __init__(self):
        self.stopwords = {"um", "uma", "novo", "nova", "com", "de", "para", "o", "a"}
        self.connectors = {"e"}
        self.verbs = {
            "criar", "adicionar", "inserir", "buscar",
            "deletar", "remover", "atualizar", "consultar"
        }

        # possíveis campos conhecidos (ajuda a parar parsing)
        self.possible_keys = {
            "nome", "idade", "prioridade", "setor",
            "tipo", "profissão", "cargo"
        }

    def parse(self, text):
        words = text.lower().split()

        result = {
            "objeto": None,
            "dados": {}
        }

        # 🔥 1. detectar objeto
        for w in words:
            if w not in self.stopwords and w not in self.verbs:
                result["objeto"] = w
                break

        i = 0
        while i < len(words):

            word = words[i]

            # ignorar irrelevantes
            if word in self.stopwords or word in self.verbs or word in self.connectors:
                i += 1
                continue

            # 🔥 detectar chave
            key = None
            value_tokens = []

            # padrão: chave de valor
            if i + 1 < len(words) and words[i + 1] == "de":
                key = word
                i += 2  # pula "chave de"

            else:
                # padrão: chave valor
                if word in self.possible_keys:
                    key = word
                    i += 1
                else:
                    i += 1
                    continue

            # 🔥 coletar valor composto
            while i < len(words):
                current = words[i]

                # parar se encontrar nova chave ou conector
                if (
                    current in self.connectors
                    or current in self.verbs
                    or current in self.possible_keys
                ):
                    break

                value_tokens.append(current)
                i += 1

            # salvar valor
            if key and value_tokens:
                result["dados"][key] = " ".join(value_tokens)

        return result