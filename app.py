import flask
from flask import Flask, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
from pi_logic import motor_logic, thermostat_logic
import json

app = Flask(__name__)
db = TinyDB('./db.json')
table = db.table('spray_timestamp')
Spray = Query()


@app.route('/spray', methods=['POST'])
def spray_air_freshener():
    """
    Request to cycle sprayer motor.
    """
    
    # motor_logic.cycle_sprayer_manually()
    print('hitting sprayer endpoint manually...')
    date = datetime.now().strftime('%m/%d/%y')
    time = datetime.now().strftime('%H:%M:%S')

    if len(table.all()) > 0:
        print(f'updating db entry: {table.all()[0]} to {time}')
        # table.update({'date': date, 'time': time})
        # print(f'updated db entry: {table.all()[0]}')
    else: 
        print(f'db search: {table.all()}')
        # table.insert({'date': f"{date}", 'time': f'{time}'})

    response = jsonify({'date': date, 'time': time})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/timestamp', methods=['GET', 'POST'])
def get_last_time_sprayed():
    """
    Return last time sprayers was cycled
    """
    if flask.request.method == 'GET':
        last_sprayed_time = table.all()[0]['time']
        last_sprayed_date = table.all()[0]['date']
        print(f'returning last time sprayed: {last_sprayed_time}')
        response = jsonify({'time': last_sprayed_time, 'date': last_sprayed_date})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    elif flask.request.method == 'POST':
        data = flask.request.data
        print(f'saving data to db: {data}')


@app.route('/status', methods=['GET'])
def get_system_status():
    """
    Returns current system status
    """
    status = thermostat_logic.get_current_system_status()
    response = jsonify({'status': status})
    return response


@app.route('/start', methods=['POST'])
def start_main_loop():
    """
    Starts main loop background process
    """
    try:
        # main_loop.start()
        print("Main loop started.")
    except AssertionError:
        print("Main loop is already running.")
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/stop", methods=['POST'])
def stop_main_loop():
    """
    Terminates main loop process
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
