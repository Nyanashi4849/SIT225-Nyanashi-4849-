
import matplotlib
matplotlib.use('Agg')  
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

filename = "task.csv"  
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    print(f"Error: File '{filename}' not found. Check the path.")
    exit()
except Exception as e:
    print(f"Error reading CSV: {e}")
    print("Check if the file is open in another program or if the encoding is incorrect.")
    exit()


df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y%m%d%H%M%S', errors='coerce')

df.dropna(inplace=True)

df = df.set_index('Timestamp')

if df.empty:
    print("Error: DataFrame is empty after cleaning. Check your data and cleaning steps.")
    exit()

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df.index, df['Temperature'], label='Temperature (°C)', color='tab:red', marker='.', linestyle='-')  # Added markers

ax.plot(df.index, df['Humidity'], label='Humidity (%)', color='tab:blue', marker='.', linestyle='-')  # Added markers

ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Values', fontsize=12)
ax.set_title('Temperature and Humidity over Time', fontsize=14)
ax.legend(fontsize=10)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))  
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  
plt.xticks(rotation=45, ha='right', fontsize=10)

plt.tight_layout()

plt.savefig('temperature_humidity_plot.png')  
print(df.dtypes)
print(df.head())

print("\nAnalysis and Comments:")
