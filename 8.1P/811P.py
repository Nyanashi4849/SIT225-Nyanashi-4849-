import sys
import time
import traceback
import os
from arduino_iot_cloud import ArduinoCloudClient
import csv

DEVICE_ID = "d292d609-626a-4200-809c-fc67df5ab96a"
SECRET_KEY = "mF0Fef8w14qNRB1tsB3YRPGtt"

# Define the variables to store the accelerometer data
cur_data = []
temp_data = []
x, y, z = 0, 0, 0
count = 0
N_SAMPLES = 20

# =============================================================================
# Define the callback function for accelerometer_x changes
def on_accelerometer_x_changed(client, value):
    global x
    x = value

# Define the callback function for accelerometer_y changes
def on_accelerometer_y_changed(client, value):
    global y
    y = value

# Define the callback function for accelerometer_z changes
def on_accelerometer_z_changed(client, value):
    global z
    z = value
            
#================================= MAIN FUNCTION =================================
if __name__ == "__main__":
    try:
        # Instantiate Arduino cloud client
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode = True)
        
        # Register the callback functions
        client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
        client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
        client.register("py_z", value=None, on_write=on_accelerometer_z_changed)

        client.start()

        # Keep the client running
        while True:
            if x is not None and y is not None and z is not None:
                if count < N_SAMPLES:
                    count += 1
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    temp_data.append([count,timestamp,x,y,z])
                    print([count,timestamp,x,y,z])
                    x, y, z = None, None, None
                else:
                    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
                    df = pd.DataFrame(temp_data, columns=['index','Timestamp', 'X', 'Y', 'Z'])
                    df.to_csv(f"csv_{timestamp}.csv")
                    fig = px.line(df, x= 'Timestamp', y = ['X','Y','Z'])  # Scatter plot
                    filename = f"images/plot_{timestamp}.png"  # Correct filename format
                    pio.write_image(fig, filename)
                    count = 0
                    cur_data = temp_data.copy()
                    temp_data.clear()
            client.update()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)


        app.run_server(debug_mode = True, jupyter_tab = True)

        _df = pd.read_csv("811P.csv")
_df.drop(columns ={"Unnamed: 0", "index"}, inplace = True)
_df.Timestamp = pd.to_datetime(_df.Timestamp)
_df.set_index("Timestamp", inplace = True)

act_1 = _df.between_time("01:15:40", "01:16:30")
act_2 = _df.between_time("01:16:50", "01:18:30")
act_3 = _df.between_time("01:21:10", "01:22:40")
act_4 = _df.between_time("01:24:45", "01:25:15")
act_5 = _df.between_time("01:30:00", "01:30:40")

act_1.info()

figsize = (16,9)
sns.lineplot(x=_df.index, y=_df["X"], label="X")
sns.lineplot(x=_df.index, y=_df["Y"], label="Y")
sns.lineplot(x=_df.index, y=-df["Z"], label="Z")

fig, ax = plt.subplots(5, figsize = (10,9))

for i, data in enumerate([act_1,act_2,act_3,act_4,act_5]):
    sns.lineplot(x=data.index, y=data["X"], label="X", ax = ax[i])
    sns.lineplot(x=data.index, y=data["Y"], label="Y", ax = ax[i])
    sns.lineplot(x=data.index, y=data["Z"], label="Z", ax = ax[i])
    ax[i].legend()

plt.tight_layout()
plt.show()

act_1.describe()
act_2.describe()