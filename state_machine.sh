#!/bin/bash

# Define the states
STATE_1="Weather_Check"
STATE_2="Stepper_Run"
STATE_3="RFID_Reading"
STATE_4="ESP_Coms_LED"
STATE_5="FINAL"

# Initialize the current state
state=$STATE_1

# Create the named pipe
mkfifo /tmp/myfifo
mkfifo /tmp/motor_control_fifo

# Give write permission to all users
chmod a+w /tmp/myfifo
chmod a+w /tmp/motor_control_fifo

while true; do
    # Handle the current state
    case $state in
        $STATE_1)
            echo "In $state"
            ./weather &
            state=$STATE_2
            ;;
        $STATE_2)
            echo "In $state"
            ./new_move_stepper.py &
            state=$STATE_3
            ;;
        $STATE_3)
            echo "In $state"
            ./rfid_reader.py &
            sleep 5 # Sleeping for 2 sec (IMP: If the final writing to pipe not working try adjusting the Sleep time here!)
	    state=$STATE_4
            ;;
        $STATE_4)
            echo "In $state"
            ./esp_32_udp_coms.py
            state=$STATE_5
            ;;
        $STATE_5)
            echo "In $state"
            echo "Enter EXIT to exit or CONTINUE to continue:"
            read decision
            if [ "$decision" == "EXIT" ]; then
                echo "Exiting state machine..."
                exit 0
            elif [ "$decision" == "CONTINUE" ]; then
                state=$STATE_1  # loop back to the first state
            else
                echo "Invalid input. Exiting state machine..."
                exit 1
            fi
            ;;
        *)
            echo "Invalid state"
            break
            ;;
    esac
    sleep 1  # Sleep for 1 second after each state
done
