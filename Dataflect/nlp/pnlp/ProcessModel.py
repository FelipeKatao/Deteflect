

class ProcessModel:
    def __init__(self):
        pass
    def ProcessModel(self,Model,TokenText):
        position = 1
        BiasToken = []
        for i in TokenText:
            Divide = len(TokenText) / position
            Minus = Divide - 1
            position += 1
            if Model.get(i):
                Minus+=0.5
            BiasToken.append(Minus)
        return BiasToken
    
    def Qualification(self,BiasToken):
        BiasToken.pop(0)
        avg= len(BiasToken)/2
        q = []
        for i in BiasToken:
            if i <= 1.1 and i > 0:
                q.append(i)
            else:
                q.append("_")
        return q
    
    def ReturnRelevanceWords(self,text,model):
      pos = []
      List_ = []
      x =0
      for i in self.Qualification(self.ProcessModel(model,text)):
          if i != "_":
              pos.append(x) 
          x+=1
      return pos