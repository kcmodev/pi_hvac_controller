import RPi.GPIO as GPIO
import time

while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print("LED ON")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1)
    print("LED OFF")
    GPIO.output(18, GPIO.LOW)
    time.sleep(1)
