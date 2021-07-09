# from thermostat_logic import run_thermostat_logic
# from motor_logic import run_motor_logic
from pi_logic.thermostat_logic import run_thermostat_logic
from pi_logic.motor_logic import run_motor_logic
from time import sleep


def check_hvac_status():
    """
    Checks status of thermostat. If heating or cooling it will actuate the air freshener motor
    and then wait 20 minutes before returning to check the status again.
    """

    current_hvac_status = run_thermostat_logic()

    if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
        print(
            f'HVAC system \'{current_hvac_status}\'. Cycling air freshener...')
        run_motor_logic()  # run air freshener logic
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
