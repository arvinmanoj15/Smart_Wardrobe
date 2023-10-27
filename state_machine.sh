#!/bin/bash

# Define the states
STATE_1="Dummy_State_1"
STATE_2="Dummy_State_2"
STATE_3="Dummy_State_3"
STATE_4="Dummy_State_4"
STATE_5="Dummy_State_5"
STATE_6="Dummy_State_6"
STATE_7="Dummy_State_7"
STATE_8="Dummy_State_8"
STATE_9="Dummy_State_9"
STATE_10="Dummy_State_10"

# Initialize the current state
state=$STATE_1

while true; do
    # Handle the current state
    case $state in
        $STATE_1)
            echo "In $state"
            state=$STATE_2
            ;;
        $STATE_2)
            echo "In $state"
            state=$STATE_3
            ;;
        $STATE_3)
            echo "In $state"
            state=$STATE_4
            ;;
        $STATE_4)
            echo "In $state"
            state=$STATE_5
            ;;
        $STATE_5)
            echo "In $state"
            state=$STATE_6
            ;;
        $STATE_6)
            echo "In $state"
            state=$STATE_7
            ;;
        $STATE_7)
            echo "In $state"
            state=$STATE_8
            ;;
        $STATE_8)
            echo "In $state"
            state=$STATE_9
            ;;
        $STATE_9)
            echo "In $state"
            state=$STATE_10
            ;;
        $STATE_10)
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
