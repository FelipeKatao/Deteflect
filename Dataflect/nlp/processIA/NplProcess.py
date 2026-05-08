# =========================================================
# app.py
# =========================================================

import os
import re
import json
import torch
import torch.nn as nn

from transformers import (
    AutoTokenizer,
    AutoModel
)

# =========================================================
# CONFIG
# =========================================================

MODEL_NAME = "neuralmind/bert-base-portuguese-cased"

LOCAL_MODEL_PATH = "./models/bertimbau"
CUSTOM_MODEL_PATH = "./models/custom_nlp.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# =========================================================
# INTENTS CONFIG
# =========================================================

INTENT_MAP = {
    0: "CREATE",
    1: "READ",
    2: "UPDATE",
    3: "DELETE"
}

LABEL_TO_ID = {
    "CREATE": 0,
    "READ": 1,
    "UPDATE": 2,
    "DELETE": 3
}

# =========================================================
# FALLBACK CONFIG
# =========================================================

INTENT_FALLBACK = {

    "CREATE": [
        "criar",
        "adicionar",
        "inserir",
        "cadastrar",
        "novo"
    ],

    "READ": [
        "buscar",
        "consultar",
        "listar",
        "mostrar"
    ],

    "UPDATE": [
        "editar",
        "alterar",
        "atualizar",
        "modificar"
    ],

    "DELETE": [
        "deletar",
        "apagar",
        "remover",
        "excluir"
    ]
}

# =========================================================
# MINI DATASET
# =========================================================

TRAINING_DATA = [

    # CREATE
    {
        "text": "criar cliente com nome lucas idade 21",
        "intent": "CREATE"
    },

    {
        "text": "adicionar funcionario marcos matricula 1234",
        "intent": "CREATE"
    },

    {
        "text": "inserir produto caderno cor verde",
        "intent": "CREATE"
    },

    # READ
    {
        "text": "buscar cliente lucas",
        "intent": "READ"
    },

    {
        "text": "consultar funcionario matricula 1234",
        "intent": "READ"
    },

    {
        "text": "listar produtos ativos",
        "intent": "READ"
    },

    # UPDATE
    {
        "text": "atualizar idade do cliente lucas",
        "intent": "UPDATE"
    },

    {
        "text": "editar setor do funcionario marcos",
        "intent": "UPDATE"
    },

    {
        "text": "alterar status do pedido 123",
        "intent": "UPDATE"
    },

    # DELETE
    {
        "text": "deletar cliente lucas",
        "intent": "DELETE"
    },

    {
        "text": "remover funcionario matricula 1234",
        "intent": "DELETE"
    },

    {
        "text": "apagar produto caderno",
        "intent": "DELETE"
    }
]

# =========================================================
# DOWNLOAD MODEL
# =========================================================

def download_model():

    if os.path.exists(LOCAL_MODEL_PATH):
        return

    print("Baixando BERTimbau...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModel.from_pretrained(
        MODEL_NAME
    )

    os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)

    tokenizer.save_pretrained(
        LOCAL_MODEL_PATH
    )

    model.save_pretrained(
        LOCAL_MODEL_PATH
    )

    print("Modelo salvo localmente.")

# =========================================================
# MODEL
# =========================================================

class IntentClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        self.bert = AutoModel.from_pretrained(
            LOCAL_MODEL_PATH
        )

        hidden_size = self.bert.config.hidden_size

        self.dropout = nn.Dropout(0.2)

        self.intent_head = nn.Linear(
            hidden_size,
            len(INTENT_MAP)
        )

    def forward(self, input_ids, attention_mask):

        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled = outputs.last_hidden_state[:, 0]

        pooled = self.dropout(pooled)

        return self.intent_head(pooled)

# =========================================================
# NLP PROCESSOR
# =========================================================

