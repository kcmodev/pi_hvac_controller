from flask import Flask, render_template
from .pi_logic.motor_logic import cycle_sprayer_manually
import json

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route("/spray_air_freshener", methods=['GET'])
def spray_air_freshener():
    cycle_sprayer_manually()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
