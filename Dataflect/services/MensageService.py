from domain.Menssage_domain import MessagesDomain
from nlp.nlp_domain.npl_run import App
from enumData.ResposeData import ResposeData
class MensageService():
    def __init__(self) -> None:
        self.domain = MessagesDomain()
        self.appNpl = App()

    def ReturnMensage(self,text):
        if len(text) >=8:
            text = self.appNpl.run("2",text)
            return  (self.domain.ResponseDataDomain(text),200)
        else:
            return ResposeData.Error.value
