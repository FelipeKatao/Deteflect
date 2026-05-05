from flask  import Flask, render_template, request, session
from routes.ResponseData import Responses
from routes.GetConfig import GetConfig
from flask_cors import CORS # type: ignore
import os
from config_generator import ensure_config_yaml

app = Flask(__name__)
CORS(app)

# Carregar configuração e definir chave secreta
config_path = os.path.join(os.path.dirname(__file__), "Deteflect.yaml")
config = ensure_config_yaml(config_path)
app.secret_key = config.get("SecretKey", "DataFlect_Secure_Key_2024")

@app.route('/', methods=['GET'])
def index():
    return {"Response": "Hello World"}
# App Routes 
app.register_blueprint(Responses)
app.register_blueprint(GetConfig)

if __name__ == '__main__':
    app.run(debug=True)
