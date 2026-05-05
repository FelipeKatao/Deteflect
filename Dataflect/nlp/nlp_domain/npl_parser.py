import re

class DataParser:

    def __init__(self):
        self.stopwords = {
            "um", "uma", "novo", "nova", "com", "de", "da", "do", "para", "o", "a"
        }

        self.connectors = {"e", "and"}

        self.known_objects = {
            "usuario", "cliente", "tabela", "pedido","chamado","prioridade"
        }

    def parse(self, text):
        text = text.lower()
        words = text.split()

        result = {
            "objeto": None,
            "dados": {}
        }

        # 🔥 1. identificar objeto
        for w in words:
            if w in self.known_objects:
                result["objeto"] = w
                break

        # 🔥 2. limpar palavras irrelevantes
        filtered = [
            w for w in words
            if w not in self.stopwords and w not in self.connectors
        ]

        i = 0
        while i < len(filtered):

            word = filtered[i]

            # ignorar verbos de ação
            if word in ["criar", "inserir", "adicionar", "deletar", "remover", "buscar"]:
                i += 1
                continue

            # ignorar objeto
            if word == result["objeto"]:
                i += 1
                continue

            # 🔥 detectar chave composta (ex: "id processo")
            if i + 1 < len(filtered):
                next_word = filtered[i + 1]

                # caso especial: "id processo"
                if word == "id":
                    key = f"{word}_{next_word}"
                    i += 2
                else:
                    key = word
                    i += 1
            else:
                break

            # 🔥 capturar valor (1 ou 2 tokens)
            value_parts = []

            while i < len(filtered):
                current = filtered[i]

                # parar se próximo parece nova chave
                if current in self.known_objects:
                    break

                # parar se próximo parece outra chave comum
                if current in ["nome", "idade", "profissão", "id"]:
                    break

                value_parts.append(current)
                i += 1

            if value_parts:
                value = " ".join(value_parts)
                result["dados"][key] = value

        return result