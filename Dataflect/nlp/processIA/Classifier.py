import os
import re
import json
import torch
import torch.nn as nn
from nlp.processIA.npl_app import INTENT_MAP,CUSTOM_MODEL_PATH,DEVICE,DEVICE,TRAINING_DATA,LABEL_TO_ID,INTENT_FALLBACK
from .Npl_process  import LOCAL_MODEL_PATH

from transformers import (
    AutoTokenizer,
    AutoModel
)

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