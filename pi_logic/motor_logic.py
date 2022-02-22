# from gpiozero import Motor, DigitalOutputDevice
from datetime import datetime
from time import sleep
from pi_logic.thermostat_logic import run_fan_only

# motor = Motor(forward=23, backward=24, enable=12, pwm=True)
# fan = DigitalOutputDevice(14, active_high=True)
last_spray_time = ""


def reset_sprayer():
    print("Resetting the sprayer to start position...")
    # motor.backward(speed=0.3)
    sleep(0.1)
    # motor.stop()


def cycle_sprayer_motor(manual=False, num_sprays=2):
    """
    Fully cycles sprayer motor for x number of cycles.
    """
    global last_spray_time

    if check_time(manual):
        for i in range(num_sprays):
            print(f'Cycle {i + 1} of {num_sprays}')
#             motor.forward(speed=0.4)
            sleep(0.6)
#             motor.backward(speed=0.3)
            sleep(0.3)
#             motor.stop()
            sleep(1)

        last_spray_time = datetime.now()


def check_time(manual=False) -> bool:
    """
    Checks time to spray between the hours of 0700 and 2200.
    """

    hours = datetime.now().hour

    if 7 < hours < 22:  # run between 7am and 10pm (2200 hrs)
        print("Currently daytime, cycling sprayer...")
        return True
    elif manual:
        print("Cycling sprayer manually...")
        return True

    return False


def temporarily_stop_cycle(num_days):
    minutes_per_day = 24 * 60  # 24 hours * 60 minutes
    requested_time = minutes_per_day * num_days
    sleep(requested_time)


def cycle_sprayer_manually():
    print(f"{datetime.now()} -- Manually cycling sprayer...")
    run_fan_only()
    sleep(10)
    cycle_sprayer_motor(True)


def get_last_time_cycled_sprayer() -> str:
    return last_spray_time
