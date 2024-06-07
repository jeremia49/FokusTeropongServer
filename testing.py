import RPi.GPIO as GPIO
import time

tilt1_pin = 17
tilt2_pin = 27

light1_pin = 22
light2_pin = 23

buzzer_pin = 24

addpower_pin = 25
addpower2_pin = 16


GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tilt2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(light1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(light2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
        
GPIO.setup(addpower_pin, GPIO.OUT)
GPIO.setup(addpower2_pin, GPIO.OUT)
GPIO.output(addpower_pin, GPIO.HIGH)
GPIO.output(addpower2_pin, GPIO.HIGH)

try:
    while True:
        hidupkanbuzzer =  False
        if GPIO.input(tilt1_pin) == GPIO.LOW: #low tidak sesuai
            print("Tilt 1 error")
            hidupkanbuzzer = True
        if GPIO.input(tilt2_pin) == GPIO.LOW: #low tidak sesuai
            print("Tilt 2 error")
            hidupkanbuzzer = True
        if GPIO.input(light1_pin) == GPIO.HIGH: #high tidak sesuai
            print("Light 1 error")
            hidupkanbuzzer = True
        if GPIO.input(light2_pin) == GPIO.HIGH: #high tidak sesuai
            print("Light 2 error")
            hidupkanbuzzer = True
        
        if(hidupkanbuzzer):
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            print("Sesuai")
            GPIO.output(buzzer_pin, GPIO.LOW)
        
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()