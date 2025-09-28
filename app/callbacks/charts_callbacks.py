"""
Callbacks for the historical charts page
"""

from dash import Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def register_charts_callbacks(app, dashboard):
    @app.callback(
        Output("historical-charts-content", "children"),
        [
            Input("charts-float-dropdown", "value"),
            Input("analysis-type-dropdown", "value"),
            Input("date-range-picker", "start_date"),
            Input("date-range-picker", "end_date"),
            Input("chart-options", "value")
        ]
    )
    def update_charts(float_id, analysis_type, start_date, end_date, options):
        if not float_id:
            return dbc.Alert(
                "👆 Select a float from the dropdown above to view analysis",
                color="info"
            )

        profile_data = dashboard.get_profile_data()
        float_data = profile_data[profile_data['PLATFORM_NUMBER'] == float_id]
        
        if float_data.empty:
            return dbc.Alert(
                "No data available for the selected float",
                color="warning"
            )
            
        # Filter by date range if provided
        if start_date and end_date:
            float_data = float_data[
                (float_data['JULD'] >= start_date) &
                (float_data['JULD'] <= end_date)
            ]

        cards = []
        
        if analysis_type in ['temperature', 'complete']:
            fig_temp = create_temperature_plot(float_data, show_trends='trends' in options)
            cards.append(
                dbc.Card([
                    dbc.CardHeader("🌡️ Temperature Analysis"),
                    dbc.CardBody([dcc.Graph(figure=fig_temp)])
                ], className="mb-4")
            )
            
        if analysis_type in ['salinity', 'complete']:
            fig_sal = create_salinity_plot(float_data, show_trends='trends' in options)
            cards.append(
                dbc.Card([
                    dbc.CardHeader("🧂 Salinity Analysis"),
                    dbc.CardBody([dcc.Graph(figure=fig_sal)])
                ], className="mb-4")
            )
            
        if analysis_type in ['depth', 'complete']:
            fig_depth = create_depth_plot(float_data, show_trends='trends' in options)
            cards.append(
                dbc.Card([
                    dbc.CardHeader("🌊 Depth Analysis"),
                    dbc.CardBody([dcc.Graph(figure=fig_depth)])
                ], className="mb-4")
            )
            
        return html.Div(cards)

    @app.callback(
        Output("comparison-charts", "children"),
        [
            Input("comparison-floats-dropdown", "value"),
            Input("comparison-metric", "value")
        ]
    )
    def update_comparison(float_ids, metric):
        if not float_ids or len(float_ids) < 2:
            return dbc.Alert(
                "Select at least two floats to compare",
                color="info"
            )
            
        profile_data = dashboard.get_profile_data()
        fig = create_comparison_plot(profile_data, float_ids, metric)
        
        return dcc.Graph(figure=fig)

def create_temperature_plot(data, show_trends=True):
    """Create temperature analysis plot"""
    surface_data = data[data['PRES'] <= 50].groupby('JULD')['TEMP'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=surface_data['JULD'],
            y=surface_data['TEMP'],
            mode='lines+markers',
            name='Surface Temperature',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        )
    )
    
    if show_trends:
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=surface_data['JULD'],
                y=surface_data['TEMP'].rolling(window=5).mean(),
                mode='lines',
                name='Moving Average',
                line=dict(color='rgba(255,0,0,0.3)', width=3, dash='dot')
            )
        )
    
    fig.update_layout(
        title="Surface Temperature Over Time",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        template="plotly_white",
        height=500
    )
    
    return fig

def create_salinity_plot(data, show_trends=True):
    """Create salinity analysis plot"""
    surface_data = data[data['PRES'] <= 50].groupby('JULD')['PSAL'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=surface_data['JULD'],
            y=surface_data['PSAL'],
            mode='lines+markers',
            name='Surface Salinity',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        )
    )
    
    if show_trends:
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=surface_data['JULD'],
                y=surface_data['PSAL'].rolling(window=5).mean(),
                mode='lines',
                name='Moving Average',
                line=dict(color='rgba(0,0,255,0.3)', width=3, dash='dot')
            )
        )
    
    fig.update_layout(
        title="Surface Salinity Over Time",
        xaxis_title="Date",
        yaxis_title="Salinity (PSU)",
        template="plotly_white",
        height=500
    )
    
    return fig

def create_depth_plot(data, show_trends=True):
    """Create depth analysis plot"""
    max_depth = data.groupby('JULD')['PRES'].max().reset_index()
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=max_depth['JULD'],
            y=max_depth['PRES'],
            mode='lines+markers',
            name='Maximum Depth',
            line=dict(color='green', width=2),
            marker=dict(size=6)
        )
    )
    
    if show_trends:
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=max_depth['JULD'],
                y=max_depth['PRES'].rolling(window=5).mean(),
                mode='lines',
                name='Moving Average',
                line=dict(color='rgba(0,255,0,0.3)', width=3, dash='dot')
            )
        )
    
    fig.update_layout(
        title="Profile Depth Over Time",
        xaxis_title="Date",
        yaxis_title="Depth (m)",
        yaxis_autorange="reversed",
        template="plotly_white",
        height=500
    )
    
    return fig

def create_comparison_plot(data, float_ids, metric):
    """Create comparison plot for multiple floats"""
    fig = go.Figure()
    
    for float_id in float_ids:
        float_data = data[data['PLATFORM_NUMBER'] == float_id]
        surface_data = float_data[float_data['PRES'] <= 50]
        
        if metric == 'temperature':
            y_data = surface_data.groupby('JULD')['TEMP'].mean().reset_index()
            title = "Temperature Comparison"
            y_title = "Temperature (°C)"
            
        elif metric == 'salinity':
            y_data = surface_data.groupby('JULD')['PSAL'].mean().reset_index()
            title = "Salinity Comparison"
            y_title = "Salinity (PSU)"
            
        else:  # depth
            y_data = float_data.groupby('JULD')['PRES'].max().reset_index()
            title = "Profile Depth Comparison"
            y_title = "Depth (m)"
        
        fig.add_trace(
            go.Scatter(
                x=y_data['JULD'],
                y=y_data[metric.upper() if metric != 'depth' else 'PRES'],
                mode='lines+markers',
                name=f'Float {float_id}',
                marker=dict(size=6)
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_title,
        template="plotly_white",
        height=600
    )
    
    if metric == 'depth':
        fig.update_layout(yaxis_autorange="reversed")
    
    return fig