

import FakeRPi.GPIO as GPIO
# import RPi.GPIO as GPIO
import threading
from time import sleep


#pin assignment
# dict format --> {"light_num": [red, yellow, green]}
light_pins = {"1" : [3, 5, 7],
              "2" : [11, 13, 15],
              "3" : [19, 21, 23],
              "4" : [22, 24, 26],
              "5" : [29, 31, 33],
              "6" : [36, 38, 40]}


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

    def go_green(self, green_duration=30):
        """
        Become green_led
        """
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.HIGH)
        sleep(green_duration)

    def stop_traffic(self, duration=10):
        """
        """
        thread = threading.Thread(target=self.go_red, args=(duration,))
        thread.start()
        return thread

    def start_traffic(self, duration=30):
        """
        """
        thread = threading.Thread(target=self.go_green, args=(duration,))
        thread.start()
        return thread


#creating traffic light objects
traffic_lights = {}
for key, value in light_pins.items():
    traffic_lights[key] = TrafficLight(value[0], value[1], value[2])


def turn_on(traffic_light):
    """Accepts a string"""
    print("{} turn on".format(traffic_light))
    traffic_lights[traffic_light].start_traffic(duration=30)

def turn_off(traffic_light):
    """Accepts a string"""
    print("{} turn off".format(traffic_light))
    traffic_lights[traffic_light].stop_traffic(duration=10)
