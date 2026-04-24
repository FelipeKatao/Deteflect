import torch

class Modelpnlp:
    def __init__(self):
        self.Model = None
        self.ObjModel = None
        self.ListText = []
    def SetModel(self,model):
        self.Model = model
    def GetModel(self):
        self.objModel = torch.load(self.Model+".pt")
        return self.objModel
    def CreateModel(self):
        if self.Model:
            if self.ObjModel == None:
                self.ObjModel = {}
            torch.save(self.ObjModel,self.Model+".pt")
    def CreateToken(self,token,weight):
        if self.ObjModel == None:
            self.ObjModel = {}
        if self.Model:
            startToken = token[0]
            EndToken = token[:0]
            Count = len(token)
            id = 1 
            while(self.ObjModel.get(startToken+str(Count)+str(id)+EndToken)):
                id += 1
            self.ObjModel[startToken+str(Count)+str(id)+EndToken] = weight
            return startToken+str(Count)+str(id)+EndToken
    def SaveModel(self):
        if self.Model:
            torch.save(self.ObjModel,self.Model+".pt")
    def GetWord(self,position):
        for i in self.ListText:
            if len(i) <=3:
                self.ListText.remove(i)
        return self.ListText[int(position)]
    def ExtractTokens(self,text):
        self.ObjModelbjModel = {}
        start = True
        weight = 0
        self.ListText = str(text).split(" ")
        for i in self.ListText:

            if start:
               weight = 1 
               start = False    
            else:
                weight = 0.1
            if len(i) >=3:
                self.CreateToken(str(i).lower(),weight)
        return self.ObjModel
