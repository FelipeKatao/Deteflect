import os
from npl_processor import NLPProcessor, MODEL_PATH


class App:
    def __init__(self):
        self.processor = NLPProcessor()

    def run(self):
        print("=== NLP SYSTEM V2 ===")
        print("1 - Treinar")
        print("2 - Usar")

        mode = input("Escolha: ")

        if mode == "1":
            print("Treinando...")
            self.processor.train()
            print("OK")

        elif mode == "2":
            if not os.path.exists(MODEL_PATH):
                print("Treine primeiro")
                return

            self.processor.load()

            while True:
                text = input(">> ")

                if text == "sair":
                    break

                print(self.processor.predict(text))


if __name__ == "__main__":
    App().run()