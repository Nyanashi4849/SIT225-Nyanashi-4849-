
# imprt necessary libraries
# Bokeh imports for interactive visualization. curdloc is used to add the layout to the current document.
from bokeh.io import curdoc

# Bokeh imports for creating interactive widgets and layout management.
from bokeh.models import ColumnDataSource, Select, MultiSelect, Slider, Button
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter

# pandas for data manipulation and analysis.
import pandas as pd

# numpy for numerical operations, specifically for histogram calculations.
from numpy import histogram

# Load data  from CSV file
# The CSV file is expected to have a header row with the following columns: timestamp, x, y, z.
df = pd.read_csv("5.2D.csv", names=["timestamp", "x", "y", "z"])

# Parse timestamps properly to ensure they are in datetime format.
# This is crucial for time series data visualization.
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# Remove any rows with invalid timestamps 
df = df.dropna(subset=["timestamp"])

# Data source so that Bokeh can update the plot and table dynamically.
# The data source is a dictionary where keys are column names and values are lists of data.
source = ColumnDataSource(data=df)

# Widgets for user interaction. widgets like dropdowns, sliders, and buttons and control the number of samples displayed.
# Select widget for choosing the type of graph to display.
graph_type_select = Select(title="Graph Type", value="Line Chart",
                           options=["Line Chart", "Scatter Plot", "Distribution Plot", "Histogram"])

variable_select = MultiSelect(title="Select Data Variables",
                              options=["x", "y", "z"],
                              value=["x", "y", "z"])

sample_slider = Slider(title="Number of Samples to Display", start=1, end=len(df), value=100, step=1)

# Button widgets for navigating through the data samples.
# These buttons allow the user to move back and forth through the data samples.
prev_button = Button(label="⬅ Previous")
next_button = Button(label="Next ➡")

# State variable to keep track of the current index in the data.
# This is used to determine which subset of data to display based on the slider value.
start_index = 0

# Data table to display the current subset of data.
# This table will show the x, y, and z values for the current selection of data samples.
columns = [TableColumn(field=col, title=col, formatter=NumberFormatter(format="0.0000")) for col in ["x", "y", "z"]]
data_table = DataTable(source=source, columns=columns, width=600, height=200)

# Plot initialization
# The plot is created using Bokeh's figure function, which allows for interactive plotting.
plot = figure(title="Sensor Data", x_axis_label="Timestamp", y_axis_label="Value", width=800, height=400)

# Predefined color palette for different variables.
# This is used to differentiate between the different variables in the plot. like different colours for x, y, and z.
color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

# Update functions to refresh the data and plot based on user input.
def update_data():
    global start_index
    end_index = start_index + sample_slider.value
    sub_df = df.iloc[start_index:end_index]
    source.data = sub_df.to_dict("list")
    update_plot(sub_df)

# This function updates the plot based on the selected graph type and variables.
# It clears the previous values and redraws the plot with the new data.
def update_plot(sub_df):
    plot.renderers.clear()
    plot.title.text = f"{graph_type_select.value} Visualization"
    variables = variable_select.value

    if not variables:
        return
#   This loop goes through the selected variables and plots them on the graph.
    for i, var in enumerate(variables):
        color = color_palette[i % len(color_palette)]

        # if loop- if line graph type is selected, it will plot the line graph.
        if graph_type_select.value == "Line Chart":
            plot.line(sub_df["timestamp"], sub_df[var], legend_label=var, line_width=2, color=color)

        # eleif loop- if scatter graph type is selected, it will plot the scatter graph.
        elif graph_type_select.value == "Scatter Plot":
            plot.circle(sub_df["timestamp"], sub_df[var], legend_label=var, size=7, color=color)

            # elif loop- if distribution graph type is selected, it will plot the distribution graph.
        elif graph_type_select.value in ["Distribution Plot", "Histogram"]:
            hist, edges = histogram(sub_df[var], bins=20)
            plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=0.5, legend_label=var, color=color)
            
# if varialbes is not empty, it will hide the legend when clicked
    if variables:
        plot.legend.click_policy = "hide"

# Button callbacks for navigating through the data samples.
# These functions are called when the user clicks the "Previous" or "Next" buttons.
def prev_callback():
    global start_index
    start_index = max(0, start_index - sample_slider.value)
    update_data()

def next_callback():
    global start_index
    start_index = min(len(df) - sample_slider.value, start_index + sample_slider.value)
    update_data()

# Widget callbacks for updating the data and plot when the user interacts with the widgets.
# This function is called when the user changes the graph type or selected variables.   
def widget_callback(attr, old, new):
    update_data()

# Attach callbacks to widgets and buttons.
# These callbacks will trigger the update functions when the user interacts with the widgets.
graph_type_select.on_change("value", widget_callback)
variable_select.on_change("value", widget_callback)
sample_slider.on_change("value", widget_callback)
prev_button.on_click(prev_callback)
next_button.on_click(next_callback)

# Layout the widgets and plot in a column format.
# The layout is organized in a way that the widgets are at the top, followed by the plot and data table.
layout = column(
    row(graph_type_select, variable_select),
    row(sample_slider, prev_button, next_button),
    plot,
    data_table
)

# Add to Bokeh doc and set the title.
curdoc().add_root(layout)
curdoc().title = "Bokeh Sensor Dashboard"

# Initial display of data and plot.
update_data()
