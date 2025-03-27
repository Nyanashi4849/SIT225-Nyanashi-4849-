import serial  # Import the serial 
import random  # Import the random module to generate random numbers

try:
    # Establish a serial connection on port COM10
    ser = serial.Serial('COM10', 9600, timeout=1)  
    print("Serial connection established.")
    
    while True:
        # Generate a random number between 1 and 10
        random_number = random.randint(1, 10)
        
        # Send the random number as a string and prints the numbers
        ser.write(str(random_number).encode())
        print(f"Sent: {random_number}")
        
        # Read response from Arduino and decode it
        response = ser.readline().decode().strip()
        
        # Check if response is received or not
        if response:
            print(f"Received: {response}")
        else:
            print("No response received.")
# checks if there is  any error or not. if there is errorit pritns messages according to the types of error that has occured.
except serial.SerialException as e:
    print(f"Error: {e}")
    print("Make sure the serial port is not in use by another program.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure serial port is closed when script exits
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")

