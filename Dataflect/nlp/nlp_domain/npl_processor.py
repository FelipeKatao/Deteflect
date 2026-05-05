import torch
import torch.nn as nn
import torch.optim as optim
import os

from transformers import AutoTokenizer
from npl_dataset_intent import training_data
from npl_model import IntentModel
from npl_parser import DataParser

MODEL_PATH = "model.pt"
TOKENIZER_PATH = "tokenizer/"


class NLPProcessor:

    def __init__(self):
        self.model_name = "neuralmind/bert-base-portuguese-cased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.intents = ["CREATE", "READ", "UPDATE", "DELETE"]
        self.sentiments = ["NEGATIVO", "NEUTRO", "POSITIVO"]

        self.model = IntentModel(
            self.model_name,
            len(self.intents),
            len(self.sentiments)
        )

        self.parser = DataParser()

    def save(self):
        torch.save(self.model.state_dict(), MODEL_PATH)
        self.tokenizer.save_pretrained(TOKENIZER_PATH)

    def load(self):
        self.model.load_state_dict(torch.load(MODEL_PATH))
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

    def train(self):
        optimizer = optim.Adam(self.model.parameters(), lr=2e-5)
        loss_fn = nn.CrossEntropyLoss()

        self.model.train()

        for epoch in range(5):
            for item in training_data:

                encoding = self.tokenizer(
                    item["text"],
                    return_tensors="pt",
                    padding="max_length",
                    truncation=True,
                    max_length=32
                )

                input_ids = encoding["input_ids"]
                attention_mask = encoding["attention_mask"]

                intent_label = torch.tensor([self.intents.index(item["intent"])])
                sentiment_label = torch.tensor([self.sentiments.index(item["sentiment"])])

                intent_pred, sentiment_pred = self.model(input_ids, attention_mask)

                loss_intent = loss_fn(intent_pred, intent_label)
                loss_sent = loss_fn(sentiment_pred, sentiment_label)

                loss = loss_intent + loss_sent

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        self.save()

    def predict(self, text):
        encoding = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=32
        )

        intent_pred, sentiment_pred = self.model(
            encoding["input_ids"],
            encoding["attention_mask"]
        )

        intent = self.intents[intent_pred.argmax().item()]
        sentiment = self.sentiments[sentiment_pred.argmax().item()]

        parsed = self.parser.parse(text)

        return {
            "acao": intent,
            "sentimento": sentiment,
            "objeto": parsed["objeto"],
            "dados": parsed["dados"]
        }