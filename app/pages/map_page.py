"""
Map Page Layout
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.layout import create_page_header
from app.components.visualizations import create_interactive_map, create_plotly_interactive_map

def create_map_page(dashboard):
    """Create the dedicated map page"""
    float_info = dashboard.get_float_info()
    
    return html.Div([
        create_page_header(
            "🗺️ Interactive Ocean Map",
            "Explore Argo float locations across the Indian Ocean",
            "Real-time Positioning",
            "primary"
        ),
        
        # Map controls section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="fas fa-sliders-h me-2"),
                            "Map Controls & Filters"
                        ], className="text-primary mb-3"),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label("Temperature Filter:", className="fw-bold"),
                                dcc.RangeSlider(
                                    id='temp-filter',
                                    min=float_info['AVG_TEMP'].min(),
                                    max=float_info['AVG_TEMP'].max(),
                                    value=[float_info['AVG_TEMP'].min(), float_info['AVG_TEMP'].max()],
                                    marks={
                                        int(float_info['AVG_TEMP'].min()): f"{float_info['AVG_TEMP'].min():.0f}°C",
                                        int(float_info['AVG_TEMP'].max()): f"{float_info['AVG_TEMP'].max():.0f}°C"
                                    },
                                    tooltip={"placement": "bottom", "always_visible": True}
                                )
                            ], md=4),
                            dbc.Col([
                                html.Label("Region Filter:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='region-filter',
                                    options=[
                                        {'label': '🌊 All Regions', 'value': 'all'},
                                        {'label': '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Arabian Sea', 'value': 'Arabian Sea'},
                                        {'label': '🇮🇳 Bay of Bengal', 'value': 'Bay of Bengal'},
                                        {'label': '🌏 South Indian Ocean', 'value': 'South Indian Ocean'},
                                        {'label': '🏝️ Andaman Sea', 'value': 'Andaman Sea'}
                                    ],
                                    value='all',
                                    className="mb-2"
                                )
                            ], md=4),
                            dbc.Col([
                                html.Label("Map Type:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='map-type-selector',
                                    options=[
                                        {'label': '🗺️ Interactive (Plotly)', 'value': 'plotly'},
                                        {'label': '🌍 Traditional (Folium)', 'value': 'folium'}
                                    ],
                                    value='plotly',
                                    className="mb-2"
                                )
                            ], md=4)
                        ])
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        # Map section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4([
                                html.I(className="fas fa-globe-asia me-2"),
                                "Live Ocean Monitoring"
                            ], className="mb-0 d-inline"),
                            dbc.ButtonGroup([
                                dbc.Button([
                                    html.I(className="fas fa-expand-arrows-alt me-1"),
                                    "Fullscreen"
                                ], color="outline-primary", size="sm"),
                                dbc.Button([
                                    html.I(className="fas fa-download me-1"),
                                    "Export"
                                ], color="outline-success", size="sm")
                            ], className="float-end")
                        ], className="d-flex justify-content-between align-items-center")
                    ]),
                    dbc.CardBody([
                        # Legend and info
                        dbc.Row([
                            dbc.Col([
                                dbc.Alert([
                                    html.H6([
                                        html.I(className="fas fa-info-circle me-2"),
                                        "Navigation Tips"
                                    ], className="alert-heading mb-2"),
                                    html.Ul([
                                        html.Li("🖱️ Click markers for detailed float information"),
                                        html.Li("🔍 Use mouse wheel or +/- controls to zoom"),
                                        html.Li("🎨 Colors indicate temperature ranges (see legend)"),
                                        html.Li("🗺️ Switch map layers using the control panel"),
                                        html.Li("📱 Full-screen mode available for detailed analysis")
                                    ], className="mb-0 small")
                                ], color="info", className="mb-3")
                            ])
                        ]),
                        
                        # Map container (dynamically updated based on map type)
                        html.Div(
                            id="interactive-map-container",
                            children=create_plotly_interactive_map(float_info),  # Default to Plotly
                            style={'min-height': '600px'}
                        ),
                        
                        # Float click info display
                        html.Div(id="float-click-info", className="mt-3")
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-4"),
        
        # Statistics section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Regional Statistics"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div(id="regional-stats")
                    ])
                ], className="shadow-sm")
            ], md=12)
        ])
    ])
