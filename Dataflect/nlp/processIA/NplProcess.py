import os
import torch
import torch.nn as nn
from .Database import INTENT_MAP

from transformers import (
    AutoTokenizer,
    AutoModel
)


MODEL_NAME = "neuralmind/bert-base-portuguese-cased"

LOCAL_MODEL_PATH = "./models/bertimbau"
CUSTOM_MODEL_PATH = "./models/custom_nlp.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


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
