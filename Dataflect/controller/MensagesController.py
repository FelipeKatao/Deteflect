import json

from pipeline import process_AI_data
from pipeline.process_AI_data import GetContext
from project import Rule_data
from util.NormalizeText import NormalizeText

class MensagesController:
    def __init__(self) -> None:
        self.MaxTry = 4
        self.tryAnalyze = 0

    def analyze(self, text: str) -> str:
        normalized = NormalizeText(text).normalize()
        memo = Rule_data.GetMemory(normalized)
        if memo is not None:
            return json.dumps({"Rule": memo["action"]()})
        data = process_AI_data.analyze(normalized)
        intent_field = data["intent"]
        intent_name = intent_field[0] if isinstance(intent_field, (list, tuple)) else str(intent_field)
        keywords = data.get("MajorKeywords") or []
        sentiment = data.get("Sentiment")
        if keywords:
            self.tryAnalyze = 0
        detected = Rule_data.ResponseRule(normalized, intent_name, keywords if keywords else None,sentiment)
        Build_dataContext = self.BuildResponseData([data,detected,GetContext(text),{"Sent":sentiment},{"Keys":keywords}])
        if not keywords:
            self.tryAnalyze += 1
            if self.tryAnalyze <= self.MaxTry:
                return json.dumps({"Error": "I do know this, but you need to try again."})
        if detected is not None:
            return json.dumps({"Rule": detected["action"]()})
        return json.dumps(Build_dataContext)

    def BuildResponseData(self,Data):
       ResponseField = {"Sentiment":[],"Objeto":[],"Itens":[],"Entidade":[]}
       for i in Data:
            print(i)
            if i:
                if  i.get("MajorKeywords"):
                    ResponseField["Itens"].append(i["MajorKeywords"])
                if i.get("Ação_contexto"):
                        ResponseField["Entidade"].append(i["Ação_contexto"])
                if i.get("Sentiment"):
                        ResponseField["Sentiment"].append(i["Sentiment"])
                if i.get("entidades"):
                        ResponseField["Entidade"].append(i["entidades"])
                if i.get("context"):
                        ResponseField["Objeto"].append(i["context"]["hints"])
       print(ResponseField)
       return ResponseField