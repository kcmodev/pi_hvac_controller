import requests
import config
import json


def get_new_token():
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

    # print(f'data returned: \n {json.dumps(res_json, indent=2)}')

    return access_token


def get_thermostat_status(token):
    URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices/{config.DEVICE_ID}'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    res = requests.get(URL, headers=HEADERS)
    res_json = res.json()

    # print(f'response: \n {json.dumps(res_json, indent=2)}')

    current_status = res_json['traits']['sdm.devices.traits.ThermostatHvac']['status']

    print(f'Current HVAC status: {current_status}')

    return current_status


def run_thermostat_logic():
    new_token = get_new_token()
    hvac_status = get_thermostat_status(new_token)

    return hvac_status
