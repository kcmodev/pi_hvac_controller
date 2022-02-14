from flask import Flask, jsonify, render_template
import json
from pi_logic import motor_logic, thermostat_logic

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    '''
    Renders landing page for user interaction.
    '''
    global system_status, last_spray_time

    return render_template('index.html', system_status=system_status, last_spray_time=last_spray_time)


@app.route("/spray_air_freshener", methods=['POST'])
def spray_air_freshener():
    '''
    Accepts POST request to cycle sprayer motor on button press.
    '''
    motor_logic.cycle_sprayer_manually()
    response = jsonify({'success': True}, 200, {'ContentType': 'application/json'})
    response.headers.add('Access-Control-Allow-Origin', '*')
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return response


@app.route("/get_last_time_sprayed", methods=['GET'])
def get_last_time_sprayed():
    last_sprayed = motor_logic.get_last_time_cycled_sprayer()
    return jsonify(last_sprayed)


@app.route("/get_system_status", methods=['GET'])
def get_system_status():
    system_status = thermostat_logic.get_current_system_status()
    return jsonify(system_status)


@app.route("/start_main_loop", methods=['POST'])
def start_main_loop():
    '''
    Accepts GET request to start main loop process
    '''
    try:
        # main_loop.start()
        print('Main loop started.')
    except AssertionError:
        print('Main loop is already running.')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/stop_main_loop", methods=['POST'])
def stop_main_loop():
    '''
    Accepts GET request to terminate main loop process
    '''
    try:
        # main_loop.terminate()
        print('Main loop terminated.')
    except AttributeError:
        print('Main loop not running.')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    # main_loop = Process(target=main.start_main_hvac_event_loop(), daemon=True)
    app.run(host='0.0.0.0', port=80, load_dotenv=True)
