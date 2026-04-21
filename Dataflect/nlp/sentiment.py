import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

MODEL_PATH = "./script/models/nlp"

nlp = spacy.load(MODEL_PATH)

nlp.add_pipe("spacytextblob")

def get_sentiment(text):

    doc = nlp(text)

    polarity = doc._.blob.polarity

    if polarity > 0:
        return "POSITIVO"

    if polarity < 0:
        return "NEGATIVO"

    return "NEUTRO"
