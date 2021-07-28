from pi_logic.thermostat_logic import get_thermostat_status, check_hvac_connectivity
from pi_logic.motor_logic import cycle_sprayer_motor, reset_sprayer
from time import sleep, localtime
from datetime import datetime


def check_hvac_status(manual=True):
    """
    Checks status of thermostat. If heating or cooling it will actuate the air freshener motor
    and then wait 20 minutes before returning to check the status again.
    """
    minute = 60
    current_hour = localtime().tm_hour
    
    if 7 < current_hour < 22:
        # only automatically check status during the day
        current_hvac_status = get_thermostat_status()

        if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
            print(
                f'HVAC system currently \'{current_hvac_status}\'. Cycling air freshener... on {datetime.now()}')
            cycle_sprayer_motor()
            sleep(minute * 30)  # wait 30 minutes before spraying again
        else:
            # wait 5 minutes to check again if no hvac is not active
            sleep(minute * 5)
    else:
        print('Currently night time, process sleeping...')
        sleep(minute * 60)


def start_main_hvac_event_loop():
    """
    Resets sprayer to starting position and initiates event loop to monitor
    HVAC system status.
    """
    reset_sprayer()

    try:
        while True:
            check_hvac_status()

    except KeyboardInterrupt:
        print('User interrupted. Terminating...')


if __name__ == '__main__':
    pass
