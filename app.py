from flask import Flask, jsonify, render_template
from tinydb import TinyDB, Query
from datetime import datetime
from . import constants
from pi_logic import motor_logic, thermostat_logic
import json
import requests

app = Flask(__name__)
db = TinyDB('./db.json')
table = db.table('spray_timestamp')
Spray = Query()

@app.route('/spray_air_freshener', methods=['POST'])
def spray_air_freshener():
    """
    Accepts POST request to cycle sprayer motor on button press.
    """
    
    # motor_logic.cycle_sprayer_manually()
    print('hitting sprayer endpoint manually...')
    date = datetime.now().strftime('%m/%d/%y')
    time = datetime.now().strftime('%H:%M:%S')

    if len(table.all()) > 0:
        # print(f'updating db entry: {table.all()[0]} to {time}')
        table.update({'date': date, 'time': time})
        # print(f'updated db entry: {table.all()[0]}')
    else: 
        # print(f'db search: {table.all()}')
        table.insert({'date': f"{date}", 'time': f'{time}'})

    response = jsonify({'date': date , 'time': time})
    response.headers.add('Access-Control-Allow-Origin', '*')

    URL = f'http://{constants.FRONT_END_IP}/timestamp'
    params = {"date": date, "time": time}
    requests.patch(url=URL, params=params)

    return response


@app.route('/get_timestamp', methods=['GET'])
def get_last_time_sprayed():
    """
    Return last time sprayers was cycled
    """

    last_sprayed = table.all()[0]['time']
    print(f'returning last time sprayed: {last_sprayed}')
    response = jsonify({'time': last_sprayed}, 200, {
                       'ContentType': 'application/json'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/get_system_status', methods=['GET'])
def get_system_status():
    """
    GET request to return current system status
    """

    system_status = thermostat_logic.get_current_system_status()
    return json.dumps({'system_status': system_status})


@app.route('/start_main_loop', methods=['POST'])
def start_main_loop():
    """
    Accepts GET request to start main loop process
    """
    
    try:
        # main_loop.start()
        print("Main loop started.")
    except AssertionError:
        print("Main loop is already running.")
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/stop_main_loop", methods=['POST'])
def stop_main_loop():
    """
    Accepts GET request to terminate main loop process
    """
    
    try:
        # main_loop.terminate()
        print("Main loop terminated.")
    except AttributeError:
        print("Main loop not running.")
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    # main_loop = Process(target=main.start_main_hvac_event_loop(), daemon=True)
    app.run(host='0.0.0.0', port=80, load_dotenv=True, debug=True)
