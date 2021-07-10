from flask import Flask, render_template
from pi_logic.motor_logic import cycle_sprayer_manually
import json

app = Flask(__name__)  # init flask app server


@app.route("/", methods=['GET'])
def index():
    """
    Renders landing page for user interaction.
    """
    
    return render_template('index.html')


@app.route("/spray_air_freshener", methods=['GET'])
def spray_air_freshener():
    """
    Accepts GET request to cycle sprayer motor on button press.
    """

    cycle_sprayer_manually()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
