import serial
import random


try:
    ser = serial.Serial('COM10', 9600)  
    print("Serial connection established.")
    
    while True:
        random_number = random.randint(1, 10)
        
        ser.write(str(random_number).encode())
        print(f" Sent: {random_number}")
        
        response = ser.readline().decode().strip()
        print(f" Received: {response}")
        
except serial.SerialException as e:
    print(f"Error: {e}")
    print("Make sure the serial port is not in use by another program.")
except Exception as e:
    print(f"An error occurred: {e}")
