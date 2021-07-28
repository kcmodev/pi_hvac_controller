from flask import Flask, render_template
from pi_logic.motor_logic import cycle_sprayer_manually
from multiprocessing import Process
import json

from main import start_main_hvac_event_loop

app = Flask(__name__)
system_status = 'Determining...'
last_spray_time = 0

# TODO: Set globals for system status, temp etc..
# TODO: Enhance web app styling
# TODO: Convert web app into PWA and find svg icons


@app.route("/", methods=['GET'])
def index():
    """
    Renders landing page for user interaction.
    """
    global system_status, last_spray_time

    return render_template('index.html', system_status=system_status, last_spray_time=last_spray_time)


@app.route("/spray_air_freshener", methods=['GET'])
def spray_air_freshener():
    """
    Accepts GET request to cycle sprayer motor on button press.
    """

    cycle_sprayer_manually()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/start_main_loop", methods=["GET"])
def start_main_loop():
    """
    Accepts GET request to start main loop process
    """
    try:
        main_loop.start()
        print('Main loop started.')
    except AssertionError:
        print('Main loop is already running.')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/stop_main_loop", methods=["GET"])
def stop_main_loop():
    """
    Accepts GET request to terminate main loop process
    """
    try:
        main_loop.terminate()
        print('Main loop terminated.')
    except AttributeError:
        print('Attribute error.')
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    main_loop = Process(target=start_main_hvac_event_loop, daemon=True)
    app.run(debug=True, host='0.0.0.0', port=80)
