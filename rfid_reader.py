#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import signal

led = 40

# Setup GPIO
def setup_gpio():
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)

# Cleanup GPIO
def cleanup_gpio(signal, frame):
    GPIO.cleanup()
    exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup_gpio)
signal.signal(signal.SIGTERM, cleanup_gpio)

def main():
    reader = SimpleMFRC522()
    
    while True:
        try:
            id, text = reader.read()
            print(id)
            print(type(id))
            print(text)
            sleep(2)

            if id == 837695175856:
                sleep(2)
                GPIO.output(led, GPIO.HIGH)
                sleep(1)
                GPIO.output(led, GPIO.LOW)
            else:
                GPIO.output(led, GPIO.LOW)

        except Exception as e:
            print(f"An error occurred: {e}")
            cleanup_gpio(None, None)

if __name__ == "__main__":
    setup_gpio()
    main()

