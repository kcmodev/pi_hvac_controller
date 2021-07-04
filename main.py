from gpiozero import Motor, MotionSensor
from signal import pause
from time import sleep, localtime as lt, process_time as pt

motor = Motor(forward=4, backward=14)
pir_sensor = MotionSensor(26)
prev_process_time = ''


"""
TODO:
    Determine length of time since it last sprayed
"""

def reset_sprayer():
    print('Resetting the sprayer...')
    motor.backward(speed=0.5)
    sleep(0.1)
    motor.stop()

def cycle_sprayer_motor():
    # fully cycles sprayer for num sprays
    num_sprays = 2
    
    for i in range(num_sprays):
        print(f'Cycle {i+1} of {num_sprays}')
        motor.forward(speed=0.5)
        sleep(1)
        motor.backward(speed=0.6)
        sleep(0.3)
        motor.stop()
        sleep(1)
    
def check_time(hours, proc_time):
    # checks time to spray between the hours of
    # 0700 and 2200
    # also checks to cycle only once every 10 minutes
    curr_process_time = proc_time
    
    if 7 < hours < 22:
        print('Currently daytime, cycling sprayer...')
        process_time_diff = curr_process_time - prev_process_time
        
        if  process_time_diff <= 60:
            print('No spray recently, spraying....')
            prev_process_time = proc_time
            #cycle_sprayer_motor()
        else:
            print(f'Difference in time was only {tim_diff}. NOT spraying...')
    else:
        print('Currently night time, NOT cycling sprayer...')
    

def spray_the_can():
    # detect how long it has been since it has sprayed
    
    print("spraying the air freshener...")
    
    curr_time = lt()
    curr_hour = curr_time.tm_hour
    curr_min = curr_time.tm_min
    
    print(f'current time: {curr_hour}{curr_min}')
    
    check_time(curr_hour, pt())
    
    sleep(2)
    pir_sensor.wait_for_motion()

if __name__ == "__main__":
    reset_sprayer() # set sprayer to starting position
    
    try:
        pir_sensor.when_motion = spray_the_can
        
    except KeyboardInterrupt:
        print('User interrupt detected. terminating...')
        
        
        
        
        