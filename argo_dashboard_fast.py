import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium
import warnings
warnings.filterwarnings('ignore')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Argo Float Dashboard - Indian Ocean"

class ArgoFloatDashboard:
    def __init__(self):
        print("Initializing dashboard with sample data...")
        self.sample_data = self.create_sample_data()
        
    def create_sample_data(self):
        """Create comprehensive sample data for demonstration"""
        np.random.seed(42)
        
        # Sample float positions around Indian coast with realistic locations
        float_positions = [
            {'lat': 15.5, 'lon': 72.8, 'name': 'Arabian Sea - Mumbai Coast'},
            {'lat': 12.3, 'lon': 75.2, 'name': 'Kerala Coast - Kochi'},
            {'lat': 18.7, 'lon': 83.3, 'name': 'Bay of Bengal - Visakhapatnam'},
            {'lat': 8.2, 'lon': 77.5, 'name': 'South Indian Ocean - Kanyakumari'},
            {'lat': 21.0, 'lon': 70.0, 'name': 'Gujarat Coast - Porbandar'},
            {'lat': 13.1, 'lon': 80.2, 'name': 'Tamil Nadu Coast - Chennai'},
            {'lat': 16.8, 'lon': 82.5, 'name': 'Andhra Coast - Kakinada'},
            {'lat': 11.5, 'lon': 92.8, 'name': 'Andaman Sea - Port Blair'}
        ]
        
        float_info_list = []
        profile_data_list = []
        
        for i, pos in enumerate(float_positions):
            platform_number = 1234567 + i
            
            # Generate realistic float summary info
            last_date = datetime.now() - timedelta(days=np.random.randint(1, 15))
            max_cycles = np.random.randint(25, 85)
            max_depth = np.random.randint(1200, 2000)
            
            # Temperature varies by location (Arabian Sea warmer than Bay of Bengal)
            base_temp = 28.5 if 'Arabian Sea' in pos['name'] or 'Gujarat' in pos['name'] else 27.2
            avg_temp = base_temp + np.random.normal(0, 1.5)
            
            # Salinity varies by region
            base_salinity = 35.2 if 'Arabian Sea' in pos['name'] else 34.1
            avg_salinity = base_salinity + np.random.normal(0, 0.3)
            
            float_info_list.append({
                'PLATFORM_NUMBER': platform_number,
                'LATITUDE': pos['lat'] + np.random.normal(0, 0.3),
                'LONGITUDE': pos['lon'] + np.random.normal(0, 0.3),
                'LAST_DATE': last_date,
                'MAX_CYCLE': max_cycles,
                'MAX_DEPTH': max_depth,
                'AVG_TEMP': avg_temp,
                'AVG_SALINITY': avg_salinity,
                'LOCATION': pos['name']
            })
            
            # Generate realistic profile data for each float
            n_profiles = np.random.randint(5, 12)  # Multiple profiles per float
            
            for profile in range(n_profiles):
                profile_date = datetime.now() - timedelta(days=np.random.randint(1, 180))
                cycle_number = profile + 1
                
                # Generate depth points (more resolution in upper ocean)
                depths_shallow = np.arange(0, 200, 5)   # High resolution in upper 200m
                depths_mid = np.arange(200, 1000, 20)   # Medium resolution 200-1000m
                depths_deep = np.arange(1000, max_depth, 50)  # Lower resolution below 1000m
                depths = np.concatenate([depths_shallow, depths_mid, depths_deep])
                
                for depth in depths:
                    # Realistic temperature profile (warm surface, cold deep)
                    if depth < 50:  # Mixed layer
                        temp = avg_temp + np.random.normal(0, 0.5)
                    elif depth < 200:  # Thermocline
                        temp = avg_temp - (depth - 50) * 0.12 + np.random.normal(0, 0.8)
                    elif depth < 1000:  # Deep water
                        temp = 12 - (depth - 200) * 0.008 + np.random.normal(0, 0.3)
                    else:  # Abyssal
                        temp = 4 - (depth - 1000) * 0.002 + np.random.normal(0, 0.2)
                    
                    temp = max(temp, 2.0)  # Minimum temperature
                    
                    # Realistic salinity profile
                    if depth < 100:  # Surface layer
                        salinity = avg_salinity + np.random.normal(0, 0.1)
                    elif depth < 500:  # Subsurface
                        salinity = avg_salinity + 0.3 + (depth - 100) * 0.0005 + np.random.normal(0, 0.1)
                    else:  # Deep water
                        salinity = 34.7 + np.random.normal(0, 0.05)
                    
                    profile_data_list.append({
                        'PLATFORM_NUMBER': platform_number,
                        'CYCLE_NUMBER': cycle_number,
                        'JULD': profile_date,
                        'LATITUDE': pos['lat'] + np.random.normal(0, 0.05),
                        'LONGITUDE': pos['lon'] + np.random.normal(0, 0.05),
                        'PRES': depth,
                        'TEMP': temp,
                        'PSAL': salinity
                    })
        
        float_info_df = pd.DataFrame(float_info_list)
        profile_data_df = pd.DataFrame(profile_data_list)
        
        return {
            'float_info': float_info_df,
            'profile_data': profile_data_df
        }

