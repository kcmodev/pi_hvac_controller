from pi_logic.thermostat_logic import get_thermostat_status, check_hvac_connectivity
from pi_logic.motor_logic import cycle_sprayer_motor, reset_sprayer
from time import sleep, localtime, asctime
from datetime import datetime


def check_hvac_status(manual=True):
    """
    Checks status of thermostat. If heating or cooling it will actuate the air freshener motor
    and then wait 20 minutes before returning to check the status again.
    """
    minute = 60
    current_hour = localtime().tm_hour
    
    if 7 <= current_hour <= 22:
        # only automatically check status during the day
        current_hvac_status = get_thermostat_status()

        if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
            print(
                f'{asctime(localtime())} -- HVAC system currently {current_hvac_status}.')
            cycle_sprayer_motor()
            print('Waiting 30 minutes to spray again...')
            sleep(minute * 30)  # wait 30 minutes before spraying again
        else:
            # wait 5 minutes to check again if no hvac is not active
            print(f'{asctime(localtime())} -- HVAC system currently {current_hvac_status}. Sleeping for 5 minutes.')
            sleep(minute * 5)
    else:
        print(f'{asctime(localtime())} -- Currently night time. Waiting 30 minutes to check time again...')
        sleep(minute * 30)


def start_main_hvac_event_loop():
    """
    Resets sprayer to starting position and initiates event loop to monitor
    HVAC system status.
    """

    print(f'{asctime(localtime())} -- Starting main event loop...')
    try:
        while True:
            check_hvac_status()

    except KeyboardInterrupt:
        print('User interrupted. Terminating...')


if __name__ == '__main__':
    start_main_hvac_event_loop()
