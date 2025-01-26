import serial
import time
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from collections import deque
import numpy as np
import requests
import geocoder

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)  # Check available ports




# Set up serial communication
arduino_port = 'COM5'  # Replace with your Arduino COM port
baud_rate = 9600

# Initialize serial connection
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port {arduino_port}: {e}")
    print("Please check if the correct port is selected and if you have permission to access it")
    exit(1)

# Create a Dash app
app = dash.Dash(__name__)

# Create fixed-length deques for data storage
MAX_POINTS = 1000
time_data = deque(maxlen=MAX_POINTS)
amplitude_data = deque(maxlen=MAX_POINTS)
frequency_data = deque(maxlen=MAX_POINTS)
coordinates_data = deque(maxlen=MAX_POINTS)
adc_data = deque(maxlen=MAX_POINTS)

# Initialize with some empty data
initial_time = time.time()
for i in range(MAX_POINTS):
    time_data.append(initial_time - (MAX_POINTS - i) * 0.1)
    amplitude_data.append(None)
    frequency_data.append(None)
    coordinates_data.append(None)
    adc_data.append(None)

# Enhanced graph layouts
frequency_layout = {
    'title': {
        'text': 'Frequency Over Time',
        'font': {'size': 24}
    },
    'xaxis': {
        'title': 'Time (seconds)',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': 'lightgray',
        'showline': True,
        'zeroline': False,
        'type': 'date'
    },
    'yaxis': {
        'title': 'Frequency (Hz)',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': 'lightgray',
        'showline': True,
        'zeroline': True,
        'zerolinecolor': 'gray',
        'zerolinewidth': 2,
        'autorange': True
    },
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
    'plot_bgcolor': '#f8f9fa',
    'paper_bgcolor': '#ffffff',
    'showlegend': True,
    'hovermode': 'x unified'
}

amplitude_layout = {
    'title': {
        'text': 'Amplitude Over Time',
        'font': {'size': 24}
    },
    'xaxis': {
        'title': 'Time (seconds)',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': 'lightgray',
        'showline': True,
        'zeroline': False,
        'type': 'date'
    },
    'yaxis': {
        'title': 'Amplitude (V)',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': 'lightgray',
        'showline': True,
        'zeroline': True,
        'zerolinecolor': 'gray',
        'zerolinewidth': 2,
        'autorange': True
    },
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
    'plot_bgcolor': '#f8f9fa',
    'paper_bgcolor': '#ffffff',
    'showlegend': True,
    'hovermode': 'x unified'
}

# Create initial figures with enhanced traces
fig_frequency = go.Figure(layout=frequency_layout)
fig_amplitude = go.Figure(layout=amplitude_layout)

# Add traces with different colors and names
fig_frequency.add_trace(go.Scatter(
    x=list(time_data),
    y=list(frequency_data),
    mode='lines+markers',
    name='Frequency',
    line={
        'width': 3,
        'shape': 'spline',
        'color': '#ee5253'
    },
    marker={
        'size': 8,
        'symbol': 'circle',
        'color': '#ee5253'
    },
    connectgaps=True,
    fill='tozeroy',
    fillcolor='rgba(238, 82, 83, 0.2)'
))

fig_amplitude.add_trace(go.Scatter(
    x=list(time_data),
    y=list(amplitude_data),
    mode='lines+markers',
    name='Amplitude',
    line={
        'width': 3,
        'shape': 'spline',
        'color': '#2e86de'
    },
    marker={
        'size': 8,
        'symbol': 'circle',
        'color': '#2e86de'
    },
    connectgaps=True,
    fill='tozeroy',
    fillcolor='rgba(46, 134, 222, 0.2)'
))

