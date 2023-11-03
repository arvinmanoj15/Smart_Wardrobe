import socket
import random
import time

# Set the ESP32's IP address and port
esp32_ip = '10.0.0.17'  # ESP32's IP address
esp32_port = 12345  # Connection Port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Generate a random value between 0 and 3
        value = random.randint(0, 3)
        
        # Send the value to the ESP32
        message = str(value)
        sock.sendto(message.encode(), (esp32_ip, esp32_port))
        
        print(f"Sent value: {value}")
        
        # Wait for 5 seconds
        time.sleep(5)
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    sock.close()
