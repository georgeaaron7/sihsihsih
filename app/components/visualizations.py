"""
Map and Visualization Components
"""

import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import requests
import logging

# Configure logging for API calls
logger = logging.getLogger(__name__)

def create_interactive_map(float_info):
    """Create an interactive Folium map with float locations"""
    # Create map centered on Indian Ocean
    m = folium.Map(
        location=[15, 78], 
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add different tile layers
    folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
    folium.TileLayer('Stamen Toner', name='Toner').add_to(m)
    folium.TileLayer('CartoDB positron', name='Light').add_to(m)
    
    # Add float markers
    for idx, row in float_info.iterrows():
        popup_content = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; width: 280px; padding: 10px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 15px; margin: -10px -10px 15px -10px; 
                        border-radius: 8px 8px 0 0;">
                <h3 style="margin: 0; font-size: 18px;">
                    <i class="fas fa-anchor"></i> Float {row['PLATFORM_NUMBER']}
                </h3>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">
                    <strong style="color: #495057;">📍 Position</strong><br>
                    <span style="font-size: 13px; color: #6c757d;">
                        {row['LATITUDE']:.3f}°N<br>
                        {row['LONGITUDE']:.3f}°E
                    </span>
                </div>
                <div style="background: #f8f9fa; padding: 10px; border-radius: 6px;">
                    <strong style="color: #495057;">📅 Updated</strong><br>
                    <span style="font-size: 13px; color: #6c757d;">
                        {row['LAST_DATE'].strftime('%Y-%m-%d')}
                    </span>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
                <div style="text-align: center; padding: 8px; background: #fff3cd; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #856404;">
                        {row['AVG_TEMP']:.1f}°C
                    </div>
                    <div style="font-size: 11px; color: #856404;">Temperature</div>
                </div>
                <div style="text-align: center; padding: 8px; background: #d1ecf1; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #0c5460;">
                        {row['AVG_SALINITY']:.1f}
                    </div>
                    <div style="font-size: 11px; color: #0c5460;">Salinity (PSU)</div>
                </div>
            </div>
            
            <div style="background: #e9ecef; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                <strong style="color: #495057;">🌊 Depth:</strong> {row['MAX_DEPTH']:.0f}m &nbsp;
                <strong style="color: #495057;">🔄 Cycles:</strong> {row['MAX_CYCLE']}
            </div>
            
            <div style="font-size: 12px; color: #6c757d; font-style: italic;">
                📍 {row['LOCATION']}
            </div>
        </div>
        """
        
        # Enhanced color coding by temperature
        temp = row['AVG_TEMP']
        if temp > 29:
            color = 'red'
            icon_color = 'white'
        elif temp > 27:
            color = 'orange'
            icon_color = 'black'
        elif temp > 25:
            color = 'green'
            icon_color = 'white'
        elif temp > 23:
            color = 'blue'
            icon_color = 'white'
        else:
            color = 'purple'
            icon_color = 'white'
        
        # Create custom marker
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"🚢 Float {row['PLATFORM_NUMBER']} • {temp:.1f}°C • {row['LOCATION']}",
            icon=folium.Icon(
                color=color, 
                icon='anchor', 
                prefix='fa',
                icon_color=icon_color
            )
        ).add_to(m)
    
    # Add enhanced legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 20px; left: 20px; width: 200px; 
                background: rgba(255, 255, 255, 0.95); 
                border: 2px solid #ccc; 
                z-index: 9999; 
                font-size: 13px; 
                padding: 15px; 
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="margin: 0 0 10px 0; color: #333; font-size: 16px;">
            🌡️ Temperature Legend
        </h4>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <i class="fas fa-anchor" style="color: red; width: 20px; margin-right: 8px;"></i>
            <span>Very Hot (>29°C)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <i class="fas fa-anchor" style="color: orange; width: 20px; margin-right: 8px;"></i>
            <span>Hot (27-29°C)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <i class="fas fa-anchor" style="color: green; width: 20px; margin-right: 8px;"></i>
            <span>Warm (25-27°C)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <i class="fas fa-anchor" style="color: blue; width: 20px; margin-right: 8px;"></i>
            <span>Cool (23-25°C)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <i class="fas fa-anchor" style="color: purple; width: 20px; margin-right: 8px;"></i>
            <span>Cold (<23°C)</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen button
    from folium import plugins
    plugins.Fullscreen().add_to(m)
    
    # Return as iframe
    map_html = m._repr_html_()
    return html.Iframe(
        srcDoc=map_html, 
        width='100%', 
        height='650px', 
        style={'border': 'none', 'border-radius': '8px'}
    )

def create_data_table(float_info):
    """Create an enhanced data table"""
    table_data = float_info.copy()
    table_data['LAST_DATE'] = table_data['LAST_DATE'].dt.strftime('%Y-%m-%d')
    table_data['MAX_DEPTH'] = table_data['MAX_DEPTH'].round(0)
    table_data['AVG_TEMP'] = table_data['AVG_TEMP'].round(1)
    table_data['AVG_SALINITY'] = table_data['AVG_SALINITY'].round(2)
    
    return dash_table.DataTable(
        id='float-table',
        columns=[
            {'name': '🚢 Platform ID', 'id': 'PLATFORM_NUMBER', 'type': 'numeric'},
            {'name': '📍 Latitude', 'id': 'LATITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
            {'name': '📍 Longitude', 'id': 'LONGITUDE', 'type': 'numeric', 'format': {'specifier': '.3f'}},
            {'name': '📅 Last Update', 'id': 'LAST_DATE'},
            {'name': '🔄 Cycles', 'id': 'MAX_CYCLE', 'type': 'numeric'},
            {'name': '🌊 Max Depth (m)', 'id': 'MAX_DEPTH', 'type': 'numeric'},
            {'name': '🌡️ Avg Temp (°C)', 'id': 'AVG_TEMP', 'type': 'numeric'},
            {'name': '🧂 Avg Salinity', 'id': 'AVG_SALINITY', 'type': 'numeric'},
            {'name': '📍 Location', 'id': 'LOCATION'},
        ],
        data=table_data.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        style_cell={
            'textAlign': 'center', 
            'fontSize': '12px', 
            'padding': '12px',
            'fontFamily': 'Segoe UI, Arial, sans-serif',
            'backgroundColor': 'black',
            'color': 'white'
        },
        style_header={
            'backgroundColor': '#667eea',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontSize': '13px',
            'padding': '15px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'black'
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} > 28'},
                'backgroundColor': 'black',
                'color': '#42a5f5',
                'fontWeight': 'bold'
            },
            {
                'if': {'column_id': 'AVG_TEMP', 'filter_query': '{AVG_TEMP} <= 24'},
                'backgroundColor': '#000000',
                'color': '#000000',
                'fontWeight': 'bold'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#667eea !important',
                'color': 'black',
            }
        ],
        page_size=12,
        sort_action="native",
        filter_action="native",
        style_table={
            'overflowX': 'auto',
            'border': '1px solid #dee2e6',
            'borderRadius': '8px'
        },
        css=[{
            'selector': '.dash-table-tooltip',
            'rule': 'background-color: #667eea; color: black;'
        }]
    )

def create_profile_plots(profile_df, platform_number):
    """Create enhanced profile plots"""
    if profile_df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle fa-2x mb-3"),
            html.H5("No Profile Data Available"),
            html.P("Unable to load profile data for this float. Please try selecting another float.")
        ], color="warning", className="text-center p-4")
    
    # Get the most recent profile
    latest_cycle = profile_df['CYCLE_NUMBER'].max()
    recent_data = profile_df[profile_df['CYCLE_NUMBER'] == latest_cycle].sort_values('PRES')
    
    # Create subplots with improved layout
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '🌡️ Temperature Profile', 
            '🧂 Salinity Profile', 
            '📊 T-S Diagram',
            '📈 Profile Comparison'
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # Temperature profile
    temp_data = recent_data.dropna(subset=['TEMP', 'PRES'])
    if not temp_data.empty:
        fig.add_trace(
            go.Scatter(
                x=temp_data['TEMP'],
                y=-temp_data['PRES'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#e74c3c', width=3),
                marker=dict(color='#e74c3c', size=5, symbol='circle'),
                hovertemplate='<b>Temperature Profile</b><br>Temp: %{x:.1f}°C<br>Depth: %{y:.0f}m<extra></extra>'
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
                mode='lines+markers',
                name='Salinity',
                line=dict(color='#3498db', width=3),
                marker=dict(color='#3498db', size=5, symbol='circle'),
                hovertemplate='<b>Salinity Profile</b><br>Salinity: %{x:.2f} PSU<br>Depth: %{y:.0f}m<extra></extra>'
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
                    colorscale='Viridis_r',
                    size=10,
                    colorbar=dict(
                        title="<b>Pressure<br>(dbar)</b>", 
                        x=1.02, 
                        len=0.4,
                        y=0.25
                    ),
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>T-S Diagram</b><br>Salinity: %{x:.2f} PSU<br>Temp: %{y:.1f}°C<br>Depth: %{marker.color:.0f}m<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Profile comparison (multiple cycles)
    cycles_to_show = profile_df['CYCLE_NUMBER'].unique()[-3:]  # Last 3 cycles
    colors = ['#e74c3c', '#f39c12', '#27ae60']
    
    for i, cycle in enumerate(cycles_to_show):
        cycle_data = profile_df[profile_df['CYCLE_NUMBER'] == cycle].sort_values('PRES')
        cycle_temp = cycle_data.dropna(subset=['TEMP', 'PRES'])
        
        if not cycle_temp.empty:
            fig.add_trace(
                go.Scatter(
                    x=cycle_temp['TEMP'],
                    y=-cycle_temp['PRES'],
                    mode='lines',
                    name=f'Cycle {cycle}',
                    line=dict(color=colors[i % len(colors)], width=2),
                    opacity=0.8,
                    hovertemplate=f'<b>Cycle {cycle}</b><br>Temp: %{{x:.1f}}°C<br>Depth: %{{y:.0f}}m<extra></extra>'
                ),
                row=2, col=2
            )
    
    # Update layout with modern styling
    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_xaxes(title_text="Salinity (PSU)", row=1, col=2, showgrid=True, gridcolor='lightgray')
    fig.update_xaxes(title_text="Salinity (PSU)", row=2, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_xaxes(title_text="Temperature (°C)", row=2, col=2, showgrid=True, gridcolor='lightgray')
    
    fig.update_yaxes(title_text="Depth (m)", row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Depth (m)", row=1, col=2, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Temperature (°C)", row=2, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Depth (m)", row=2, col=2, showgrid=True, gridcolor='lightgray')
    
    fig.update_layout(
        height=800,
        title={
            'text': f"🔬 Comprehensive Profile Analysis - Float {platform_number} (Latest: Cycle {latest_cycle})",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=True,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return dcc.Graph(figure=fig, className="shadow-sm")

def create_time_series_plots(profile_df, platform_number):
    """Create enhanced time series plots"""
    if profile_df.empty:
        return dbc.Alert([
            html.I(className="fas fa-info-circle fa-2x mb-3"),
            html.H5("No Time Series Data Available"),
            html.P("Unable to load time series data for this float.")
        ], color="warning", className="text-center p-4")
    
    # Create time series data
    surface_data = profile_df[profile_df['PRES'] <= 50]
    time_series = surface_data.groupby(['JULD', 'CYCLE_NUMBER']).agg({
        'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
        'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
    }).reset_index()
    
    depth_series = profile_df.groupby(['JULD', 'CYCLE_NUMBER'])['PRES'].max().reset_index()
    
    time_series = time_series.sort_values('JULD')
    depth_series = depth_series.sort_values('JULD')
    
    # Create enhanced subplots
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            '🌡️ Surface Temperature Evolution', 
            '🧂 Surface Salinity Evolution', 
            '🌊 Maximum Profile Depth'
        ),
        vertical_spacing=0.08
    )
    
    # Temperature time series with trend
    temp_clean = time_series.dropna(subset=['TEMP'])
    if not temp_clean.empty:
        fig.add_trace(
            go.Scatter(
                x=temp_clean['JULD'],
                y=temp_clean['TEMP'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#e74c3c', width=3),
                marker=dict(color='#e74c3c', size=8, symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(231, 76, 60, 0.1)',
                hovertemplate='<b>Surface Temperature</b><br>Date: %{x}<br>Temperature: %{y:.1f}°C<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Salinity time series
    sal_clean = time_series.dropna(subset=['PSAL'])
    if not sal_clean.empty:
        fig.add_trace(
            go.Scatter(
                x=sal_clean['JULD'],
                y=sal_clean['PSAL'],
                mode='lines+markers',
                name='Salinity',
                line=dict(color='#3498db', width=3),
                marker=dict(color='#3498db', size=8, symbol='circle'),
                fill='tonexty',
                fillcolor='rgba(52, 152, 219, 0.1)',
                hovertemplate='<b>Surface Salinity</b><br>Date: %{x}<br>Salinity: %{y:.2f} PSU<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Depth time series
    if not depth_series.empty:
        fig.add_trace(
            go.Scatter(
                x=depth_series['JULD'],
                y=depth_series['PRES'],
                mode='lines+markers',
                name='Max Depth',
                line=dict(color='#27ae60', width=3),
                marker=dict(color='#27ae60', size=8, symbol='diamond'),
                fill='tozeroy',
                fillcolor='rgba(39, 174, 96, 0.1)',
                hovertemplate='<b>Profile Depth</b><br>Date: %{x}<br>Max Depth: %{y:.0f} dbar<extra></extra>'
            ),
            row=3, col=1
        )
    
    # Update layout
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Salinity (PSU)", row=2, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Pressure (dbar)", row=3, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_xaxes(title_text="Date", row=3, col=1, showgrid=True, gridcolor='lightgray')
    
    fig.update_layout(
        height=900,
        title={
            'text': f"📈 Historical Analysis - Float {platform_number} Evolution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        showlegend=False,
        template="plotly_white"
    )
    
    return dcc.Graph(figure=fig, className="shadow-sm")

def create_plotly_interactive_map(float_info):
    """Create an interactive Plotly map with float locations that can trigger API callbacks"""
    
    # Prepare data for plotting
    float_data = float_info.copy()
    
    # Color mapping based on temperature
    def get_temp_color(temp):
        if temp > 29:
            return 'red'
        elif temp > 27:
            return 'orange'
        elif temp > 25:
            return 'green'
        elif temp > 23:
            return 'blue'
        else:
            return 'purple'
    
    float_data['color'] = float_data['AVG_TEMP'].apply(get_temp_color)
    float_data['size'] = 15  # Marker size
    
    # Create hover text
    float_data['hover_text'] = float_data.apply(lambda row: 
        f"<b>Float {row['PLATFORM_NUMBER']}</b><br>" +
        f"📍 {row['LATITUDE']:.3f}°N, {row['LONGITUDE']:.3f}°E<br>" +
        f"🌡️ Temperature: {row['AVG_TEMP']:.1f}°C<br>" +
        f"🧂 Salinity: {row['AVG_SALINITY']:.1f} PSU<br>" +
        f"⚓ Max Depth: {row['MAX_DEPTH']:.0f}m<br>" +
        f"📅 Last Update: {row['LAST_DATE'].strftime('%Y-%m-%d')}<br>" +
        f"📍 {row['LOCATION']}", axis=1)
    
    # Create the Plotly figure
    fig = go.Figure()
    
    # Add float markers grouped by color for legend
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    color_labels = {
        'red': 'Very Hot (>29°C)',
        'orange': 'Hot (27-29°C)',
        'green': 'Warm (25-27°C)',
        'blue': 'Cool (23-25°C)',
        'purple': 'Cold (<23°C)'
    }
    
    for color in colors:
        color_data = float_data[float_data['color'] == color]
        if not color_data.empty:
            fig.add_trace(go.Scattermapbox(
                lat=color_data['LATITUDE'],
                lon=color_data['LONGITUDE'],
                mode='markers',
                marker=dict(
                    size=15,
                    color=color,
                    opacity=0.8,
                    symbol='circle'
                ),
                text=color_data['hover_text'],
                hovertemplate='%{text}<extra></extra>',
                customdata=color_data['PLATFORM_NUMBER'],
                name=color_labels[color],
                showlegend=True
            ))
    
    # Update layout for the map
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=15, lon=78),
            zoom=4
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return dcc.Graph(
        id='plotly-float-map',
        figure=fig,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        },
        style={'height': '600px'}
    )
