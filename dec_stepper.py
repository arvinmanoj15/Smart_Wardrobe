#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# GPIO pins
control_pins = [7, 11, 13, 15]

# Setup
GPIO.setmode(GPIO.BOARD)
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Sequence
seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def rotate_motor(direction, duration):
    step_count = len(seq)
    step_dir = 1 if direction == 'cw' else -1

    step_counter = 0
    end_time = time.time() + duration

    while time.time() < end_time:
        for pin in range(4):
            GPIO.output(control_pins[pin], seq[step_counter][pin])
        step_counter += step_dir

        # If we reach the end of the sequence
        # start again
        if (step_counter >= step_count):
            step_counter = 0
        if (step_counter < 0):
            step_counter = step_count - 1

        time.sleep(0.0009)  # Control rotation speed

try:
    rotate_motor('cw', 5)  # Rotate clockwise for 5 seconds
    rotate_motor('cw', 5) # Rotate counter-clockwise for 5 seconds
finally:
    GPIO.cleanup()  # Clean up GPIO on exit

