import RPi.GPIO as GPIO
import time


class Sensor():

    def __init__(self):  
        self.status = "OK"      
        self.shouldBuzzerOn = False
        self.tilt1_pin = 17
        self.tilt2_pin = 27

        self.light1_pin = 22
        self.light2_pin = 23

        self.buzzer_pin = 24

        self.addpower_pin = 25
        self.addpower2_pin = 16

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.tilt1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.tilt2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.light1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.light2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        
        GPIO.setup(self.addpower_pin, GPIO.OUT)
        GPIO.setup(self.addpower2_pin, GPIO.OUT)
        GPIO.output(self.addpower_pin, GPIO.HIGH)
        GPIO.output(self.addpower2_pin, GPIO.HIGH)

        GPIO.output(self.buzzer_pin, GPIO.LOW)
    
    def alertDeteksiGagal(self):
        if(not self.shouldBuzzerOn):
            return
        GPIO.output(self.buzzer_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        time.sleep(2)


    def start_sensor(self):
        try:
            while True:
                hidupkanbuzzer =  False
                if GPIO.input(self.tilt1_pin) == GPIO.LOW: #low tidak sesuai
                    self.status = "Tilt 1 error"
                    print("Tilt 1 error")
                    hidupkanbuzzer = True
                if GPIO.input(self.tilt2_pin) == GPIO.LOW: #low tidak sesuai
                    self.status = "Tilt 2 error"
                    print("Tilt 2 error")
                    hidupkanbuzzer = True
                if GPIO.input(self.light1_pin) == GPIO.HIGH: #high tidak sesuai
                    self.status = "Light 1 error"
                    print("Light 1 error")
                    hidupkanbuzzer = True
                if GPIO.input(self.light2_pin) == GPIO.HIGH: #high tidak sesuai
                    self.status = "Light 2 error"
                    print("Light 2 error")
                    hidupkanbuzzer = True
                
                if(hidupkanbuzzer):
                    # if(self.shouldBuzzerOn):
                    GPIO.output(self.buzzer_pin, GPIO.HIGH)
                    time.sleep(2)
                    GPIO.output(self.buzzer_pin, GPIO.LOW)
                    time.sleep(2)
                else:
                    self.status = "OK"
                    print("Sesuai")
                    GPIO.output(self.buzzer_pin, GPIO.LOW)
                
                time.sleep(1)
        except Exception as e:
            print(e)
        finally:
            GPIO.cleanup()
