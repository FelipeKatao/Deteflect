from .pnlp.model import Modelpnlp
from .pnlp.ProcessModel import ProcessModel

class pnlp():
    def __init__(self):
        pass
    def Relevance(self,texto):
        v = Modelpnlp()
        z = ProcessModel()
        v.SetModel("./nlp/model/test")
        v.GetModel()
        Relevance_obj = z.ReturnRelevanceWords(v.ReturnVectorToken(texto),v.GetModel())
        Relevance_props = texto.split(" ")
        Relevance_props = [
            i for i in Relevance_props
            if i not in Relevance_obj
        ]
        return {"Context":Relevance_obj,"Relevance":Relevance_props}

    def ReturnContext(self,texto):
        v = Modelpnlp()
        v.SetModel("./nlp/model/test")
        v.GetModel()
        Return_Context = {
        "Ação_contexto": None,
        "Objetos": None,
        "entidades": [],
        "Complemento": None,
        "Complemento_valor": None
        }
        tokens = v.ContextDataObject(texto)
        prev_peso = None
        for posicao, (palavra, peso) in enumerate(tokens):
            if len(palavra) < 4:
                continue
            if posicao == 0:
                Return_Context["Ação_contexto"] = palavra
                prev_peso = peso
                continue
            if len(palavra) > 4:
                delta = peso - prev_peso
            if posicao == 1:
                Return_Context["Objetos"] = palavra
            elif delta <= 0.15:
                Return_Context["entidades"].append(palavra)
            elif delta <= 0.3:
                Return_Context["Complemento"] = palavra
            else:
                Return_Context["Complemento_valor"] = palavra
            if len(palavra) > 4:
                prev_peso = peso
        return Return_Context