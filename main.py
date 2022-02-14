from pi_logic.thermostat_logic import get_thermostat_status
from pi_logic.motor_logic import cycle_sprayer_motor, reset_sprayer
from time import sleep
from datetime import datetime


def check_hvac_status():
    """
    Checks status of thermostat. If heating or cooling it will actuate the air freshener motor
    and then wait 20 minutes before returning to check the status again.
    """
    minute = 60

    current_hvac_status = get_thermostat_status()

    if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
        print(
            f'HVAC system currently \'{current_hvac_status}\'. Cycling air freshener... on {datetime.now()}')
        cycle_sprayer_motor()
        sleep(minute)  # wait 30 minutes before spraying again
    else:
        # wait 5 minutes to check again if no hvac is not active
        sleep(minute)


def start_main_hvac_event_loop():
    """
    Resets sprayer to starting position and initiates event loop to monitor
    HVAC system status.
    """
    reset_sprayer()

    try:
        # main event loop
        while True:
            check_hvac_status()

    except KeyboardInterrupt:
        print('User interrupted. Terminating...')


if __name__ == '__main__':
    start_main_hvac_event_loop()