# Initialize dashboard
dashboard = ArgoFloatDashboard()
float_info = dashboard.sample_data['float_info']
profile_data = dashboard.sample_data['profile_data']

print(f"Dashboard initialized with {len(float_info)} floats")

def create_map():
    """Create Folium map with float locations"""
    # Create map centered on Indian Ocean
    m = folium.Map(
        location=[15, 75], 
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add float markers
    for idx, row in float_info.iterrows():
        popup_text = f"""
        <div style="font-family: Arial, sans-serif; width: 220px;">
            <h4 style="color: #2c3e50; margin-bottom: 10px;">🚢 Float {row['PLATFORM_NUMBER']}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>📍 Position:</b><br>
            {row['LATITUDE']:.3f}°N, {row['LONGITUDE']:.3f}°E</p>
            
            <p style="margin: 5px 0;"><b>📅 Last Update:</b><br>
            {row['LAST_DATE'].strftime('%Y-%m-%d %H:%M')}</p>
            
            <p style="margin: 5px 0;"><b>🌊 Max Depth:</b> {row['MAX_DEPTH']:.0f}m</p>
            <p style="margin: 5px 0;"><b>🔄 Cycles:</b> {row['MAX_CYCLE']}</p>
            <p style="margin: 5px 0;"><b>🌡️ Avg Temp:</b> {row['AVG_TEMP']:.1f}°C</p>
            <p style="margin: 5px 0;"><b>🧂 Avg Salinity:</b> {row['AVG_SALINITY']:.1f} PSU</p>
            
            <p style="margin: 5px 0;"><b>📍 Location:</b><br>
            {row['LOCATION']}</p>
        </div>
        """
        
        # Color code by temperature
        temp = row['AVG_TEMP']
        if temp > 28:
            color = 'red'
        elif temp > 26:
            color = 'orange'
        elif temp > 24:
            color = 'green'
        else:
            color = 'blue'
        
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"🚢 Float {row['PLATFORM_NUMBER']} ({temp:.1f}°C)",
            icon=folium.Icon(color=color, icon='anchor', prefix='fa')
        ).add_to(m)
    
    # Add temperature legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 170px; height: 110px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; border-radius: 5px;">
    <p style="margin: 5px 0;"><strong>🌡️ Temperature Legend</strong></p>
    <p style="margin: 3px 0;"><i class="fa fa-anchor" style="color:red"></i> > 28°C (Very Warm)</p>
    <p style="margin: 3px 0;"><i class="fa fa-anchor" style="color:orange"></i> 26-28°C (Warm)</p>
    <p style="margin: 3px 0;"><i class="fa fa-anchor" style="color:green"></i> 24-26°C (Moderate)</p>
    <p style="margin: 3px 0;"><i class="fa fa-anchor" style="color:blue"></i> < 24°C (Cool)</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map as HTML string
    map_html = m._repr_html_()
    return html.Iframe(srcDoc=map_html, width='100%', height='600px', style={'border': 'none'})

