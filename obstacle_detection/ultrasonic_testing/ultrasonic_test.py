import RPi.GPIO as GPIO
import time
import logging

# Logging config
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ⚠️ Double-check these GPIO pin numbers!
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

logging.info("Ultrasonic Sensor Testing...")

try:
    while True:
        GPIO.output(TRIG, False)
        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        duration = pulse_end - pulse_start
        distance = duration * 17150
        distance = round(distance, 2)

        logging.info(f"Distance: {distance} cm")

except KeyboardInterrupt:
    GPIO.cleanup()
