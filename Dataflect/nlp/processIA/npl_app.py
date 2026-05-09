
from .NplProcess import download_model
from .Npl_process import NLPProcessor


class App:

    def __init__(self):
        self.processor = NLPProcessor()

    def Train(self):
        download_model()
        self.processor.train()

    def CreateTextArray(self,text):
          v =  ""
          for i in text:
                v+=i+" "
          return v

    def run(self, text):
        text = " ".join([w for w in str(text).split() if len(w) >= 3])

        result = self.processor.process(text)
        data = result["data"]
        list_words = text.split()
        int_x = 2

        while data and int_x < len(list_words):
            list_words.pop(int_x)
            new_data = self.processor.process(self.CreateTextArray(list_words))["data"]
            data.update(new_data)

        result["data"] = {k: v for k, v in data.items() if len(v.split()) < 3}
        return result
