from gpiozero import Motor, MotionSensor, LED
from signal import pause
from time import sleep

motor = Motor(forward=4, backward=14)
pir_sensor = MotionSensor(26)
led = LED(16)

def reset_sprayer():
    print('resetting the sprayer...')
    motor.forward(speed=0.5)
    sleep(0.1)
    motor.stop()

def cycle_sprayer():
    motor.backward(speed=0.6)
    sleep(0.75)
    motor.forward(speed=0.5)
    sleep(0.3)
    motor.stop()

def spray_the_can():
    print("spraying the air freshener...")
    led.on()
    cycle_sprayer()
    sleep(2)
    led.off()

if __name__ == "__main__":
    reset_sprayer() # set sprayer to starting position
    
    try:
        pir_sensor.when_motion = spray_the_can
        
    except KeyboardInterrupt:
        print('user interrupt detected. terminating...')
        
        
        
        
        