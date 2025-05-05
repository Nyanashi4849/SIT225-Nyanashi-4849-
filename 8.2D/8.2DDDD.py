import sys
import time
import traceback
import os
import csv
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, callback_context
from arduino_iot_client import ArduinoIoTClient
from threading import Thread, Lock
from datetime import datetime
import cv2
import base64
from io import BytesIO
from PIL import Image
import glob
import atexit
import random

# Arduino IoT credentials
DEVICE_ID = "d046d841-f427-46fc-80de-48f1fea947c1"
SECRET_KEY = " q?3fKYL#IO@krDMRNluagQzrA"

# Configuration
ACTIVITY_DURATION = (15, 20)  # 15-20 seconds per activity
ACTIVITIES = {
    0: "no-activity",
    1: "waving",
    2: "shaking"
}

# Global variables with thread-safe locks
data_lock = Lock()
cur_data = []  # Stores recent accelerometer readings
all_data = []  # Stores all collected data
sequence_number = 1
last_capture_time = time.time()
is_running = True
current_activity = 0  # Default to no-activity
x, y, z = None, None, None  # Accelerometer values
activity_start_time = time.time()
current_activity_duration = random.randint(*ACTIVITY_DURATION)

# Create directories
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Webcam setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    sys.exit(1)

# Initialize annotations file
if not os.path.exists('annotations.csv'):
    with open('annotations.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'activity'])

# Arduino Cloud callbacks
def on_accelerometer_x_changed(client, value):
    global x
    x = value

def on_accelerometer_y_changed(client, value):
    global y
    y = value

def on_accelerometer_z_changed(client, value):
    global z
    z = value

def start_data_stream():
    global cur_data, all_data, x, y, z, is_running

    try:
        client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
        client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
        client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
        client.register("py_z", value=None, on_write=on_accelerometer_z_changed)
        client.start()

        while is_running:
            if x is not None and y is not None and z is not None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                data_point = [timestamp, x, y, z]
                
                with data_lock:
                    cur_data.append(data_point)
                    all_data.append(data_point)
                    
                    if len(cur_data) > 50:
                        cur_data.pop(0)
                
                x, y, z = None, None, None

            client.update()

    except Exception as e:
        print("Error in data stream:")
        traceback.print_exc()

def capture_and_save_data():
    global all_data, sequence_number, last_capture_time, current_activity
    global activity_start_time, current_activity_duration
    
    while is_running:
        current_time = time.time()
        
        # Check if it's time to switch activities
        if current_time - activity_start_time >= current_activity_duration:
            current_activity = random.choice(list(ACTIVITIES.keys()))
            activity_start_time = current_time
            current_activity_duration = random.randint(*ACTIVITY_DURATION)
            print(f"Switched to activity: {ACTIVITIES[current_activity]} for {current_activity_duration} seconds")
        
        # Save data every second
        if current_time - last_capture_time >= 1 and is_running:
            last_capture_time = current_time
            
            if not all_data:
                continue
                
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename_base = f"{sequence_number}_{timestamp}"
            
            # Save accelerometer data
            csv_filename = f"data/{filename_base}.csv"
            try:
                with open(csv_filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
                    writer.writerows(all_data)
            except Exception as e:
                print(f"Error saving CSV: {e}")
                continue
            
            # Capture and save image
            ret, frame = cap.read()
            if ret:
                img_filename = f"images/{filename_base}.jpg"
                try:
                    cv2.imwrite(img_filename, frame)
                    
                    # Add to annotation data
                    with data_lock:
                        with open('annotations.csv', 'a', newline='') as ann_file:
                            writer = csv.writer(ann_file)
                            writer.writerow([filename_base, current_activity])
                except Exception as e:
                    print(f"Error saving image or annotation: {e}")
            
            # Reset for next interval
            with data_lock:
                all_data = []
                sequence_number += 1

        time.sleep(0.1)

# Cleanup function
def cleanup_on_exit():
    global is_running, all_data, sequence_number, current_activity
    if is_running:
        print("Performing cleanup before exit...")
        with open('annotations.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for data in all_data:
                writer.writerow([f"{sequence_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}", current_activity])
        cap.release()
        cv2.destroyAllWindows()

atexit.register(cleanup_on_exit)

# Dash app setup
app = Dash(_name_)

app.layout = html.Div([
    html.H1("Activity Data Collection (15-20 sec per activity)"),
    html.Div([
        html.Div(id='current-activity', style={'fontSize': 24, 'margin': '20px', 'fontWeight': 'bold'}),
        html.Div(id='activity-timer', style={'fontSize': 20, 'margin': '10px'}),
        html.Button("No Activity", id="btn-no-activity", n_clicks=0, style={'margin': '10px', 'padding': '10px'}),
        html.Button("Waving", id="btn-activity-1", n_clicks=0, style={'margin': '10px', 'padding': '10px'}),
        html.Button("Shaking", id="btn-activity-2", n_clicks=0, style={'margin': '10px', 'padding': '10px'}),
        html.Button("STOP Collection", id="btn-stop", n_clicks=0, 
                   style={'margin': '10px', 'padding': '10px', 'background': 'red', 'color': 'white'})
    ], style={'margin': '20px'}),
    dcc.Graph(id='live-graph', style={'height': '400px'}),
    html.Img(id='activity-image', style={'height': '400px', 'margin': '20px', 'border': '1px solid black'}),
    dcc.Interval(id='interval-component', interval=1000),
    html.Div(id='status-message', style={'margin': '20px', 'color': 'blue'})
])

# Main callback
@app.callback(
    [Output('live-graph', 'figure'),
     Output('activity-image', 'src'),
     Output('current-activity', 'children'),
     Output('activity-timer', 'children'),
     Output('status-message', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    global cur_data, activity_start_time, current_activity_duration
    
    time_remaining = max(0, current_activity_duration - (time.time() - activity_start_time))
    timer_msg = f"Activity timer: {time_remaining:.1f}s remaining"
    status_msg = f"Collecting: {ACTIVITIES[current_activity]}"
    
    # Create graph from current data
    with data_lock:
        if not cur_data:
            return go.Figure(), "", f"Current Activity: {ACTIVITIES[current_activity]}", timer_msg, status_msg
        
        timestamps = [d[0] for d in cur_data]
        x_values = [d[1] for d in cur_data]
        y_values = [d[2] for d in cur_data]
        z_values = [d[3] for d in cur_data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps, 
            y=x_values, 
            mode='lines+markers', 
            name='X'
        ))
        fig.add_trace(go.Scatter(
            x=timestamps, 
            y=y_values, 
            mode='lines+markers', 
            name='Y'
        ))
        fig.add_trace(go.Scatter(
            x=timestamps, 
            y=z_values, 
            mode='lines+markers', 
            name='Z'
        ))
        
        fig.update_layout(
            title=f'Live Accelerometer Data - {ACTIVITIES[current_activity]}',
            xaxis_title='Timestamp',
            yaxis_title='Acceleration (m/s²)',
            margin=dict(l=40, r=20, t=60, b=40),
            height=400
        )
    
    # Get latest image
    img_src = ""
    if sequence_number > 1:
        try:
            latest_img = f"images/{sequence_number-1}_*.jpg"
            img_files = sorted(glob.glob(latest_img))
            if img_files:
                with open(img_files[-1], 'rb') as f:
                    img = Image.open(f)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    img_src = f"data:image/jpeg;base64,{img_str}"
                    status_msg = f"Last saved: {os.path.basename(img_files[-1])}"
        except Exception as e:
            print(f"Error loading image: {e}")
    
    return fig, img_src, f"Current Activity: {ACTIVITIES[current_activity]}", timer_msg, status_msg

# Activity buttons callback
@app.callback(
    [Output('btn-no-activity', 'n_clicks'),
     Output('btn-activity-1', 'n_clicks'),
     Output('btn-activity-2', 'n_clicks')],
    [Input('btn-no-activity', 'n_clicks'),
     Input('btn-activity-1', 'n_clicks'),
     Input('btn-activity-2', 'n_clicks')]
)
def update_activity_buttons(btn1, btn2, btn3):
    global current_activity, activity_start_time, current_activity_duration
    
    ctx = callback_context
    if not ctx.triggered:
        return [0, 0, 0]
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-no-activity':
        current_activity = 0
    elif button_id == 'btn-activity-1':
        current_activity = 1
    elif button_id == 'btn-activity-2':
        current_activity = 2
    
    # Reset timer when manually changing activity
    activity_start_time = time.time()
    current_activity_duration = random.randint(*ACTIVITY_DURATION)
    
    return [0, 0, 0]

# Stop button callback
@app.callback(
    Output('interval-component', 'disabled'),
    [Input('btn-stop', 'n_clicks')]
)
def stop_collection(n_clicks):
    global is_running
    
    if n_clicks > 0:
        is_running = False
        with data_lock:
            cap.release()
            cv2.destroyAllWindows()
            print("Data collection stopped. Annotations saved to annotations.csv")
        return True
    
    return False

if __name__ == "__main__":
    # Start data collection threads
    data_thread = Thread(target=start_data_stream)
    data_thread.daemon = True
    data_thread.start()

    capture_thread = Thread(target=capture_and_save_data)
    capture_thread.daemon = True
    capture_thread.start()

    print(f"""
    =============================================
    Activity Data Collection Started

    Features:
    - Each activity lasts 15-20 seconds
    - Activities: No activity, Waving, Shaking
    - Data saved every second
    - CSV files in: data/
    - Images in: images/
    - Annotations in: annotations.csv

    Dashboard: http://127.0.0.1:8050
    =============================================
    """)
    
    # Run Dash app
    app.run_server(debug=True, port=8050)

