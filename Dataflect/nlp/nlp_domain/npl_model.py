import torch
import torch.nn as nn
from transformers import AutoModel


class IntentModel(nn.Module):
    def __init__(self, model_name, num_intents, num_sentiments):
        super().__init__()

        self.bert = AutoModel.from_pretrained(model_name,ignore_mismatched_sizes=True)
        hidden = self.bert.config.hidden_size

        self.intent_head = nn.Linear(hidden, num_intents)
        self.sentiment_head = nn.Linear(hidden, num_sentiments)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        cls = outputs.last_hidden_state[:, 0]

        intent = self.intent_head(cls)
        sentiment = self.sentiment_head(cls)

        return intent, sentiment