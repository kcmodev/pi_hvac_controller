from gpiozero import Motor, DigitalOutputDevice
from time import localtime, sleep, asctime
from pi_logic.thermostat_logic import run_fan_only

motor = Motor(forward=23, backward=24, enable=12, pwm=True)
fan = DigitalOutputDevice(14, active_high=True)


def reset_sprayer():
    print('Resetting the sprayer to start position...')
    motor.backward(speed=0.3)
    sleep(0.1)
    motor.stop()


def cycle_sprayer_motor(num_sprays=2):
    """
    Fully cycles sprayer motor for x number of cycles.
    """ 
    print(f'{asctime(localtime())} -- Cycling sprayer motor...')
    for i in range(num_sprays):
        print(f'\tCycle {i + 1} of {num_sprays}')
        motor.forward(speed=0.6)
        sleep(0.5)
        motor.stop()
        sleep(3)


def temporarily_stop_cycle(num_days):
    # minutes in a day: 24 hours * 60 minutes * 60 seconds
    minutes_per_day = 24 * 60 * 60
    requested_time = minutes_per_day * num_days

    print(f'Pausing program for {num_days} days.')
    sleep(requested_time)


def cycle_sprayer_manually():
    print(f'{asctime(localtime())} -- Manually cycling sprayer...')
    run_fan_only()
    sleep(10)
    cycle_sprayer_motor()
