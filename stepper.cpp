#include <wiringPi.h>
#include <iostream>

// Define the GPIO pins connected to the L298N motor driver
const int IN1 = 17; // Connect to L298N IN1
const int IN2 = 18; // Connect to L298N IN2
const int IN3 = 27; // Connect to L298N IN3
const int IN4 = 22; // Connect to L298N IN4

// Define the delay between steps (adjust as needed for your motor)
const int stepDelayMicros = 2000; // 2000 microseconds = 2 milliseconds

// Define the sequence of steps for the stepper motor
const int stepSequence[8][4] = {
    {1, 0, 0, 1}, // Step 1
    {1, 0, 0, 0}, // Step 2
    {1, 1, 0, 0}, // Step 3
    {0, 1, 0, 0}, // Step 4
    {0, 1, 1, 0}, // Step 5
    {0, 0, 1, 0}, // Step 6
    {0, 0, 1, 1}, // Step 7
    {0, 0, 0, 1}  // Step 8
};

void stepMotor(int stepNumber) {
    for (int pin = 0; pin < 4; ++pin) {
        digitalWrite(IN1 + pin, stepSequence[stepNumber][pin]);
    }
    delayMicroseconds(stepDelayMicros);
}

int main() {
    if (wiringPiSetupGpio() == -1) {
        std::cerr << "Error: Unable to initialize wiringPi." << std::endl;
        return 1;
    }

    // Set GPIO pins as outputs
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    // Move the stepper motor in one direction (e.g., clockwise)
    for (int i = 0; i < 512; ++i) { // 512 steps for one complete rotation
        for (int step = 0; step < 8; ++step) {
            stepMotor(step);
        }
    }

    // Turn off all motor driver inputs
    for (int pin = IN1; pin <= IN4; ++pin) {
        digitalWrite(pin, 0);
    }

    return 0;
}
