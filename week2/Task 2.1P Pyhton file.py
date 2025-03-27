 # Import serial communication library, time module for handling time-based operations,  CSV module for logging data, regular expressions for extracting numeric values
import serial 
import time  
import csv  
import re 

# Open serial connection  on COM10 having  baud rate 9600
# Timeout set to 1 second to prevent blocking reads
ser = serial.Serial('COM10', 9600, timeout=1)

# Define the filename of csv file
filename = "2.csv"

def extract_numeric_value(text):

    try:
            # Find the first number in the text
        match = re.search(r"[-+]?\d*\.\d+|\d+", str(text))  
        if match:
            # Convert matched value to float
            return float(match.group(0))  
             # Handle  exceptions that might occur due to error
    except (TypeError, ValueError, AttributeError): 
          # Return None if extraction fails
        return None

# Open the CSV file 
with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)  # Create CSV writer object

    # If the file is empty, it writes the header row
    if file.tell() == 0:
         # Write column headers in csv
        writer.writerow(["Timestamp", "Temperature", "Humidity"]) 

    # Start the data collection process by recording the start time first
    start_time = time.time() 
    while time.time() - start_time <= 30 * 60:  # takes the reading for 30 minutes
        line = ser.readline().decode('utf-8').strip()  # Read and decode incoming data
        
        # If data is received
        if line:  
            try:
                # Generate a timestamp in YYYY/MM/DD/HH/MM/SS format
                timestamp = time.strftime("%Y%m%d%H%M%S")

                # Split the received data by commas 
                parts = line.split(',') 

                # Extract numeric values for temperature and humidity
                temp = extract_numeric_value(parts[0])  # gets temperature
                hum = extract_numeric_value(parts[1]) if len(parts) > 1 else None  # gets humidity

                # If both values are right and valid then write them to the CSV file
                if temp is not None and hum is not None: 
                    writer.writerow([timestamp, temp, hum])  # Save data
                    print(f"{timestamp},{temp},{hum}")  # Print data on terminal
                
                time.sleep(10)  # Wait 10 seconds before reading the next data point

            except (ValueError, IndexError) as e:
                print(f"Error processing data: {line} - {e}")  # Handle data processing errors
        else:
            print("Getting data.")  # if data is not being read then prints get data
            time.sleep(1)  # Wait 1 sec before checking for data again

# Close the serial connection after data collection ends.
ser.close()
# Confirms that data is saved in csv
print(f"Data saved to {filename}")  
