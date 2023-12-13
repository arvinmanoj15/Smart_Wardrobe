# Smart_Wardrobe

## About
Smart_Wardrobe is an innovative wardrobe management system that suggests clothing based on weather conditions, integrating technologies like weather APIs, RFID, linear motor systems, and ESP32.

## Features
- Weather-Based Clothing Suggestions
- Automated Wardrobe Tracking with RFID
- LED Indicators controlled by ESP32
- Stepper Motor Control for wardrobe management
- State Machine Workflow for component coordination

## Components
1. **Weather.cpp:** Fetches weather data and suggests clothing.
2. **Statemachine.sh:** Manages the system's workflow.
3. **RFID_reader.py:** Reads RFID tags and controls an LED indicator.
4. **Esp32_coms.py:** ESP32 communication for LED control.
5. **new_move_stepper.py:** Stepper motor control.

## Installation & Usage
- Connect the RFID reader and Stepper motor to the system.
- Run the `Statemachine.sh` script to start the system.
