from .processor import process

def split_sentences(text):

    doc = process(text)

    sentences = []

    for sent in doc.sents:
        sentences.append(sent.text)

    return sentences


def extract_object(text):

    doc = process(text)

    for token in doc:

        if token.dep_ == "obj":

            return token.text

    return None


def extract_entities(text):

    doc = process(text)

    entities = []

    for ent in doc.ents:

        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities

def extract_subject(text):

    doc = process(text)

    for token in doc:

        if token.dep_ == "nsubj":

            return token.text

    return None