#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import signal

# Define GPIO pins
led = 40

rfid_values = [
    837695175856,  # Heavy Sweater
    769133311166,  # RFID value for 0-5°C
    769903311166,  # RFID value for 5-10°C
    837695175889,  # RFID value for 10-15°C
    837695175900,  # RFID value for 15-20°C
    837695175911,  # RFID value for 20-25°C
    837695175922,  # RFID value for 25-30°C
    837695175933   # RFID value for above 30°C
]


# Setup GPIO
def setup_gpio():
    GPIO.setwarnings(False)  # Ignore warning for now
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
    setup_gpio()
    reader = SimpleMFRC522()
    count = 0  # Initialize a count variable
    id_value = None
    temp_id_value = None

    try:
        # Open the named pipe for reading
        with open("/tmp/myfifo", 'rb') as fifo_reader:  # Replace with the appropriate path
            while True:
                try:
                    rfid_value_bytes = fifo_reader.read()
                    id_value = int.from_bytes(rfid_value_bytes, byteorder='little', signed=True)
                    print("Received RFID Value ID:", id_value)
                    break  # Exit the loop after obtaining rfid_value

                except Exception as e:
                    print(f"An error occurred: {e}")
                    cleanup_gpio(None, None)

        # Create a new loop for RFID reading and LED control
        while True:
            id, _ = reader.read()
            
            if id != temp_id_value:
            	temp_id_value = id;
            	print(id)
            	count += 1  # Increment the count every time an RFID value is read

            if id == rfid_values[id_value]:
                print(f"Target RFID ({rfid_values[id_value]}) found after {count} reads!")
                GPIO.output(led, GPIO.HIGH)
                sleep(1)
                GPIO.output(led, GPIO.LOW)
                break

    except FileNotFoundError:
        print("Named pipe '/tmp/myfifo' not found. Make sure it's created by the C++ program.")

if __name__ == "__main__":
    main()

