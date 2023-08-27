import json
from flask import Flask

from agentes import Puerto

app = Flask(__name__)

model = Puerto()

# cada request nos dice la posicion en el siguiente step.
@app.route('/index')
def index():
    model.step()
    datos = model.get_data()
    # no todos los valores de id son numeros entonces hay que serializarlo
    serialized_data = json.dumps(datos)
    return serialized_data

app.run()