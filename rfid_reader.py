#!/usr/bin/env python3

from mfrc522 import SimpleMFRC522
import signal

# Register signal handlers
def cleanup_gpio(signal, frame):
    exit(0)

signal.signal(signal.SIGINT, cleanup_gpio)
signal.signal(signal.SIGTERM, cleanup_gpio)

# Define the RFID value to search for
target_rfid = 837695175856

def main():
    reader = SimpleMFRC522()
    count = 0  # Initialize a count variable
    
    while True:
        try:
            id, _ = reader.read()
            print(id)
            count += 1  # Increment the count every time an RFID value is read

            if id == target_rfid:
                print(f"Target RFID ({target_rfid}) found after {count} reads!")
                break  # Exit the loop when the target RFID is found

        except Exception as e:
            print(f"An error occurred: {e}")
            cleanup_gpio(None, None)

if __name__ == "__main__":
    main()

