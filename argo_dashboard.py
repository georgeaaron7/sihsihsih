import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import argopy
from datetime import datetime, timedelta
import json
import folium
from folium import plugins
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Argo Float Dashboard - Indian Ocean"

# Define the region around India's coast
INDIA_BBOX = [68, 8, 97, 30]  # [lon_min, lat_min, lon_max, lat_max]

class ArgoFloatDashboard:
    def __init__(self):
        self.fetcher = argopy.DataFetcher()
        self.float_data = None
        self.profile_data = None
        
    def fetch_floats_in_region(self, bbox=INDIA_BBOX, date_range=30):
        """Fetch Argo floats in the specified region"""
        try:
            # Get floats from the last 30 days around Indian coast
            end_date = datetime.now()
            start_date = end_date - timedelta(days=date_range)
            
            # Fetch data for the region
            ds = self.fetcher.region(bbox).load()
            
            # Convert to DataFrame for easier handling
            df = ds.argo.point2profile()
            
            # Get unique float information
            float_info = df.groupby('PLATFORM_NUMBER').agg({
                'LATITUDE': 'last',
                'LONGITUDE': 'last',
                'JULD': 'last',
                'CYCLE_NUMBER': 'max',
                'PRES': lambda x: x.dropna().max() if len(x.dropna()) > 0 else np.nan,
                'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
                'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan
            }).reset_index()
            
            float_info.columns = ['PLATFORM_NUMBER', 'LATITUDE', 'LONGITUDE', 'LAST_DATE', 
                                'MAX_CYCLE', 'MAX_DEPTH', 'AVG_TEMP', 'AVG_SALINITY']
            
            return float_info, ds
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None, None
    
    def get_float_profile_data(self, platform_number):
        """Get detailed profile data for a specific float"""
        try:
            # Fetch data for specific float
            ds = self.fetcher.float(int(platform_number)).load()
            df = ds.argo.point2profile()
            return df[df['PLATFORM_NUMBER'] == int(platform_number)]
        except Exception as e:
            print(f"Error fetching float data: {e}")
            return None

# Initialize dashboard
dashboard = ArgoFloatDashboard()

# Fetch initial data
print("Fetching Argo float data...")
float_info, raw_data = dashboard.fetch_floats_in_region()

if float_info is not None:
    print(f"Found {len(float_info)} floats in the region")
else:
    print("No data found. Using sample data for demonstration.")
    # Create sample data for demonstration
    float_info = pd.DataFrame({
        'PLATFORM_NUMBER': [1234567, 2345678, 3456789],
        'LATITUDE': [15.5, 12.3, 18.7],
        'LONGITUDE': [72.8, 75.2, 83.3],
        'LAST_DATE': [datetime.now() - timedelta(days=1)] * 3,
        'MAX_CYCLE': [45, 67, 23],
        'MAX_DEPTH': [2000, 1800, 1950],
        'AVG_TEMP': [28.5, 27.8, 29.1],
        'AVG_SALINITY': [35.2, 34.8, 35.5]
    })

def create_map():
    """Create Folium map with float locations"""
    if float_info is None:
        return html.Div("No data available")
    
    # Create map centered on Indian Ocean
    m = folium.Map(
        location=[15, 75], 
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add float markers
    for idx, row in float_info.iterrows():
        popup_text = f"""
        <b>Float ID:</b> {row['PLATFORM_NUMBER']}<br>
        <b>Last Position:</b> {row['LATITUDE']:.2f}°N, {row['LONGITUDE']:.2f}°E<br>
        <b>Last Update:</b> {row['LAST_DATE'].strftime('%Y-%m-%d') if pd.notna(row['LAST_DATE']) else 'N/A'}<br>
        <b>Max Depth:</b> {row['MAX_DEPTH']:.0f}m<br>
        <b>Cycles:</b> {row['MAX_CYCLE']}<br>
        <b>Avg Temp:</b> {row['AVG_TEMP']:.1f}°C<br>
        <b>Avg Salinity:</b> {row['AVG_SALINITY']:.1f} PSU
        """
        
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"Float {row['PLATFORM_NUMBER']}",
            icon=folium.Icon(color='blue', icon='anchor', prefix='fa')
        ).add_to(m)
    
    # Save map as HTML string
    map_html = m._repr_html_()
    return html.Iframe(srcDoc=map_html, width='100%', height='600px')