class NLPProcessor:

    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            LOCAL_MODEL_PATH
        )

        self.model = IntentClassifier().to(DEVICE)

        # carregar modelo treinado
        if os.path.exists(CUSTOM_MODEL_PATH):

            self.model.load_state_dict(
                torch.load(
                    CUSTOM_MODEL_PATH,
                    map_location=DEVICE
                )
            )

        self.model.eval()

        self.stopwords = {
            "com",
            "de",
            "e",
            "o",
            "a",
            "um",
            "uma",
            "novo",
            "nova"
        }

    # =====================================================
    # TRAIN
    # =====================================================

    def train(self):

        print("\nTreinando modelo...\n")

        self.model.train()

        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=2e-5
        )

        criterion = nn.CrossEntropyLoss()

        epochs = 6

        for epoch in range(epochs):

            total_loss = 0

            print(f"Epoch {epoch+1}/{epochs}")

            for item in TRAINING_DATA:

                text = item["text"]
                label = LABEL_TO_ID[item["intent"]]

                encoded = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=64
                )

                input_ids = encoded["input_ids"].to(DEVICE)
                attention_mask = encoded["attention_mask"].to(DEVICE)

                labels = torch.tensor(
                    [label]
                ).to(DEVICE)

                optimizer.zero_grad()

                outputs = self.model(
                    input_ids,
                    attention_mask
                )

                loss = criterion(outputs, labels)

                loss.backward()

                optimizer.step()

                total_loss += loss.item()

            print(
                f"Loss: {total_loss:.4f}\n"
            )

        torch.save(
            self.model.state_dict(),
            CUSTOM_MODEL_PATH
        )

        print("Modelo treinado salvo.")

    # =====================================================
    # FALLBACK
    # =====================================================

    def fallback_intent(self, text):

        text = text.lower()

        for intent, words in INTENT_FALLBACK.items():

            for word in words:

                if word in text:
                    return intent

        return None

    # =====================================================
    # BERT INTENT
    # =====================================================

    def predict_intent(self, text):

        # fallback primeiro
        fallback = self.fallback_intent(text)

        if fallback:
            return fallback

        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=64
        )

        input_ids = encoded["input_ids"].to(DEVICE)
        attention_mask = encoded["attention_mask"].to(DEVICE)

        with torch.no_grad():

            outputs = self.model(
                input_ids,
                attention_mask
            )

        pred = torch.argmax(
            outputs,
            dim=1
        ).item()

        return INTENT_MAP[pred]

    # =====================================================
    # ENTITY
    # =====================================================

    def extract_entity(self, text):

        words = text.lower().split()

        ignored = set()

        for verbs in INTENT_FALLBACK.values():
            ignored.update(verbs)

        ignored.update(self.stopwords)

        for word in words:

            if word not in ignored:
                return word

        return None

    # =====================================================
    # GENERIC DATA PARSER
    # =====================================================

    def extract_data(self, text):

        text = text.lower()

        data = {}

        # remove conectores
        clean_text = re.sub(
            r"\b(com|e)\b",
            " ",
            text
        )

        words = clean_text.split()

        entity = self.extract_entity(text)

        # remove verbo e entidade
        filtered = []

        for w in words:

            if w == entity:
                continue

            skip = False

            for verbs in INTENT_FALLBACK.values():

                if w in verbs:
                    skip = True
                    break

            if not skip:
                filtered.append(w)

        i = 0

        while i < len(filtered):

            key = filtered[i]

            if i + 1 >= len(filtered):
                break

            value_tokens = []

            j = i + 1

            while j < len(filtered):

                current = filtered[j]

                # nova chave detectada
                if (
                    j + 1 < len(filtered)
                    and (
                        filtered[j + 1].isdigit()
                        or filtered[j + 1].startswith("r$")
                    )
                ):
                    break

                if current in self.stopwords:
                    break

                value_tokens.append(current)

                j += 1

                # limite simples
                if len(value_tokens) >= 4:
                    break

            if value_tokens:

                data[key] = " ".join(value_tokens)

            i = j

        return data

    # =====================================================
    # PROCESS
    # =====================================================

    def process(self, text):

        return {

            "intent": self.predict_intent(text),

            "entity": self.extract_entity(text),

            "data": self.extract_data(text)
        }

# =========================================================
# APP
# =========================================================

class App:

    def __init__(self):

        download_model()

        self.processor = NLPProcessor()

    def run(self):

        print("\n=== NLP LOCAL SYSTEM ===\n")
        print("1 - Treinar")
        print("2 - Usar\n")

        option = input("Escolha: ")

        if option == "1":

            self.processor.train()

        elif option == "2":

            while True:

                text = input("\n>> ")

                if text.lower() == "sair":
                    break

                result = self.processor.process(text)

                print("\nRESULTADO\n")

                print(
                    "Intent:",
                    result["intent"]
                )

                print(
                    "Entity:",
                    result["entity"]
                )

                print("\nData:")

                for k, v in result["data"].items():

                    print(f"{k}: {v}")

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    App().run()