def create_float_table():
    """Create data table for float information"""
    table_data = float_info.copy()
    table_data['LAST_DATE'] = table_data['LAST_DATE'].dt.strftime('%Y-%m-%d %H:%M')
    table_data['MAX_DEPTH'] = table_data['MAX_DEPTH'].round(0)
    table_data['AVG_TEMP'] = table_data['AVG_TEMP'].round(1)
    table_data['AVG_SALINITY'] = table_data['AVG_SALINITY'].round(2)
    
    return dash_table.DataTable(
        id='float-table',
        columns=[
            {'name': 'Platform ID', 'id': 'PLATFORM_NUMBER', 'type': 'numeric'},
            {'name': 'Latitude', 'id': 'LATITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
            {'name': 'Longitude', 'id': 'LONGITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
            {'name': 'Last Update', 'id': 'LAST_DATE'},
            {'name': 'Cycles', 'id': 'MAX_CYCLE', 'type': 'numeric'},
            {'name': 'Max Depth (m)', 'id': 'MAX_DEPTH', 'type': 'numeric'},
            {'name': 'Avg Temp (°C)', 'id': 'AVG_TEMP', 'type': 'numeric'},
            {'name': 'Avg Salinity (PSU)', 'id': 'AVG_SALINITY', 'type': 'numeric'},
            {'name': 'Location', 'id': 'LOCATION'},
        ],
        data=table_data.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        style_cell={'textAlign': 'center', 'fontSize': '11px', 'padding': '6px'},
        style_header={
            'backgroundColor': '#3498db',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontSize': '12px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} > 28'},
                'backgroundColor': '#ffebee',
                'color': 'black',
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} <= 25'},
                'backgroundColor': '#e3f2fd',
                'color': 'black',
            }
        ],
        page_size=10,
        sort_action="native",
        filter_action="native",
        style_table={'overflowX': 'auto'}
    )

