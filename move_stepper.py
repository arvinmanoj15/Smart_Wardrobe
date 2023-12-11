#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import threading

# Set up the GPIO pins
GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Step sequence for clockwise motion
cw_fullstep_seq = [
    [1,0,0,0],
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0]
]

# Generate counterclockwise sequence by reversing the clockwise sequence
ccw_fullstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

# Variable to control the running of the motor
running = True
direction = "ccw"  # Change to "ccw" for counterclockwise motion

# Function to run the motor
def run_motor():
    while running:
        step_seq = cw_fullstep_seq if direction == "cw" else ccw_fullstep_seq
        for fullstep in step_seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], fullstep[pin])
            #time.sleep(0.001)  # Adjusted delay for smoother operation
            time.sleep(0.00075) #0.0009 & 0.00075 for opposite

# Start the motor in a separate thread
motor_thread = threading.Thread(target=run_motor)
motor_thread.start()

# Wait for the user to press 'q'
input("Press 'q' to stop the motor...")
running = False

# Wait for the motor thread to finish
motor_thread.join()

# Clean up GPIO
GPIO.cleanup()

