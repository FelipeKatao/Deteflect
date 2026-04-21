from .processor import process

INTENTS = {
    "criar": "CREATE",
    "gerar": "GENERATE",
    "deletar": "DELETE",
    "buscar": "READ",
    "atualizar": "UPDATE"
}

def detect_intent(text):

    doc = process(text)

    for token in doc:

        palavra = token.lemma_.lower()

        if palavra in INTENTS:
            return INTENTS[palavra]

    return "UNKNOWN"
