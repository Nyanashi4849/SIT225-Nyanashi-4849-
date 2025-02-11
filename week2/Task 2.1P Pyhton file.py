
import serial
import time
import csv
import re  

ser = serial.Serial('COM10', 9600, timeout=1)  
filename = "2.csv"

def extract_numeric_value(text):
    try:
        match = re.search(r"[-+]?\d*\.\d+|\d+", str(text))  
        if match:
            return float(match.group(0))  
    except (TypeError, ValueError, AttributeError):  
        return None


with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Temperature", "Humidity"])

    start_time = time.time()
    while time.time() - start_time <= 30 * 60:  
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                timestamp = time.strftime("%Y%m%d%H%M%S")
                parts = line.split(',') 
                temp = extract_numeric_value(parts[0])  
                hum = extract_numeric_value(parts[1]) if len(parts) > 1 else None 

                if temp is not None and hum is not None: 
                  writer.writerow([timestamp, temp, hum])
                  print(f"{timestamp},{temp},{hum}")
                
                time.sleep(10)
            except (ValueError, IndexError) as e:
                print(f"Error processing data: {line} - {e}")
        else:
            print("Getting data.")
            time.sleep(1)

ser.close()
print(f"Data saved to {filename}")
