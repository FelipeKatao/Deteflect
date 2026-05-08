
from .NplProcess import download_model
from .Npl_process import NLPProcessor


class App:

    def __init__(self):
        self.processor = NLPProcessor()

    def Train(self):
        download_model()
        self.processor.train()

    def run(self,text):
                result = self.processor.process(text)
                return result
