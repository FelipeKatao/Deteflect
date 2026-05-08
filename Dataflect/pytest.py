from nlp.processIA.npl_app import App

v = App()
while(True):
    txt = input("Digite algo: ")
    print(v.run(txt))