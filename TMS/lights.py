import Rpi.GPIO as GPIO
import threading
from time import sleep

class TrafficLight:
    """
    Create traffic light objects
    """

    def __init__(self, red_led, yellow_led, green_led):
        """
        """
        #set pinmodes etc...
        self.red_led = red_led
        self.green_led = green_led
        self.yellow_led = yellow_led
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(red_led, GPIO.OUT)
        GPIO.setup(green_led, GPIO.OUT)
        GPIO.setup(yellow_led, GPIO.OUT)



    def go_red(self, yellow_duration=10):
        """
        Become Yellow for yellow_duration (s). Then turn red
        """
        GPIO.output(self.green_led, GPIO.LOW)
        GPIO.output(self.yellow_led, GPIO.HIGH)
        sleep(yellow_duration)
        GPIO.output(self.yellow_led, GPIO.LOW)
        GPIO.output(self.red_led, GPIO.HIGH)

    def go_green(self):
        """
        Become green_led
        """
        GPIO.output(self.green_led, GPIO.HIGH)

    def stop_traffic(self, duration=10):
        """
        """
        thread = threading.Thread(target=self.go_red, args=(duration,))
        thread.start()
        return thread

    def start_traffic(self, duration=10):
        """
        """
        thread = threading.Thread(target=self.go_green)
        thread.start()
        return thread
