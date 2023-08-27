import json
from flask import Flask

from agentes import Puerto

app = Flask(__name__)

model = Puerto()

@app.route('/index')
def index():
    model.step()
    datos = model.get_data()
    serialized_data = json.dumps(datos)
    return serialized_data

app.run()