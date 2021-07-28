from gpiozero import Motor, DigitalOutputDevice
from time import localtime, sleep
from pi_logic.thermostat_logic import run_fan_only

motor = Motor(forward=23, backward=24, enable=12, pwm=True)
fan = DigitalOutputDevice(14, active_high=True)


def reset_sprayer():
    print('Resetting the sprayer to start position...')
    motor.backward(speed=0.3)
    sleep(0.1)
    motor.stop()


def cycle_sprayer_motor(manual=False, num_sprays=2):
    """
    Fully cycles sprayer motor for x number of cycles.
    """ 
    for i in range(num_sprays):
        print(f'Cycle {i + 1} of {num_sprays}')
        motor.forward(speed=0.4)
        sleep(0.6)
        motor.backward(speed=0.3)
        sleep(0.3)
        motor.stop()
        sleep(1)


def temporarily_stop_cycle(num_days):
    # minutes in a day: 24 hours * 60 minutes * 60 seconds
    minutes_per_day = 24 * 60 * 60
    requested_time = minutes_per_day * num_days

    print(f'Pausing program for {num_days} days.')
    sleep(requested_time)


def cycle_sprayer_manually():
    print('Cycling sprayer manually...')
    run_fan_only()
    sleep(10)
    cycle_sprayer_motor(manual=True)
