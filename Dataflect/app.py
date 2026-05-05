from flask  import Flask, render_template, request, session
from routes.ResponseData import Responses

from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return {"Response": "Hello World"}
# App Routes 
app.register_blueprint(Responses)

if __name__ == '__main__':
    app.run(debug=True)