# Layout of the Dash app with side panel
app.layout = html.Div([
    html.H2('Real-Time Sensor Data Visualization', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'padding': '20px'}),
    
    # Main container with flexbox
    html.Div([
        # Graphs container
        html.Div([
            dcc.Graph(id='frequency-graph', 
                     figure=fig_frequency,
                     style={'height': '400px'}),
            dcc.Graph(id='amplitude-graph', 
                     figure=fig_amplitude,
                     style={'height': '400px'}),
        ], style={'width': '75%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        # Side panel
        html.Div([
            html.Div([
                html.H3('Real-Time Values', style={'textAlign': 'center', 'color': '#2c3e50'}),
                
                # Current Values Display
                html.Div([
                    html.Div([
                        html.H4('ADC Value:', style={'color': '#2c3e50', 'margin': '10px 0'}),
                        html.Div(id='adc-value', style={'fontSize': '24px', 'color': '#27ae60'})
                    ]),
                    html.Div([
                        html.H4('Frequency:', style={'color': '#2c3e50', 'margin': '10px 0'}),
                        html.Div(id='frequency-value', style={'fontSize': '24px', 'color': '#ee5253'})
                    ]),
                    html.Div([
                        html.H4('Amplitude:', style={'color': '#2c3e50', 'margin': '10px 0'}),
                        html.Div(id='amplitude-value', style={'fontSize': '24px', 'color': '#2e86de'})
                    ]),
                    html.Hr(),
                    html.H4('Operation Status:', style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.Div(id='status-display', style={'fontSize': '18px', 'color': '#2c3e50'}),
                    html.Hr(),
                    html.H4('Coordinates:', style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.Div(id='coordinates-display', style={'fontSize': '18px', 'color': '#2c3e50'})
                ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
            ], style={'position': 'fixed', 'width': '23%'})
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=100,
        n_intervals=0
    )
])

def parse_sensor_data(line):
    parts = [part.strip() for part in line.split('|')]
    
    adc_value = float(parts[0].split(':')[1].strip().split()[0])
    amplitude = float(parts[1].split(':')[1].strip().split('V')[0])
    frequency = float(parts[2].split(':')[1].strip().split('Hz')[0])
    status = parts[3].strip() if len(parts) > 3 else "N/A"
    
    return adc_value, amplitude, frequency, status

def update_plots(time_data, frequency_data, amplitude_data, current_time):
    fig_frequency.data[0].update(x=list(time_data), y=list(frequency_data))
    fig_amplitude.data[0].update(x=list(time_data), y=list(amplitude_data))
    
    time_window = 15
    xaxis_range = [current_time - time_window, current_time]
    fig_frequency.update_layout(xaxis_range=xaxis_range)
    fig_amplitude.update_layout(xaxis_range=xaxis_range)

def get_display_values(adc_value, frequency, amplitude, status):
    return (
        f"Status: {status}",
        f"Operation Mode: {status}",
        f"{adc_value:.2f}",
        f"{frequency:.2f} Hz",
        f"{amplitude:.2f} V"
    )

def get_fallback_values():
    return (
        fig_frequency,
        fig_amplitude,
        "System operational",
        coordinates_data[-1] if coordinates_data else "Waiting for coordinates...",
        f"{adc_data[-1]:.2f}" if adc_data and adc_data[-1] is not None else "Waiting...",
        f"{frequency_data[-1]:.2f} Hz" if frequency_data and frequency_data[-1] is not None else "Waiting...",
        f"{amplitude_data[-1]:.2f} V" if amplitude_data and amplitude_data[-1] is not None else "Waiting..."
    )

def handle_error(error_type="read", error=None):
    print(f"Error in {error_type}: {error}")
    return (
        fig_frequency,
        fig_amplitude,
        f"Error {error_type}ing data",
        "Error in data",
        str(adc_data[-1]) if adc_data else "Error",
        str(frequency_data[-1]) if frequency_data else "Error",
        str(amplitude_data[-1]) if amplitude_data else "Error"
    )

def update_data_points(adc_value, amplitude, frequency, status):
    current_time = time.time()
    time_data.append(current_time)
    amplitude_data.append(amplitude)
    frequency_data.append(frequency)
    coordinates_data.append(status)
    adc_data.append(adc_value)
    return current_time

@app.callback(
    [Output('frequency-graph', 'figure'),
     Output('amplitude-graph', 'figure'),
     Output('status-display', 'children'),
     Output('coordinates-display', 'children'),
     Output('adc-value', 'children'),
     Output('frequency-value', 'children'),
     Output('amplitude-value', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n_intervals):
    global fig_frequency, fig_amplitude, time_data, amplitude_data, frequency_data, coordinates_data, adc_data
    
    try:
        if not ser.in_waiting:
            return get_fallback_values()
            
        line = ser.readline().decode('utf-8').strip()
        if not ('ADC Value' in line and 'Amplitude' in line and 'Frequency' in line):
            return get_fallback_values()

        try:
            adc_value, amplitude, frequency, status = parse_sensor_data(line)
            current_time = update_data_points(adc_value, amplitude, frequency, status)
            update_plots(time_data, frequency_data, amplitude_data, current_time)
            return (fig_frequency, fig_amplitude, *get_display_values(adc_value, frequency, amplitude, status))
            
        except (IndexError, ValueError) as e:
            return handle_error("parsing", e)
            
    except Exception as e:
        return handle_error("reading", e)

# Start the Dash app server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)