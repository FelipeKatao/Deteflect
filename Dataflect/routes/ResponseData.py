import json

from flask  import Blueprint
from controller.MensagesController import MensagesController

Responses = Blueprint('Responses', __name__)
msg_controller = MensagesController()

@Responses.route('/sendmensage/API/<text>', methods=['GET'])
def Send(text):
    Response = json.loads(msg_controller.analyze(text))
    if Response.get("Error") != None:
          return {"Response": Response["Error"]}
    if Response.get("Rule") != None:
          return {"Response": f" One of the rules was triggered \n: {Response['Rule']}"}
    intent_raw = Response.get("intent")
    intent_name = intent_raw[0] if isinstance(intent_raw, (list, tuple)) else intent_raw
    if intent_name == "UNKNOWN":
           return {"Response":"I couldn't understand what was sent, please check if there are no spelling, syntax, or context errors. And try again"}
    ctx = Response.get("context", {})
    return {"Response": f"""
       The user asked {text}. \n
       And object of sentence is {str(Response["MajorKeywords"])} , with entities {str(Response["Entities"])}.
       With aditional sentiment {str(Response["Sentiment"])}
       and aditional intent {intent_name}
       and context {str(ctx)}"""}


