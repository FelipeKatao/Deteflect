import spacy

MODEL_PATH = "./script/models/nlp"

nlp = spacy.load(MODEL_PATH)

def process(text: str):
    return nlp(text)
