# from gpiozero import Motor
from time import time, localtime

# motor = Motor(forward=4, backward=14)


# def reset_sprayer():
#     print('Resetting the sprayer...')
#     motor.backward(speed=0.5)
#     sleep(0.1)
#     motor.stop()


# def cycle_sprayer_motor():
#     # fully cycles sprayer for num sprays
#     num_sprays = 1

#     for i in range(num_sprays):
#         print(f'Cycle {i+1} of {num_sprays}')
#         motor.forward(speed=0.5)
#         sleep(1)
#         motor.backward(speed=0.6)
#         sleep(0.3)
#         motor.stop()
#         sleep(1)


def check_time():
    # checks time to spray between the hours of
    # 0700 and 2200

    hours = localtime().tm_hour

    if 7 < hours < 22:  # run between 7am and 10pm (2200 hrs)
        print('Currently daytime, cycling sprayer...')
        # cycle_sprayer_motor()


def run_motor_logic():
    # reset_sprayer()
    check_time()
