from gpiozero import Motor
from time import sleep

motor = Motor(forward=4, backward=14)

def cycle_sprayer():
    motor.backward(speed=0.5)
    sleep(0.6)
    motor.forward(speed=0.5)
    sleep(0.3)

cycle_sprayer()
motor.stop()