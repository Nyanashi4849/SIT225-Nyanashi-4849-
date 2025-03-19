from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv("5.1PCSV.csv")  # Ensure file is correctly loaded

# Initialize Dash app
app = Dash(__name__)

# Track the current data window index
current_index = 0  # To be used in callbacks

# Layout
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard", style={'textAlign': 'center'}),

    # Dropdown for selecting graph type
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Histogram (Distribution)', 'value': 'histogram'}
        ],
        value='line'
    ),

    # Multi-Select Dropdown for choosing axes
    dcc.Dropdown(
        id='axis-selection',
        options=[{'label': col, 'value': col} for col in ['x', 'y', 'z']],
        value=['x', 'y', 'z'],
        multi=True
    ),

    # Input for number of samples
    dcc.Input(id="num-samples", type="number", value=100, step=10),

    # Previous and Next Buttons
    html.Div([
        html.Button("Previous", id="prev-btn", n_clicks=0),
        html.Button("Next", id="next-btn", n_clicks=0)
    ], style={'margin-bottom': '20px'}),

    # Graph output
    dcc.Graph(id='graph-output'),

    # Table to display statistical summary
    dash_table.DataTable(id='stats-table', style_table={'overflowX': 'auto'})
])

# Callback to update graph based on user input and navigation
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
    global current_index

    if not selected_axes:
        return px.line(title="Please select at least one axis"), [], []

    # Calculate new index based on button clicks
    max_index = len(df) - num_samples_state
    step = num_samples_state if num_samples_state else 100

    current_index = max(0, min(max_index, current_index + (next_clicks - prev_clicks) * step))

    # Filter data for display
    filtered_df = df.iloc[current_index: current_index + num_samples_state]

    # Melt DataFrame for multiple line plotting
    melted_df = filtered_df.melt(id_vars=['timestamp'], value_vars=selected_axes, var_name='axis', value_name='value')

    # Choose graph type
    if graph_type == 'line':
        fig = px.line(melted_df, x='timestamp', y='value', color='axis', title="Gyroscope Data")
    elif graph_type == 'scatter':
        fig = px.scatter(melted_df, x='timestamp', y='value', color='axis', title="Gyroscope Data")
    elif graph_type == 'histogram':
        fig = px.histogram(melted_df, x='value', color='axis', title="Gyroscope Data Distribution", nbins=30)

    # Calculate summary statistics
    stats_data = filtered_df[selected_axes].describe().reset_index().to_dict('records')
    stats_columns = [{"name": i, "id": i} for i in filtered_df[selected_axes].describe().reset_index().columns]

    return fig, stats_data, stats_columns

# Run app
if __name__ == '__main__':
    app.run(debug=True)
