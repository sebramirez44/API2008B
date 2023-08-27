import json
from flask import Flask

from agents import Puerto

app = Flask(__name__)

model = Puerto()

@app.route('/')
def index():
    model.step()
    datos = model.get_data()
    return datos

app.run()