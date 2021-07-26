# from gpiozero import Motor, DigitalOutputDevice
from time import localtime, sleep
from pi_logic.thermostat_logic import run_fan_only

# motor = Motor(forward=23, backward=24, enable=12, pwm=True)
# fan = DigitalOutputDevice(14, active_high=True)


def reset_sprayer():
    print('Resetting the sprayer to start position...')
    # motor.backward(speed=0.3)
    sleep(0.1)
    # motor.stop()


def cycle_sprayer_motor(manual=False, num_sprays=1):
    """
    Fully cycles sprayer motor for x number of cycles.
    """

    if check_time(manual):
        for i in range(num_sprays):
            print(f'Cycle {i + 1} of {num_sprays}')
            # motor.forward(speed=0.4)
            sleep(0.6)
            # motor.backward(speed=0.3)
            sleep(0.3)
            # motor.stop()
            sleep(1)


def check_time(manual=False):
    """
    Checks time to spray between the hours of 0700 and 2200.
    """

    hours = localtime().tm_hour

    if 7 < hours < 22:  # run between 7am and 10pm (2200 hrs)
        print('Currently daytime, cycling sprayer...')
        return True

    elif manual:
        print('Cycling sprayer manually...')
        return True

    return False


def temporarily_stop_cycle(num_days):
    # minutes in a day: 24 hours * 60 minutes
    minutes_per_day = 24 * 60
    requested_time = minutes_per_day * num_days

    sleep(requested_time)


def cycle_sprayer_manually():
    print('Cycling sprayer manually...')
    run_fan_only()
    sleep(10)
    cycle_sprayer_motor(True)
