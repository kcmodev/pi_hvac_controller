from pi_logic.thermostat_logic import get_thermostat_status
from pi_logic.motor_logic import cycle_sprayer_motor
from time import sleep


def check_hvac_status():
    """
    Checks status of thermostat. If heating or cooling it will actuate the air freshener motor
    and then wait 20 minutes before returning to check the status again.
    """

    current_hvac_status = get_thermostat_status()
    current_hvac_status = 'COOLING'

    if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
        print(
            f'HVAC system currently \'{current_hvac_status}\'. Cycling air freshener...')
        cycle_sprayer_motor()  # run air freshener logic
        sleep(1200)  # wait 20 mins (1200 sec) before spraying again
    else:
        # wait 60 secs to check again if no activity detected
        sleep(60)


if __name__ == "__main__":
    try:
        # main event loop
        while True:
            check_hvac_status()

    except KeyboardInterrupt:
        print('User interrupted. Terminating...')
