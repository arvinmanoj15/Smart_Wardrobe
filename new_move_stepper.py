#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Configure the Pi to use the BCM (Broadcom) pin names
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin numbers for the stepper motor
step_pin = 23  # Connect to STEP pin of A4988
dir_pin = 24   # Connect to DIR pin of A4988
enable_pin = 25 # Optional: Connect to ENABLE pin of A4988

# Set up the GPIO channels - one for input and one for output
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)

# Set the direction (High for clockwise, Low for counter-clockwise)
GPIO.output(dir_pin, GPIO.HIGH)  # Change to LOW for counter-clockwise

# Set the ENABLE pin to low (optional, if connected)
GPIO.output(enable_pin, GPIO.LOW) 

# Define the step delay to control the speed of the motor
step_delay = 0.001  # 1 millisecond, adjust to control the speed

# Perform the desired number of steps in a loop
for i in range(3000):  # Adjust the range for more or fewer steps
    # Trigger one step
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(step_delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(step_delay)

# Clean up GPIO on completion
GPIO.cleanup()

