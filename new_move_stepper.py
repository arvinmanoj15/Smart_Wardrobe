#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import threading

# Set up the GPIO pins
GPIO.setmode(GPIO.BOARD)
control_pins = [7, 11, 13, 15]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Step sequence for clockwise motion
cw_fullstep_seq = [
    [1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1],
    [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]
]

# Original counterclockwise sequence
ccw_fullstep_seq = [
    [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
    [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
]

# Variables to control the running of the motor
running = True
direction = "cw"
delay = 0.0005  # Adjusted delay for smoother operation
start_time = None
stop_time = None

# Function to run the motor
def run_motor():
    global start_time, stop_time, running
    start_time = time.time()
    while running:
        step_seq = cw_fullstep_seq if direction == "cw" else ccw_fullstep_seq
        for fullstep in step_seq:
            if not running:
                break
            for pin in range(4):
                GPIO.output(control_pins[pin], fullstep[pin])
            time.sleep(delay)
    stop_time = time.time()

# Function to read from the named pipe and control the motor
def read_pipe():
    global running, direction
    while True:
        with open("/tmp/motor_control_fifo", 'rb') as fifo_reader:
            command_bytes = fifo_reader.read()
            command = command_bytes.decode('utf-8').strip()
            if command == "STOP_AND_REVERSE":
                running = False
                break

# Start the motor and pipe reading in separate threads
motor_thread = threading.Thread(target=run_motor)
pipe_thread = threading.Thread(target=read_pipe)
motor_thread.start()
pipe_thread.start()

# Wait for both threads to finish
motor_thread.join()
pipe_thread.join()

# Calculate the time to run in the opposite direction
run_duration = stop_time - start_time if stop_time else 0

# Run motor in opposite direction for the same duration
if run_duration > 0:
    direction = "ccw" if direction == "cw" else "cw"
    running = True
    end_time = time.time() + run_duration
    while time.time() < end_time:
        step_seq = cw_fullstep_seq if direction == "cw" else ccw_fullstep_seq
        for fullstep in step_seq:
            for pin in range(4):
                GPIO.output(control_pins[pin], fullstep[pin])
            time.sleep(delay)

# Clean up GPIO
GPIO.cleanup()

