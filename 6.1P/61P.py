# Import necessary libraries
from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.express as px
import pandas as pd

# Load the CSV file containing gyroscope data
df = pd.read_csv("5.1PCSV.csv") 

# Initialize Dash app
app = Dash(__name__)

# initialising the current data index to zero
current_index = 0  

# Define the layout of the dashboard how text should align in center
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard", style={'textAlign': 'center'}),

    # Dropdown for selecting graph type (Line, Scatter, Histogram) , so we can choose whatever graph we want 
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Histogram (Distribution)', 'value': 'histogram'}
        ],
        value='line'  # Default selection
    ),

    # Multi-select dropdown for choosing which axis to plot (x, y, z) on our graph
    dcc.Dropdown(
        id='axis-selection',
        options=[{'label': col, 'value': col} for col in ['x', 'y', 'z']],
        value=['x', 'y', 'z'],  # Default selection
        multi=True
    ),

    # Input for specifying the number of samples to display ata time
    dcc.Input(id="num-samples", type="number", value=100, step=10),

    # Previous and Next buttons for navigating through data 
    html.Div([
        html.Button("Previous", id="prev-btn", n_clicks=0),
        html.Button("Next", id="next-btn", n_clicks=0)
    ], style={'margin-bottom': '20px'}),

    # Graph output to display what we asked for
    dcc.Graph(id='graph-output'),

    # DataTable to show statistical summary of the selected data
    dash_table.DataTable(id='stats-table', style_table={'overflowX': 'auto'})
])

# Callback function to update graph and statistical table based on user inputs
@app.callback(
    [Output('graph-output', 'figure'),
     Output('stats-table', 'data'),
     Output('stats-table', 'columns')],
    [Input('graph-type', 'value'),
     Input('axis-selection', 'value'),
     Input('num-samples', 'value'),
     Input('prev-btn', 'n_clicks'),
     Input('next-btn', 'n_clicks')],
    [State('num-samples', 'value')]
)
def update_graph(graph_type, selected_axes, num_samples, prev_clicks, next_clicks, num_samples_state):
    global current_index  # Use global variable to track data window

    # Ensure at least one axis is selected
    if not selected_axes:
        return px.line(title="Please select at least one axis"), [], []

    # Define the maximum index to prevent out-of-bounds errors
    max_index = len(df) - num_samples_state
    step = num_samples_state if num_samples_state else 100  # Default step if None

    # Adjust the current index based on button clicks
    current_index = max(0, min(max_index, current_index + (next_clicks - prev_clicks) * step))

    # Extract a subset of data for display
    filtered_df = df.iloc[current_index: current_index + num_samples_state]

    # Transform data to long format for better visualization
    melted_df = filtered_df.melt(id_vars=['timestamp'], value_vars=selected_axes, var_name='axis', value_name='value')

    # Choose the appropriate graph type based on user selection
    if graph_type == 'line':
        fig = px.line(melted_df, x='timestamp', y='value', color='axis', title="Gyroscope Data")
    elif graph_type == 'scatter':
        fig = px.scatter(melted_df, x='timestamp', y='value', color='axis', title="Gyroscope Data")
    elif graph_type == 'histogram':
        fig = px.histogram(melted_df, x='value', color='axis', title="Gyroscope Data Distribution", nbins=30)

    # Compute summary statistics for selected axes
    stats_data = filtered_df[selected_axes].describe().reset_index().to_dict('records')
    stats_columns = [{"name": i, "id": i} for i in filtered_df[selected_axes].describe().reset_index().columns]

    return fig, stats_data, stats_columns  # Return updated graph and stats table

# Run the Dash app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
