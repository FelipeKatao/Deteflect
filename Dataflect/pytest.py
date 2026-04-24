from nlp.pnlp.model import Modelpnlp
from nlp.pnlp.ProcessModel import ProcessModel

v = Modelpnlp()
z = ProcessModel()
v.SetModel("./nlp/model/test")
teste = "crie uma tabela com nome de Alunos"
# v.CreateModel()
# v.ExtractTokens(teste)
# v.SaveModel()
terms =[]
for x in z.ReturnRelevanceWords(v.ExtractTokens(teste),v.GetModel()):
    terms.append(v.GetWord(x))
print(terms)

