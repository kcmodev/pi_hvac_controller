import datetime
import requests
import json
from time import asctime, localtime

token = ''
current_status = ''


def get_new_token():
    """
    Sends a post request to authenticate and retrieve the oauth access token.
    """
    global token

    oauth_url = 'https://www.googleapis.com/oauth2/v4/token'

    data = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'refresh_token': config.REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }

    res = requests.post(url=oauth_url, data=data)
    res_json = res.json()
    token = f'{res_json["token_type"]} {res_json["access_token"]}'


def get_thermostat_status():
    """
    Uses the access token to retrieve the current status of the thermostat.
    """
    global token, current_status

    status_url = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/' \
                 f'{config.PROJECT_ID}/devices/{config.DEVICE_ID}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    try:  # try to make a request to the api, if it fails get a new key
        res = requests.get(status_url, headers=headers)
        response_as_json = res.json()
        print(f'hvac response: \n {json.dumps(response_as_json, indent=2)}')

        if 'error' in response_as_json:
            response_status = response_as_json['error']['status']

            print(f'response status: {response_status}')

            if response_status == 'UNAUTHENTICATED':
                raise ConnectionRefusedError
        else:
            current_status = response_as_json['traits']['sdm.devices.traits.ThermostatHvac']['status']
            print(f'Current HVAC status: {current_status} on {datetime.datetime}')

    except ConnectionRefusedError:
        print('Connection refused. Generating new token and trying again.')
        get_new_token()
        get_thermostat_status()

    except KeyError as e:
        print(f'Key error: {e}')
        pass

    except ConnectionError:
        print('Connection error. Generating new token and trying again.')
        get_new_token()
        get_thermostat_status()


def run_fan_only():
    global token, current_status

    fan_url = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/' \
              f'{config.PROJECT_ID}/devices/{config.DEVICE_ID}:executeCommand'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    data = "{ 'command': 'sdm.devices.commands.Fan.SetTimer', " \
           "'params': { 'timerMode': 'ON', 'duration': '900s' } }"

    try:
        response = requests.post(url=fan_url, headers=headers, data=data)
        response_as_json = response.json()
        
        if 'error' in response_as_json:
            response_status = response_as_json['error']['status']

            print(f'response status: {response_status}')

            if response_status == 'UNAUTHENTICATED':
                raise ConnectionRefusedError
            
        print('Fan running for 15 minutes...')
        
    except ConnectionRefusedError:
        print('Connection refused. Generating new token and trying again.')
        get_new_token()
        run_fan_only()

    except KeyError as e:
        print(f'Key error: {e}')
        pass

    except ConnectionError:
        print('Connection error. Generating new token and trying again.')
        get_new_token()
        run_fan_only()


def check_hvac_connectivity():
    global token, current_status

    device_list_url = f'https://smartdevicemanagement.googleapis.com/v1/enterprises/{config.PROJECT_ID}/devices'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    res = requests.get(url=device_list_url, headers=headers)
    res_json = res.json()

    print(f'connectivity data: \n {json.dumps(res_json, indent=2)}')


def get_current_system_status():
    return current_status


if __name__ == 'pi_hvac_controller.pi_logic.thermostat_logic':
    """
    Corrects import to parent folder when importing with Flask from /venv/bin/activate.
    """
    from ..config_settings import config

elif __name__ == 'pi_logic.thermostat_logic':
    from config_settings import config