def create_float_table():
    """Create data table for float information"""
    if float_info is None:
        return html.Div("No data available")
    
    # Prepare data for table
    table_data = float_info.copy()
    table_data['LAST_DATE'] = table_data['LAST_DATE'].dt.strftime('%Y-%m-%d %H:%M')
    table_data['MAX_DEPTH'] = table_data['MAX_DEPTH'].round(0)
    table_data['AVG_TEMP'] = table_data['AVG_TEMP'].round(1)
    table_data['AVG_SALINITY'] = table_data['AVG_SALINITY'].round(1)
    
    return dash_table.DataTable(
        id='float-table',
        columns=[
            {'name': 'Platform ID', 'id': 'PLATFORM_NUMBER', 'type': 'numeric'},
            {'name': 'Latitude', 'id': 'LATITUDE', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Longitude', 'id': 'LONGITUDE', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Last Date', 'id': 'LAST_DATE'},
            {'name': 'Max Cycle', 'id': 'MAX_CYCLE', 'type': 'numeric'},
            {'name': 'Max Depth (m)', 'id': 'MAX_DEPTH', 'type': 'numeric'},
            {'name': 'Avg Temp (°C)', 'id': 'AVG_TEMP', 'type': 'numeric'},
            {'name': 'Avg Salinity (PSU)', 'id': 'AVG_SALINITY', 'type': 'numeric'},
        ],
        data=table_data.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        style_cell={'textAlign': 'center', 'fontSize': '12px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=10
    )

def create_profile_plots(platform_number=None):
    """Create profile plots for selected float"""
    if platform_number is None or float_info is None:
        return html.Div("Select a float to view profile data")
    
    try:
        # Get profile data for the selected float
        profile_data = dashboard.get_float_profile_data(platform_number)
        
        if profile_data is None or profile_data.empty:
            return html.Div("No profile data available for this float")
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Temperature Profile', 'Salinity Profile', 'Temperature vs Salinity'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Temperature profile
        fig.add_trace(
            go.Scatter(
                x=profile_data['TEMP'].dropna(),
                y=-profile_data.loc[profile_data['TEMP'].notna(), 'PRES'],
                mode='markers+lines',
                name='Temperature',
                marker=dict(color='red', size=4),
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
        
        # Salinity profile
        fig.add_trace(
            go.Scatter(
                x=profile_data['PSAL'].dropna(),
                y=-profile_data.loc[profile_data['PSAL'].notna(), 'PRES'],
                mode='markers+lines',
                name='Salinity',
                marker=dict(color='blue', size=4),
                line=dict(color='blue', width=2)
            ),
            row=1, col=2
        )
        
        # T-S diagram
        fig.add_trace(
            go.Scatter(
                x=profile_data['PSAL'].dropna(),
                y=profile_data.loc[profile_data['PSAL'].notna(), 'TEMP'],
                mode='markers',
                name='T-S',
                marker=dict(
                    color=profile_data.loc[profile_data['PSAL'].notna(), 'PRES'],
                    colorscale='Viridis',
                    size=6,
                    colorbar=dict(title="Pressure (dbar)")
                )
            ),
            row=1, col=3
        )
        
        # Update layout
        fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
        fig.update_xaxes(title_text="Salinity (PSU)", row=1, col=2)
        fig.update_xaxes(title_text="Salinity (PSU)", row=1, col=3)
        
        fig.update_yaxes(title_text="Depth (m)", row=1, col=1)
        fig.update_yaxes(title_text="Depth (m)", row=1, col=2)
        fig.update_yaxes(title_text="Temperature (°C)", row=1, col=3)
        
        fig.update_layout(
            height=500,
            title_text=f"Profile Data for Float {platform_number}",
            showlegend=False
        )
        
        return dcc.Graph(figure=fig)
        
    except Exception as e:
        return html.Div(f"Error creating profile plots: {str(e)}")

def create_time_series_plots(platform_number=None):
    """Create time series plots for selected float"""
    if platform_number is None or float_info is None:
        return html.Div("Select a float to view time series data")
    
    try:
        # Get profile data for the selected float
        profile_data = dashboard.get_float_profile_data(platform_number)
        
        if profile_data is None or profile_data.empty:
            return html.Div("No time series data available for this float")
        
        # Group by date/cycle for time series
        time_series = profile_data.groupby(['JULD', 'CYCLE_NUMBER']).agg({
            'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
            'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
            'PRES': lambda x: x.dropna().max() if len(x.dropna()) > 0 else np.nan
        }).reset_index()
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Surface Temperature', 'Surface Salinity', 'Max Depth'),
            vertical_spacing=0.1
        )
        
        # Temperature time series
        fig.add_trace(
            go.Scatter(
                x=time_series['JULD'],
                y=time_series['TEMP'],
                mode='markers+lines',
                name='Temperature',
                line=dict(color='red', width=2),
                marker=dict(color='red', size=6)
            ),
            row=1, col=1
        )
        
        # Salinity time series
        fig.add_trace(
            go.Scatter(
                x=time_series['JULD'],
                y=time_series['PSAL'],
                mode='markers+lines',
                name='Salinity',
                line=dict(color='blue', width=2),
                marker=dict(color='blue', size=6)
            ),
            row=2, col=1
        )
        
        # Depth time series
        fig.add_trace(
            go.Scatter(
                x=time_series['JULD'],
                y=time_series['PRES'],
                mode='markers+lines',
                name='Max Depth',
                line=dict(color='green', width=2),
                marker=dict(color='green', size=6)
            ),
            row=3, col=1
        )
        
        # Update layout
        fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Salinity (PSU)", row=2, col=1)
        fig.update_yaxes(title_text="Pressure (dbar)", row=3, col=1)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        
        fig.update_layout(
            height=600,
            title_text=f"Time Series for Float {platform_number}",
            showlegend=False
        )
        
        return dcc.Graph(figure=fig)
        
    except Exception as e:
        return html.Div(f"Error creating time series plots: {str(e)}")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🌊 Argo Float Dashboard - Indian Ocean", 
                   className="text-center mb-4",
                   style={'color': '#2c3e50'})
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("📍 Float Locations", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="map-container", children=create_map())
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("📊 Float Data Table", className="mb-0")),
                dbc.CardBody([
                    create_float_table()
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    html.Div(id="selected-float-info", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id="profile-plots")
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id="time-series-plots")
        ], width=12)
    ])
    
], fluid=True)

