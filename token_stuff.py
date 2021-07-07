import requests
import config
import json


def get_new_token():
    URL = 'https://www.googleapis.com/oauth2/v4/token'

    PAYLOAD = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'refresh_token': config.REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }

    r = requests.post(url=URL, data=PAYLOAD)
    r = r.json()
    access_token = r['token_type'] + ' ' + r['access_token']

    # print(f'data returned: \n {r}')
    # print(f'NEW access token: \'{access_token}\'')

    # return access_token
    # get_thermostat_status(access_token)
    return access_token


def get_thermostat_status(x):
    URL = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices/{config.DEVICE_ID}'

    PAYLOAD = {
        'Content-Type': 'application/json',
        'Authorization': x
    }

    res = requests.get(URL, headers=PAYLOAD)
    res_json = res.json()

    # print(f'response: \n {json.dumps(res_json, indent=2)}')

    current_status = res_json['traits']['sdm.devices.traits.ThermostatHvac']['status']

    print(f'hvac current status: {current_status}')


new_token = get_new_token()
get_thermostat_status(new_token)
