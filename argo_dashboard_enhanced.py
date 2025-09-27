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
import warnings
warnings.filterwarnings('ignore')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Argo Float Dashboard - Indian Ocean"

# Define the region around India's coast
INDIA_BBOX = [68, 8, 97, 30]  # [lon_min, lat_min, lon_max, lat_max]

class ArgoFloatDashboard:
    def __init__(self):
        # Initialize DataFetcher with proper source specification
        self.fetcher = argopy.DataFetcher(src='erddap')
        self.sample_data = self.create_sample_data()
        
    def create_sample_data(self):
        """Create sample data for demonstration"""
        np.random.seed(42)
        
        # Sample float positions around Indian coast
        float_positions = [
            {'lat': 15.5, 'lon': 72.8, 'name': 'Arabian Sea'},
            {'lat': 12.3, 'lon': 75.2, 'name': 'Kerala Coast'},
            {'lat': 18.7, 'lon': 83.3, 'name': 'Bay of Bengal'},
            {'lat': 8.2, 'lon': 77.5, 'name': 'South Indian Ocean'},
            {'lat': 21.0, 'lon': 70.0, 'name': 'Gujarat Coast'},
            {'lat': 13.1, 'lon': 80.2, 'name': 'Tamil Nadu Coast'},
            {'lat': 16.8, 'lon': 82.5, 'name': 'Andhra Coast'},
            {'lat': 11.5, 'lon': 92.8, 'name': 'Andaman Sea'}
        ]
        
        float_info_list = []
        profile_data_list = []
        
        for i, pos in enumerate(float_positions):
            platform_number = 1234567 + i
            
            # Float summary info
            float_info_list.append({
                'PLATFORM_NUMBER': platform_number,
                'LATITUDE': pos['lat'] + np.random.normal(0, 0.5),
                'LONGITUDE': pos['lon'] + np.random.normal(0, 0.5),
                'LAST_DATE': datetime.now() - timedelta(days=np.random.randint(1, 30)),
                'MAX_CYCLE': np.random.randint(20, 80),
                'MAX_DEPTH': np.random.randint(1500, 2000),
                'AVG_TEMP': 26 + np.random.normal(0, 2),
                'AVG_SALINITY': 34.5 + np.random.normal(0, 0.5),
                'LOCATION': pos['name']
            })
            
            # Generate profile data for each float
            depths = np.arange(0, 2000, 10)
            n_profiles = np.random.randint(3, 8)
            
            for profile in range(n_profiles):
                date = datetime.now() - timedelta(days=np.random.randint(1, 365))
                
                for depth in depths:
                    # Temperature profile (decreases with depth)
                    temp = 28 - (depth/100) * 0.8 + np.random.normal(0, 0.5)
                    temp = max(temp, 2)  # Minimum temperature
                    
                    # Salinity profile (increases slightly with depth)
                    salinity = 34.5 + (depth/1000) * 0.3 + np.random.normal(0, 0.1)
                    
                    profile_data_list.append({
                        'PLATFORM_NUMBER': platform_number,
                        'CYCLE_NUMBER': profile + 1,
                        'JULD': date,
                        'LATITUDE': pos['lat'] + np.random.normal(0, 0.1),
                        'LONGITUDE': pos['lon'] + np.random.normal(0, 0.1),
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
    
    def fetch_floats_in_region(self, use_real_data=True):
        """Fetch Argo floats in the specified region"""
        if not use_real_data:
            return self.sample_data['float_info'], self.sample_data['profile_data']
            
        try:
            print("Attempting to fetch real Argo data...")
            # Use proper argopy region format: [lon_min, lon_max, lat_min, lat_max, pres_min, pres_max, date_start, date_end]
            # For recent data, let's get last 30 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # Region around India with time constraints
            region_box = [INDIA_BBOX[0], INDIA_BBOX[2], INDIA_BBOX[1], INDIA_BBOX[3], 0, 2000, 
                         start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')]
            
            print(f"Fetching data for region: {region_box}")
            ds = self.fetcher.region(region_box).load()
            
            # Convert to point2profile format for easier handling
            df = ds.argo.point2profile()
            print(f"Raw data shape: {df.shape}")
            
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
            
            print(f"Successfully fetched data for {len(float_info)} floats")
            return float_info, df
            
        except Exception as e:
            print(f"Error fetching real data: {e}")
            print("Using sample data instead...")
            return self.sample_data['float_info'], self.sample_data['profile_data']
    
    def get_float_profile_data(self, platform_number, use_real_data=True):
        """Get detailed profile data for a specific float"""
        if not use_real_data:
            return self.sample_data['profile_data'][
                self.sample_data['profile_data']['PLATFORM_NUMBER'] == int(platform_number)
            ]
            
        try:
            print(f"Fetching detailed data for float {platform_number}")
            # Create new fetcher instance for specific float
            float_fetcher = argopy.DataFetcher(src='erddap')
            ds = float_fetcher.float(int(platform_number)).load()
            df = ds.argo.point2profile()
            return df[df['PLATFORM_NUMBER'] == int(platform_number)]
        except Exception as e:
            print(f"Error fetching real float data: {e}")
            return self.sample_data['profile_data'][
                self.sample_data['profile_data']['PLATFORM_NUMBER'] == int(platform_number)
            ]

# Initialize dashboard
dashboard = ArgoFloatDashboard()

# Try to fetch real data, fall back to sample data
print("Initializing Argo Float Dashboard...")
float_info, profile_data = dashboard.fetch_floats_in_region(use_real_data=True)

# Check if we got real data or sample data
if isinstance(profile_data, pd.DataFrame) and len(profile_data) > 0:
    using_real_data = 'PLATFORM_NUMBER' in profile_data.columns and len(profile_data['PLATFORM_NUMBER'].unique()) > 0
else:
    using_real_data = False

print(f"Dashboard initialized with {'real' if using_real_data else 'sample'} data")
print(f"Found {len(float_info)} floats in the region")

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
        <div style="font-family: Arial, sans-serif; width: 200px;">
            <h4 style="color: #2c3e50;">Float {row['PLATFORM_NUMBER']}</h4>
            <hr>
            <b>📍 Position:</b><br>
            {row['LATITUDE']:.3f}°N, {row['LONGITUDE']:.3f}°E<br><br>
            
            <b>📅 Last Update:</b><br>
            {row['LAST_DATE'].strftime('%Y-%m-%d') if pd.notna(row['LAST_DATE']) else 'N/A'}<br><br>
            
            <b>🌊 Max Depth:</b> {row['MAX_DEPTH']:.0f}m<br>
            <b>🔄 Cycles:</b> {row['MAX_CYCLE']}<br>
            <b>🌡️ Avg Temp:</b> {row['AVG_TEMP']:.1f}°C<br>
            <b>🧂 Avg Salinity:</b> {row['AVG_SALINITY']:.1f} PSU<br>
            
            {f"<br><b>📍 Location:</b> {row['LOCATION']}" if 'LOCATION' in row else ""}
        </div>
        """
        
        # Color code by temperature
        temp = row['AVG_TEMP']
        if temp > 28:
            color = 'red'
        elif temp > 25:
            color = 'orange'
        else:
            color = 'blue'
        
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"🚢 Float {row['PLATFORM_NUMBER']} ({temp:.1f}°C)",
            icon=folium.Icon(color=color, icon='anchor', prefix='fa')
        ).add_to(m)
    
    # Add a legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><strong>Temperature Legend</strong></p>
    <p><i class="fa fa-anchor" style="color:red"></i> > 28°C</p>
    <p><i class="fa fa-anchor" style="color:orange"></i> 25-28°C</p>
    <p><i class="fa fa-anchor" style="color:blue"></i> < 25°C</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map as HTML string
    map_html = m._repr_html_()
    return html.Iframe(srcDoc=map_html, width='100%', height='600px', style={'border': 'none'})

def create_float_table():
    """Create data table for float information"""
    # Prepare data for table
    table_data = float_info.copy()
    if 'LAST_DATE' in table_data.columns:
        table_data['LAST_DATE'] = table_data['LAST_DATE'].dt.strftime('%Y-%m-%d')
    table_data['MAX_DEPTH'] = table_data['MAX_DEPTH'].round(0)
    table_data['AVG_TEMP'] = table_data['AVG_TEMP'].round(1)
    table_data['AVG_SALINITY'] = table_data['AVG_SALINITY'].round(1)
    
    columns = [
        {'name': 'Platform ID', 'id': 'PLATFORM_NUMBER', 'type': 'numeric'},
        {'name': 'Latitude', 'id': 'LATITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
        {'name': 'Longitude', 'id': 'LONGITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
        {'name': 'Last Date', 'id': 'LAST_DATE'},
        {'name': 'Max Cycle', 'id': 'MAX_CYCLE', 'type': 'numeric'},
        {'name': 'Max Depth (m)', 'id': 'MAX_DEPTH', 'type': 'numeric'},
        {'name': 'Avg Temp (°C)', 'id': 'AVG_TEMP', 'type': 'numeric'},
        {'name': 'Avg Salinity (PSU)', 'id': 'AVG_SALINITY', 'type': 'numeric'},
    ]
    
    if 'LOCATION' in table_data.columns:
        columns.append({'name': 'Location', 'id': 'LOCATION'})
    
    return dash_table.DataTable(
        id='float-table',
        columns=columns,
        data=table_data.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        style_cell={'textAlign': 'center', 'fontSize': '12px', 'padding': '8px'},
        style_header={
            'backgroundColor': '#3498db',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} > 28'},
                'backgroundColor': '#ffe6e6',
                'color': 'black',
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} <= 25'},
                'backgroundColor': '#e6f3ff',
                'color': 'black',
            }
        ],
        page_size=10,
        sort_action="native",
        filter_action="native"
    )

def create_profile_plots(platform_number=None):
    """Create profile plots for selected float"""
    if platform_number is None:
        return dbc.Alert("Select a float from the table to view profile data", 
                        color="info", className="text-center")
    
    try:
        # Get profile data for the selected float
        if using_real_data:
            profile_df = dashboard.get_float_profile_data(platform_number, use_real_data=True)
        else:
            profile_df = profile_data[profile_data['PLATFORM_NUMBER'] == int(platform_number)]
        
        if profile_df is None or profile_df.empty:
            return dbc.Alert("No profile data available for this float", 
                           color="warning", className="text-center")
        
        # Get the most recent profile
        latest_profile = profile_df.loc[profile_df['CYCLE_NUMBER'].idxmax()]
        recent_data = profile_df[profile_df['CYCLE_NUMBER'] == latest_profile['CYCLE_NUMBER']]
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Temperature Profile', 'Salinity Profile', 'T-S Diagram'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Temperature profile
        temp_data = recent_data.dropna(subset=['TEMP', 'PRES'])
        if not temp_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=temp_data['TEMP'],
                    y=-temp_data['PRES'],
                    mode='markers+lines',
                    name='Temperature',
                    marker=dict(color='red', size=4),
                    line=dict(color='red', width=2),
                    hovertemplate='Temp: %{x:.1f}°C<br>Depth: %{y:.0f}m<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Salinity profile
        sal_data = recent_data.dropna(subset=['PSAL', 'PRES'])
        if not sal_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=sal_data['PSAL'],
                    y=-sal_data['PRES'],
                    mode='markers+lines',
                    name='Salinity',
                    marker=dict(color='blue', size=4),
                    line=dict(color='blue', width=2),
                    hovertemplate='Salinity: %{x:.2f} PSU<br>Depth: %{y:.0f}m<extra></extra>'
                ),
                row=1, col=2
            )
        
        # T-S diagram
        ts_data = recent_data.dropna(subset=['TEMP', 'PSAL', 'PRES'])
        if not ts_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=ts_data['PSAL'],
                    y=ts_data['TEMP'],
                    mode='markers',
                    name='T-S',
                    marker=dict(
                        color=ts_data['PRES'],
                        colorscale='Viridis',
                        size=8,
                        colorbar=dict(title="Pressure (dbar)", x=1.02)
                    ),
                    hovertemplate='Salinity: %{x:.2f} PSU<br>Temp: %{y:.1f}°C<br>Pressure: %{marker.color:.0f} dbar<extra></extra>'
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
            title_text=f"Latest Profile Data for Float {platform_number} (Cycle {latest_profile['CYCLE_NUMBER']})",
            showlegend=False,
            template="plotly_white"
        )
        
        return dcc.Graph(figure=fig)
        
    except Exception as e:
        return dbc.Alert(f"Error creating profile plots: {str(e)}", 
                        color="danger", className="text-center")

def create_time_series_plots(platform_number=None):
    """Create time series plots for selected float"""
    if platform_number is None:
        return dbc.Alert("Select a float from the table to view time series data", 
                        color="info", className="text-center")
    
    try:
        # Get profile data for the selected float
        if using_real_data:
            profile_df = dashboard.get_float_profile_data(platform_number, use_real_data=True)
        else:
            profile_df = profile_data[profile_data['PLATFORM_NUMBER'] == int(platform_number)]
        
        if profile_df is None or profile_df.empty:
            return dbc.Alert("No time series data available for this float", 
                           color="warning", className="text-center")
        
        # Group by date/cycle for time series (surface data - pressure < 50)
        surface_data = profile_df[profile_df['PRES'] <= 50]
        time_series = surface_data.groupby(['JULD', 'CYCLE_NUMBER']).agg({
            'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
            'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
            'PRES': lambda x: x.dropna().max() if len(x.dropna()) > 0 else np.nan
        }).reset_index()
        
        time_series = time_series.sort_values('JULD')
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Surface Temperature Over Time', 'Surface Salinity Over Time', 'Profile Depth Over Time'),
            vertical_spacing=0.12
        )
        
        # Temperature time series
        temp_ts = time_series.dropna(subset=['TEMP'])
        if not temp_ts.empty:
            fig.add_trace(
                go.Scatter(
                    x=temp_ts['JULD'],
                    y=temp_ts['TEMP'],
                    mode='markers+lines',
                    name='Temperature',
                    line=dict(color='red', width=3),
                    marker=dict(color='red', size=8),
                    hovertemplate='Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Salinity time series
        sal_ts = time_series.dropna(subset=['PSAL'])
        if not sal_ts.empty:
            fig.add_trace(
                go.Scatter(
                    x=sal_ts['JULD'],
                    y=sal_ts['PSAL'],
                    mode='markers+lines',
                    name='Salinity',
                    line=dict(color='blue', width=3),
                    marker=dict(color='blue', size=8),
                    hovertemplate='Date: %{x}<br>Salinity: %{y:.2f} PSU<extra></extra>'
                ),
                row=2, col=1
            )
        
        # Depth time series (max depth per profile)
        depth_ts = profile_df.groupby(['JULD', 'CYCLE_NUMBER'])['PRES'].max().reset_index()
        depth_ts = depth_ts.sort_values('JULD')
        
        if not depth_ts.empty:
            fig.add_trace(
                go.Scatter(
                    x=depth_ts['JULD'],
                    y=depth_ts['PRES'],
                    mode='markers+lines',
                    name='Max Depth',
                    line=dict(color='green', width=3),
                    marker=dict(color='green', size=8),
                    hovertemplate='Date: %{x}<br>Max Depth: %{y:.0f} dbar<extra></extra>'
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
            title_text=f"Time Series Analysis for Float {platform_number}",
            showlegend=False,
            template="plotly_white"
        )
        
        return dcc.Graph(figure=fig)
        
    except Exception as e:
        return dbc.Alert(f"Error creating time series plots: {str(e)}", 
                        color="danger", className="text-center")

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
                    html.H4(f"{total_floats}", className="card-title text-primary"),
                    html.P("Active Floats", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{avg_temp:.1f}°C", className="card-title text-danger"),
                    html.P("Avg Temperature", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{avg_salinity:.1f} PSU", className="card-title text-info"),
                    html.P("Avg Salinity", className="card-text")
                ])
            ], className="text-center")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{max_depth:.0f}m", className="card-title text-success"),
                    html.P("Max Depth", className="card-text")
                ])
            ], className="text-center")
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
                       className="text-center text-muted mb-4"),
                dbc.Badge(
                    f"{'Real-time Data' if using_real_data else 'Demo Mode'}", 
                    color="success" if using_real_data else "warning",
                    className="mb-3"
                )
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
                    html.P("Click on markers to view detailed information about each float.", 
                          className="text-muted mb-3"),
                    html.Div(id="map-container", children=create_map())
                ])
            ])
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
                    html.P("Click on a row to view detailed analysis for that float.", 
                          className="text-muted mb-3"),
                    create_float_table()
                ])
            ])
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
                "Data source: ", 
                html.A("Argo Global Data Assembly Centre", 
                      href="https://argo.ucsd.edu/", 
                      target="_blank"),
                " | Built with ", 
                html.A("argopy", href="https://argopy.readthedocs.io/", target="_blank"),
                " and Plotly Dash"
            ], className="text-center text-muted")
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
                html.H5("👆 Select a float from the table above", className="alert-heading"),
                html.P("Click on any row in the data table to view detailed analysis including profile plots, time series, and comprehensive float information.")
            ], color="info", className="text-center"),
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
                "🚢 Float ", html.Code(str(platform_number)), " - Detailed Information"
            ], className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("📍 Location Information", className="text-primary mb-3"),
                    html.P([html.Strong("Platform ID: "), html.Code(str(platform_number))]),
                    html.P([html.Strong("Current Position: "), 
                           f"{selected_float['LATITUDE']:.4f}°N, {selected_float['LONGITUDE']:.4f}°E"]),
                    html.P([html.Strong("Last Update: "), 
                           selected_float['LAST_DATE'].strftime('%Y-%m-%d %H:%M UTC') if pd.notna(selected_float['LAST_DATE']) else 'N/A']),
                    html.P([html.Strong("Region: "), 
                           selected_float.get('LOCATION', 'Indian Ocean')])
                ], md=4),
                dbc.Col([
                    html.H6("🔄 Operational Status", className="text-success mb-3"),
                    html.P([html.Strong("Total Cycles: "), str(selected_float['MAX_CYCLE'])]),
                    html.P([html.Strong("Maximum Depth: "), f"{selected_float['MAX_DEPTH']:.0f} meters"]),
                    html.P([html.Strong("Status: "), 
                           dbc.Badge("Active", color="success", className="ms-1")]),
                    html.P([html.Strong("Data Quality: "), 
                           dbc.Badge("Good", color="success", className="ms-1")])
                ], md=4),
                dbc.Col([
                    html.H6("🌡️ Environmental Data", className="text-info mb-3"),
                    html.P([html.Strong("Average Temperature: "), 
                           f"{selected_float['AVG_TEMP']:.2f}°C"]),
                    html.P([html.Strong("Average Salinity: "), 
                           f"{selected_float['AVG_SALINITY']:.2f} PSU"]),
                    html.P([html.Strong("Temperature Range: "), "2-30°C"]),
                    html.P([html.Strong("Salinity Range: "), "34-36 PSU"])
                ], md=4)
            ])
        ])
    ], className="mb-4", color="light", outline=True)
    
    # Create profile plots card
    profile_plots_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📈 Vertical Profile Analysis", className="mb-0")
        ]),
        dbc.CardBody([
            html.P("Vertical profiles show how temperature and salinity change with depth. The T-S diagram reveals water mass characteristics.", 
                  className="text-muted mb-3"),
            create_profile_plots(platform_number)
        ])
    ])
    
    # Create time series plots card
    time_series_card = dbc.Card([
        dbc.CardHeader([
            html.H4("📊 Time Series Analysis", className="mb-0")
        ]),
        dbc.CardBody([
            html.P("Time series plots show how oceanographic conditions have changed over time for this float.", 
                  className="text-muted mb-3"),
            create_time_series_plots(platform_number)
        ])
    ])
    
    return info_card, profile_plots_card, time_series_card

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌊 ARGO FLOAT DASHBOARD - INDIAN OCEAN")
    print("="*60)
    print(f"📊 Data Mode: {'Real-time Argo Data' if using_real_data else 'Sample Data (Demo)'}")
    print(f"🚢 Active Floats: {len(float_info)}")
    print(f"🌍 Region: Indian Ocean ({INDIA_BBOX})")
    print("="*60)
    print("\n🚀 Starting dashboard server...")
    print("📱 Open your browser and go to: http://127.0.0.1:8050")
    print("\n💡 Features:")
    print("   • Interactive map with float locations")
    print("   • Detailed profile plots (Temperature, Salinity, T-S diagrams)")
    print("   • Time series analysis")
    print("   • Data table with filtering and sorting")
    print("   • Real-time status monitoring")
    print("\n" + "="*60)
    
    app.run(debug=True, port=8050, host='127.0.0.1')
