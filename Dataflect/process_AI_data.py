from nlp.intent import detect_intent
from nlp.sentiment import get_sentiment
from nlp.extractor import (
    split_sentences,
    extract_object,
    extract_entities
)

def analyze(text):

    return {
        "sentences": split_sentences(text),
        "intent": detect_intent(text),
        "sentiment": get_sentiment(text),
        "object": extract_object(text),
        "entities": extract_entities(text)
    }

if __name__ == "__main__":

    text = (
        "Criar cliente João. "
        "Estou feliz com o sistema."
    )

    result = analyze(text)

    print(result)