def create_profile_plots(platform_number=None):
    """Create profile plots for selected float"""
    if platform_number is None:
        return dbc.Alert("👆 Select a float from the table above to view profile data", 
                        color="info", className="text-center")
    
    # Get profile data for the selected float
    float_profile_data = profile_data[profile_data['PLATFORM_NUMBER'] == int(platform_number)]
    
    if float_profile_data.empty:
        return dbc.Alert("No profile data available for this float", 
                        color="warning", className="text-center")
    
    # Get the most recent profile
    latest_cycle = float_profile_data['CYCLE_NUMBER'].max()
    recent_data = float_profile_data[float_profile_data['CYCLE_NUMBER'] == latest_cycle]
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Temperature Profile', 'Salinity Profile', 'T-S Diagram'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Temperature profile
    temp_data = recent_data.dropna(subset=['TEMP', 'PRES']).sort_values('PRES')
    fig.add_trace(
        go.Scatter(
            x=temp_data['TEMP'],
            y=-temp_data['PRES'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='red', width=3),
            marker=dict(color='red', size=4),
            hovertemplate='<b>Temperature Profile</b><br>Temp: %{x:.1f}°C<br>Depth: %{y:.0f}m<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Salinity profile
    sal_data = recent_data.dropna(subset=['PSAL', 'PRES']).sort_values('PRES')
    fig.add_trace(
        go.Scatter(
            x=sal_data['PSAL'],
            y=-sal_data['PRES'],
            mode='lines+markers',
            name='Salinity',
            line=dict(color='blue', width=3),
            marker=dict(color='blue', size=4),
            hovertemplate='<b>Salinity Profile</b><br>Salinity: %{x:.2f} PSU<br>Depth: %{y:.0f}m<extra></extra>'
        ),
        row=1, col=2
    )
    
    # T-S diagram
    ts_data = recent_data.dropna(subset=['TEMP', 'PSAL', 'PRES'])
    fig.add_trace(
        go.Scatter(
            x=ts_data['PSAL'],
            y=ts_data['TEMP'],
            mode='markers',
            name='T-S',
            marker=dict(
                color=ts_data['PRES'],
                colorscale='Viridis_r',
                size=8,
                colorbar=dict(title="Pressure (dbar)", x=1.02, len=0.3),
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>T-S Diagram</b><br>Salinity: %{x:.2f} PSU<br>Temp: %{y:.1f}°C<br>Pressure: %{marker.color:.0f} dbar<extra></extra>'
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
        title_text=f"Latest Profile Data - Float {platform_number} (Cycle {latest_cycle})",
        showlegend=False,
        template="plotly_white"
    )
    
    return dcc.Graph(figure=fig)

def create_time_series_plots(platform_number=None):
    """Create time series plots for selected float"""
    if platform_number is None:
        return dbc.Alert("👆 Select a float from the table above to view time series data", 
                        color="info", className="text-center")
    
    # Get profile data for the selected float
    float_profile_data = profile_data[profile_data['PLATFORM_NUMBER'] == int(platform_number)]
    
    if float_profile_data.empty:
        return dbc.Alert("No time series data available for this float", 
                        color="warning", className="text-center")
    
    # Create time series data (surface data - pressure < 50)
    surface_data = float_profile_data[float_profile_data['PRES'] <= 50]
    time_series = surface_data.groupby(['JULD', 'CYCLE_NUMBER']).agg({
        'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
        'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
    }).reset_index()
    
    # Also get max depth per profile
    depth_series = float_profile_data.groupby(['JULD', 'CYCLE_NUMBER'])['PRES'].max().reset_index()
    
    time_series = time_series.sort_values('JULD')
    depth_series = depth_series.sort_values('JULD')
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Surface Temperature Over Time', 'Surface Salinity Over Time', 'Profile Depth Over Time'),
        vertical_spacing=0.12
    )
    
    # Temperature time series
    fig.add_trace(
        go.Scatter(
            x=time_series['JULD'],
            y=time_series['TEMP'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='red', width=3),
            marker=dict(color='red', size=8),
            hovertemplate='<b>Surface Temperature</b><br>Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Salinity time series
    fig.add_trace(
        go.Scatter(
            x=time_series['JULD'],
            y=time_series['PSAL'],
            mode='lines+markers',
            name='Salinity',
            line=dict(color='blue', width=3),
            marker=dict(color='blue', size=8),
            hovertemplate='<b>Surface Salinity</b><br>Date: %{x}<br>Salinity: %{y:.2f} PSU<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Depth time series
    fig.add_trace(
        go.Scatter(
            x=depth_series['JULD'],
            y=depth_series['PRES'],
            mode='lines+markers',
            name='Max Depth',
            line=dict(color='green', width=3),
            marker=dict(color='green', size=8),
            hovertemplate='<b>Profile Depth</b><br>Date: %{x}<br>Max Depth: %{y:.0f} dbar<extra></extra>'
        ),
        row=3, col=1
    )
    
    # Update layout
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_yaxes(title_text="Salinity (PSU)", row=2, col=1)
    fig.update_yaxes(title_text="Pressure (dbar)", row=3, col=1)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    
    fig.update_layout(
        height=700,
        title_text=f"Time Series Analysis - Float {platform_number}",
        showlegend=False,
        template="plotly_white"
    )
    
    return dcc.Graph(figure=fig)

def create_summary_cards():
    """Create summary cards with key statistics"""
    total_floats = len(float_info)
    avg_temp = float_info['AVG_TEMP'].mean()
    avg_salinity = float_info['AVG_SALINITY'].mean()
    max_depth = float_info['MAX_DEPTH'].max()
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_floats}", className="text-primary mb-0"),
                    html.P("Active Floats", className="text-muted mb-0", style={'fontSize': '14px'})
                ])
            ], className="text-center shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{avg_temp:.1f}°C", className="text-danger mb-0"),
                    html.P("Avg Temperature", className="text-muted mb-0", style={'fontSize': '14px'})
                ])
            ], className="text-center shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{avg_salinity:.1f}", className="text-info mb-0"),
                    html.P("Avg Salinity (PSU)", className="text-muted mb-0", style={'fontSize': '14px'})
                ])
            ], className="text-center shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{max_depth:.0f}m", className="text-success mb-0"),
                    html.P("Max Depth", className="text-muted mb-0", style={'fontSize': '14px'})
                ])
            ], className="text-center shadow-sm")
        ], width=3)
    ], className="mb-4")

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🌊 Argo Float Dashboard", 
                       className="display-4 text-center mb-2",
                       style={'color': '#2c3e50', 'font-weight': 'bold'}),
                html.H4("Indian Ocean Monitoring System", 
                       className="text-center text-muted mb-3"),
                dbc.Badge("Interactive Demo with Realistic Data", 
                         color="success", className="mb-3")
            ], className="text-center")
        ])
    ]),
    
    # Summary Cards
    create_summary_cards(),
    
    # Map Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📍 Float Locations & Real-time Status", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Alert([
                        html.Strong("Interactive Map Instructions:"),
                        html.Br(),
                        "• Click on any float marker to view detailed information",
                        html.Br(),
                        "• Markers are color-coded by temperature (see legend)",
                        html.Br(),
                        "• Zoom and pan to explore different regions"
                    ], color="light", className="mb-3"),
                    html.Div(id="map-container", children=create_map())
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📊 Float Data Table", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Alert([
                        html.Strong("How to use:"),
                        " Click on any row to select a float and view detailed analysis below. ",
                        "Use column filters to search specific data."
                    ], color="light", className="mb-3"),
                    create_float_table()
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # Selected Float Information
    html.Div(id="selected-float-info", className="mb-4"),
    
    # Profile Plots
    dbc.Row([
        dbc.Col([
            html.Div(id="profile-plots")
        ], width=12)
    ], className="mb-4"),
    
    # Time Series Plots
    dbc.Row([
        dbc.Col([
            html.Div(id="time-series-plots")
        ], width=12)
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                "🔬 Data source: Argo Global Data Assembly Centre | ",
                "💻 Built with ArgoPy & Plotly Dash | ",
                "🌊 Indian Ocean Focus"
            ], className="text-center text-muted", style={'fontSize': '12px'})
        ])
    ])
    
], fluid=True, style={'backgroundColor': '#f8f9fa'})

