"""
Home Page Layout and Components
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.layout import create_info_card, create_page_header
from app.components.visualizations import create_interactive_map, create_data_table

def create_home_page(dashboard):
    """Create the main home page content"""
    float_info = dashboard.get_float_info()
    stats = dashboard.get_summary_stats()
    
    return html.Div([
        # Hero section with quick stats
        dbc.Row([
            dbc.Col([
                create_info_card(
                    "Active Floats", 
                    stats['total_floats'], 
                    "fa-ship", 
                    "primary",
                    "Monitoring Indian Ocean"
                )
            ], md=3),
            dbc.Col([
                create_info_card(
                    "Avg Temperature", 
                    f"{stats['avg_temp']:.1f}°C", 
                    "fa-thermometer-half", 
                    "danger",
                    "Surface waters"
                )
            ], md=3),
            dbc.Col([
                create_info_card(
                    "Avg Salinity", 
                    f"{stats['avg_salinity']:.1f} PSU", 
                    "fa-tint", 
                    "info",
                    "Practical Salinity Units"
                )
            ], md=3),
            dbc.Col([
                create_info_card(
                    "Max Depth", 
                    f"{stats['max_depth']:.0f}m", 
                    "fa-anchor", 
                    "success",
                    "Deepest measurement"
                )
            ], md=3)
        ], className="mb-5"),
        
        # Quick insights section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="fas fa-lightbulb text-warning me-2"),
                            "Real-time Ocean Insights"
                        ], className="card-title"),
                        html.Div([
                            dbc.Badge("🌡️ Temperature Monitoring", color="light", className="me-2 mb-2"),
                            dbc.Badge("🧂 Salinity Analysis", color="light", className="me-2 mb-2"),
                            dbc.Badge("🌊 Depth Profiling", color="light", className="me-2 mb-2"),
                            dbc.Badge("📊 Historical Trends", color="light", className="me-2 mb-2")
                        ]),
                        html.P([
                            "Our Argo float network provides continuous monitoring of ocean conditions across the Indian Ocean. ",
                            "Each float autonomously collects temperature, salinity, and pressure measurements from surface to 2000m depth, ",
                            "helping scientists understand climate patterns and ocean health."
                        ], className="mt-3 text-muted")
                    ])
                ], className="shadow-sm border-0")
            ], md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="fas fa-globe-asia text-primary me-2"),
                            "Coverage Area"
                        ], className="card-title"),
                        html.Ul([
                            html.Li("Arabian Sea monitoring"),
                            html.Li("Bay of Bengal coverage"),
                            html.Li("South Indian Ocean"),
                            html.Li("Andaman Sea region")
                        ], className="mb-0"),
                        html.Hr(),
                        html.Small([
                            html.I(className="fas fa-clock me-1"),
                            f"Last updated: {stats['date_range']['end'].strftime('%Y-%m-%d')}"
                        ], className="text-muted")
                    ])
                ], className="shadow-sm border-0")
            ], md=4)
        ], className="mb-5"),
        
        # Interactive map section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-map-marked-alt me-2"),
                            "Interactive Float Map"
                        ], className="mb-0 text-primary")
                    ]),
                    dbc.CardBody([
                        dbc.Alert([
                            html.I(className="fas fa-info-circle me-2"),
                            html.Strong("Interactive Features: "),
                            "Click on any float marker for detailed information. Use map controls to zoom and explore different regions. ",
                            "Float colors indicate temperature ranges."
                        ], color="light", className="mb-3"),
                        create_interactive_map(float_info)
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-5"),
        
        # Data table section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-table me-2"),
                            "Float Data Overview"
                        ], className="mb-0 text-success")
                    ]),
                    dbc.CardBody([
                        dbc.Alert([
                            html.I(className="fas fa-mouse-pointer me-2"),
                            html.Strong("How to use: "),
                            "Click on any row to select a float and view detailed analysis below. ",
                            "Use column filters to search specific data. Sort by clicking column headers."
                        ], color="light", className="mb-3"),
                        create_data_table(float_info)
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-4"),
        
        # Selected float analysis section
        html.Div(id="selected-float-analysis")
    ])
