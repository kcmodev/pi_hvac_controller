import requests
import json


def get_new_token():
    """
    Sends a post request to authenticate and retrieve the oauth access token.
    """

    URL = 'https://www.googleapis.com/oauth2/v4/token'

    DATA = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'refresh_token': config.REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }

    res = requests.post(url=URL, data=DATA)
    res_json = res.json()
    access_token = f'{res_json["token_type"]} {res_json["access_token"]}'

    print(f'token data: \n {json.dumps(res_json, indent=2)}')

    return access_token


def get_thermostat_status():
    """
    Uses the access token to retrieve the current status of the thermostat.
    """

    token = get_new_token()

    URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices/{config.DEVICE_ID}'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    res = requests.get(URL, headers=HEADERS)
    res_json = res.json()

    #print(f'hvac response: \n {json.dumps(res_json, indent=2)}')

    current_status = res_json['traits']['sdm.devices.traits.ThermostatHvac']['status']

    print(f'Current HVAC status: {current_status}')

    return current_status


def run_fan_only():
    token = get_new_token()

    URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices/{config.DEVICE_ID}:executeCommand'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    DATA = "{ 'command': 'sdm.devices.commands.Fan.SetTimer', 'params': { 'timerMode': 'ON', 'duration': '900s' } }"

    requests.post(url=URL, headers=HEADERS, data=DATA)

    print('Fan running for 15 mins...')


def check_hvac_connectivity():
    token = get_new_token()

    URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    res = requests.get(url=URL, headers=HEADERS)
    print(f'res {res}')
    res_json = res.json()

    print(f'connectivity data: \n {json.dumps(res_json, indent=2)}')


if __name__ == 'pi_hvac_controller.pi_logic.thermostat_logic':
    """
    Corrects import to parent folder when importing with Flask from /venv/bin/activate.
    """
    from ..config_settings import config

elif __name__ == 'pi_logic.thermostat_logic':
    from config_settings import config
