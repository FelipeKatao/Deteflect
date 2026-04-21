from nlp import NLPFacade
from nlp.intent import detect_intent_and_strip

def analyze(text):
    npl_torch =  NLPFacade()

    data_return = {
        "MajorKeywords": npl_torch.palavras_chaves_da_sentenca(text, top_k=3),
        "Entities": npl_torch.entidades_da_frase(text)[0]["text"],
        "Sentiment": "Ok",
        "intent": detect_intent_and_strip(text),
        "sentences": npl_torch.decompositor_de_frases(text),
    }

    return data_return