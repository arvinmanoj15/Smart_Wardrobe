#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import sys
from time import sleep

# Define GPIO pins
LED_PIN = 40

RFID_VALUES = [
    769133311166,  # Heavy Sweater
    769133311166,  # RFID value for 0-5°C
    769133311166,  # RFID value for 5-10°C
    769133311166,  # RFID value for 10-15°C
    837695175900,  # RFID value for 15-20°C
    837695175911,  # RFID value for 20-25°C
    837695175922,  # RFID value for 25-30°C
    837695175933   # RFID value for above 30°C
]

# Setup GPIO
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

# Cleanup GPIO
def cleanup_gpio(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup_gpio)
signal.signal(signal.SIGTERM, cleanup_gpio)

def main():
    setup_gpio()
    reader = SimpleMFRC522()
    count = 0
    id_value = None
    temp_id_value = None

    try:
        # Open the named pipe for reading
        with open("/tmp/myfifo", 'rb') as fifo_reader:
            while True:
                try:
                    rfid_value_bytes = fifo_reader.read()
                    id_value = int.from_bytes(rfid_value_bytes, byteorder='little', signed=True)
                    print("Received RFID Value ID:", id_value)
                    # Close the named pipe after successful read
                    # fifo_reader.close()
                    break

                except Exception as e:
                    print(f"An error occurred: {e}")
                    cleanup_gpio(None, None)

        # Create a new loop for RFID reading and LED control
        while True:
            # print("I'm going to read")
            id, _ = reader.read()
            # print("I'm trying to READ")

            if id != temp_id_value:
                temp_id_value = id
                print(id)
                count += 1

            if id == RFID_VALUES[id_value]:
                print(f"Target RFID ({RFID_VALUES[id_value]}) found after {count} reads!")
                GPIO.output(LED_PIN, GPIO.HIGH)
                sleep(1)
                GPIO.output(LED_PIN, GPIO.LOW)
                
                with open("/tmp/motor_control_fifo", 'wb') as fifo_writer:
                    command = "STOP_AND_REVERSE"
                    fifo_writer.write(command.encode('utf-8'))
                    print("Sent STOP_AND_REVERSE command to the motor control program")
                break

        # Open the named pipe for writing and send the count value
        print("Trying to open the pipe")
        with open("/tmp/myfifo", 'wb') as fifo_writer:
            count_bytes = count.to_bytes(4, byteorder='little', signed=True)
            fifo_writer.write(count_bytes)
            print(f"Sent count ({count}) to the named pipe.")

    except FileNotFoundError:
        print("Named pipe '/tmp/myfifo' not found. Make sure it's created by the C++ program.")

if __name__ == "__main__":
    main()