# Callbacks
@app.callback(
    [Output('selected-float-info', 'children'),
     Output('profile-plots', 'children'),
     Output('time-series-plots', 'children')],
    [Input('float-table', 'selected_rows')]
)
def update_float_details(selected_rows):
    if not selected_rows:
        return (
            dbc.Alert([
                html.H5("👆 Select a Float to Begin Analysis", className="alert-heading"),
                html.P("Click on any row in the data table above to view comprehensive analysis including:"),
                html.Ul([
                    html.Li("📈 Vertical temperature and salinity profiles"),
                    html.Li("📊 Time series analysis showing trends over time"),
                    html.Li("🌡️ T-S diagrams for water mass identification"),
                    html.Li("📍 Detailed float information and operational status")
                ])
            ], color="info"),
            html.Div(),
            html.Div()
        )
    
    selected_idx = selected_rows[0]
    selected_float = float_info.iloc[selected_idx]
    platform_number = selected_float['PLATFORM_NUMBER']
    
    # Create detailed info card
    info_card = dbc.Card([
        dbc.CardHeader([
            html.H4([
                "🚢 Float ", html.Code(str(platform_number)), " - Comprehensive Analysis"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("📍 Location & Position", className="text-primary mb-3"),
                    html.P([html.Strong("Platform ID: "), html.Code(str(platform_number))]),
                    html.P([html.Strong("Current Position: "), 
                           f"{selected_float['LATITUDE']:.4f}°N, {selected_float['LONGITUDE']:.4f}°E"]),
                    html.P([html.Strong("Last Update: "), 
                           selected_float['LAST_DATE'].strftime('%Y-%m-%d %H:%M UTC')]),
                    html.P([html.Strong("Region: "), 
                           html.Span(selected_float['LOCATION'], className="badge badge-secondary")])
                ], md=4),
                dbc.Col([
                    html.H6("🔄 Operational Data", className="text-success mb-3"),
                    html.P([html.Strong("Total Cycles: "), 
                           html.Span(str(selected_float['MAX_CYCLE']), className="badge badge-light")]),
                    html.P([html.Strong("Maximum Depth: "), 
                           f"{selected_float['MAX_DEPTH']:.0f} meters"]),
                    html.P([html.Strong("Status: "), 
                           dbc.Badge("Active & Transmitting", color="success")]),
                    html.P([html.Strong("Data Quality: "), 
                           dbc.Badge("Excellent", color="success")])
                ], md=4),
                dbc.Col([
                    html.H6("🌡️ Environmental Summary", className="text-info mb-3"),
                    html.P([html.Strong("Average Temperature: "), 
                           f"{selected_float['AVG_TEMP']:.2f}°C"]),
                    html.P([html.Strong("Average Salinity: "), 
                           f"{selected_float['AVG_SALINITY']:.2f} PSU"]),
                    html.P([html.Strong("Temp Classification: "), 
                           "Tropical" if selected_float['AVG_TEMP'] > 26 else "Subtropical"]),
                    html.P([html.Strong("Water Mass: "), 
                           "Arabian Sea" if selected_float['AVG_SALINITY'] > 35 else "Bay of Bengal"])
                ], md=4)
            ])
        ])
    ], className="mb-4 shadow-sm", color="light", outline=True)
    
    # Create profile plots card
    profile_plots_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📈 Vertical Profile Analysis", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Alert([
                html.Strong("Profile Analysis:"),
                " These plots show the most recent vertical measurements. ",
                "Temperature typically decreases with depth, while salinity shows characteristic patterns. ",
                "The T-S diagram reveals water mass properties (color indicates depth)."
            ], color="light", className="mb-3"),
            create_profile_plots(platform_number)
        ])
    ], className="shadow-sm")
    
    # Create time series plots card
    time_series_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📊 Historical Time Series Analysis", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Alert([
                html.Strong("Time Series Analysis:"),
                " Track how surface conditions have changed over time. ",
                "Look for seasonal patterns, trends, or anomalies in temperature and salinity. ",
                "Profile depth shows the maximum depth reached during each measurement cycle."
            ], color="light", className="mb-3"),
            create_time_series_plots(platform_number)
        ])
    ], className="shadow-sm")
    
    return info_card, profile_plots_card, time_series_card

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌊 ARGO FLOAT DASHBOARD - INDIAN OCEAN")
    print("="*60)
    print("📊 Mode: Interactive Demo with Realistic Sample Data")
    print(f"🚢 Active Floats: {len(float_info)}")
    print("🌍 Region: Indian Ocean (Arabian Sea, Bay of Bengal)")
    print("="*60)
    print("\n🚀 Starting dashboard server...")
    print("📱 Open your browser and navigate to: http://127.0.0.1:8052")
    print("\n✨ Dashboard Features:")
    print("   • Interactive Leaflet map with float locations")
    print("   • Detailed profile plots (Temperature, Salinity, T-S diagrams)")
    print("   • Time series analysis with historical trends")
    print("   • Sortable/filterable data table")
    print("   • Comprehensive float information and status")
    print("\n💡 Usage Tips:")
    print("   • Click on map markers for popup information")
    print("   • Select table rows to view detailed analysis")
    print("   • Use table filters to search specific data")
    print("   • All plots are interactive with hover information")
    print("\n" + "="*60)
    
    app.run(debug=False, port=8052, host='127.0.0.1')
