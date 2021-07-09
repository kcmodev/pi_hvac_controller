# from gpiozero import Motor
from time import localtime, sleep
from .thermostat_logic import run_fan_only

# motor = Motor(forward=4, backward=14)

# TODO: Try this one next time to use pwm instead
# NOTE: Forward = GPIO 12 (PWM0)
# NOTE: Backward = GPIO 13 (PWM1)
# motor = Motor(forward=12, backward=13, pwm=True)


def reset_sprayer():
    print('Resetting the sprayer to start position...')
#     motor.backward(speed=0.5)
#     sleep(0.1)
#     motor.stop()


def cycle_sprayer_motor():
    """
    Fully cycles sprayer motor for x number of cycles.
    """
    num_sprays = 1
#     # TODO: Recheck speeds while using pwm and ensure actuating force is appropriate.

    if check_time():
        for i in range(num_sprays):
            print(f'Cycle {i+1} of {num_sprays}')
    #         motor.forward(speed=0.5)
    #         sleep(1)
    #         motor.backward(speed=0.5)
    #         sleep(0.3)
    #         motor.stop()
    #         sleep(1)


def check_time():
    """
    Checks time to spray between the hours of 0700 and 2200.
    """

    hours = localtime().tm_hour

    if 7 < hours < 22:  # run between 7am and 10pm (2200 hrs)
        print('Currently daytime, cycling sprayer...')
        return True

    return False


def cycle_sprayer_manually():
    print('Cycling sprayer manually...')
    run_fan_only()
    sleep(15)
    cycle_sprayer_motor()
