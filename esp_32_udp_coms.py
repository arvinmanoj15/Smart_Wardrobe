import socket
import os

# Set the ESP32's IP address and port
esp32_ip = '10.0.0.17'  # ESP32's IP address
esp32_port = 12345  # Connection Port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open the named pipe for reading
fifo_path = '/tmp/myfifo'  # Replace with the appropriate path

try:
    with open(fifo_path, 'rb') as fifo_reader:
        # Read the value from the named pipe
        value_bytes = fifo_reader.read()
        value = int.from_bytes(value_bytes, byteorder='little', signed=True)
        
        # Send the value to the ESP32
        message = str(value)
        sock.sendto(message.encode(), (esp32_ip, esp32_port))
        
        print(f"Sent value: {value} to {esp32_ip}:{esp32_port}")
except FileNotFoundError:
    print("Named pipe '/tmp/myfifo' not found. Make sure it's created by the C++ program.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sock.close()

