from flask  import Blueprint,request,make_response
from controller.MensagesController import MensagesController

Responses = Blueprint('Responses', __name__)
@Responses.route('/sendmensage/API/<text>', methods=['GET'])
def Send(text):
    Response = MensagesController().ReturnResponse(text)
    return ({"Response":Response[0]},Response[1])
