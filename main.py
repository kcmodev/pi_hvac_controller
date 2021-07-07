import thermostat_logic
import motor_logic
from time import sleep

"""
TODO:
    Determine length of time since it last sprayed
"""


def check_hvac_status():
    current_hvac_status = thermostat_logic.run_thermostat_logic()

    # cycle sprayer every 20 mins until no longer active
    if current_hvac_status == 'COOLING' or current_hvac_status == 'HEATING':
        print(
            f'HVAC system \'{current_hvac_status}\'. Cycling air freshener...')
        motor_logic.run_motor_logic()  # run air freshener logic
        sleep(1200)  # wait 20 mins (1200 sec) before spraying again
    else:
        # wait 60 secs to check again if no activity detected
        sleep(60)


if __name__ == "__main__":
    try:
        # main event loop
        while True:  # check status every 60 seconds
            check_hvac_status()

    except KeyboardInterrupt:
        print('User interrupted. Terminating...')