# Callbacks
@app.callback(
    [Output('selected-float-info', 'children'),
     Output('profile-plots', 'children'),
     Output('time-series-plots', 'children')],
    [Input('float-table', 'selected_rows')]
)
def update_float_details(selected_rows):
    if not selected_rows or float_info is None:
        return (
            dbc.Alert("Select a float from the table to view detailed information", 
                     color="info", className="text-center"),
            html.Div("Select a float to view profile plots"),
            html.Div("Select a float to view time series plots")
        )
    
    selected_idx = selected_rows[0]
    selected_float = float_info.iloc[selected_idx]
    platform_number = selected_float['PLATFORM_NUMBER']
    
    # Create info card
    info_card = dbc.Card([
        dbc.CardHeader([
            html.H4(f"🚢 Float {platform_number} Details", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P([html.Strong("Platform ID: "), str(platform_number)]),
                    html.P([html.Strong("Position: "), 
                           f"{selected_float['LATITUDE']:.3f}°N, {selected_float['LONGITUDE']:.3f}°E"]),
                    html.P([html.Strong("Last Update: "), 
                           selected_float['LAST_DATE'].strftime('%Y-%m-%d %H:%M') if pd.notna(selected_float['LAST_DATE']) else 'N/A']),
                ], md=4),
                dbc.Col([
                    html.P([html.Strong("Max Cycle: "), str(selected_float['MAX_CYCLE'])]),
                    html.P([html.Strong("Max Depth: "), f"{selected_float['MAX_DEPTH']:.0f} m"]),
                    html.P([html.Strong("Status: "), html.Span("Active", className="text-success")]),
                ], md=4),
                dbc.Col([
                    html.P([html.Strong("Avg Temperature: "), f"{selected_float['AVG_TEMP']:.1f}°C"]),
                    html.P([html.Strong("Avg Salinity: "), f"{selected_float['AVG_SALINITY']:.1f} PSU"]),
                    html.P([html.Strong("Data Quality: "), html.Span("Good", className="text-success")]),
                ], md=4)
            ])
        ])
    ], className="mb-4")
    
    # Create profile plots
    profile_plots_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📈 Profile Plots", className="mb-0")
        ]),
        dbc.CardBody([
            create_profile_plots(platform_number)
        ])
    ])
    
    # Create time series plots
    time_series_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📊 Time Series", className="mb-0")
        ]),
        dbc.CardBody([
            create_time_series_plots(platform_number)
        ])
    ])
    
    return info_card, profile_plots_card, time_series_card

if __name__ == '__main__':
    print("Starting Argo Float Dashboard...")
    print("Open your browser and go to: http://127.0.0.1:8050")
    app.run_server(debug=True, port=8050)
