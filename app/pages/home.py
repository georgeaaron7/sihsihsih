"""
Home Page Layout and Components
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.layout import create_info_card, create_page_header
from app.components.visualizations import create_interactive_map, create_data_table

def create_home_page(dashboard):
    """Create the main home page content with ocean theme"""
    float_info = dashboard.get_float_info()
    stats = dashboard.get_summary_stats()
    
    return html.Div([
        # Hero section with ocean theme
        html.Div([
            dbc.Container([
                html.Div([
                    html.H1([
                        html.I(className="fas fa-water me-3", style={'color': '#4FC3F7'}),
                        "Discover the Ocean's Secrets"
                    ], className="display-3 text-white mb-4 font-weight-bold"),
                    html.P([
                        "Dive deep into the world's largest laboratory with Argo floats - autonomous robots exploring our oceans 24/7, ",
                        "revealing the mysteries of marine ecosystems and climate patterns across the Indian Ocean."
                    ], className="lead text-white mb-4", style={'font-size': '1.3rem'}),
                    dbc.Button([
                        html.I(className="fas fa-compass me-2"),
                        "Explore Ocean Data"
                    ], color="info", size="lg", className="me-3"),
                    dbc.Button([
                        html.I(className="fas fa-chart-line me-2"),
                        "View Analytics"
                    ], color="outline-light", size="lg")
                ], className="text-center py-5")
            ])
        ], style={
            'background': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4FC3F7 100%)',
            'min-height': '60vh',
            'display': 'flex',
            'align-items': 'center',
            'margin': '-2rem -15px 3rem -15px',
            'position': 'relative'
        }),
        
        # Stats cards with ocean theme
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-ship fa-3x text-primary mb-3 fw-bold"),
                            html.H2(stats['total_floats'], className="text-primary mb-2"),
                            html.H6("Active Floats", className="text-light mb-1 fw-bold"),
                            html.Small("Monitoring Indian Ocean", className="text-light")
                        ], className="text-center")
                    ])
                ], className="bg-light border-primary shadow-lg h-100")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-thermometer-half fa-3x text-danger mb-3"),
                            html.H2(f"{stats['avg_temp']:.1f}°C", className="text-danger mb-2"),
                            html.H6("Average Temperature", className="text-light mb-1 fw-bold"),
                            html.Small("Surface waters", className="text-light")
                        ], className="text-center")
                    ])
                ], className="bg-dark border-danger shadow-lg h-100")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-tint fa-3x text-info mb-3"),
                            html.H2(f"{stats['avg_salinity']:.1f}", className="text-info mb-2"),
                            html.H6("Average Salinity", className="text-light mb-1 fw-bold"),
                            html.Small("Practical Salinity Units", className="text-light")
                        ], className="text-center")
                    ])
                ], className="bg-dark border-info shadow-lg h-100")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-anchor fa-3x text-success mb-3"),
                            html.H2(f"{stats['max_depth']:.0f}m", className="text-success mb-2"),
                            html.H6("Maximum Depth", className="text-light mb-1 fw-bold"),
                            html.Small("Deepest measurement", className="text-light")
                        ], className="text-center")
                    ])
                ], className="bg-dark border-success shadow-lg h-100")
            ], md=3)
        ], className="mb-5"),
        
        # About Argo floats section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3([
                            html.I(className="fas fa-info-circle text-info me-3"),
                            "What are Argo Floats?"
                        ], className="text-light mb-4"),
                        html.P([
                            "Argo floats are sophisticated autonomous underwater vehicles that drift with ocean currents, ",
                            "diving and surfacing in a continuous cycle to collect crucial oceanographic data. ",
                            "These remarkable instruments are the backbone of global ocean observation."
                        ], className="text-light mb-4", style={'font-size': '1.1rem'}),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-arrows-alt-v fa-2x text-primary mb-3"),
                                    html.H5("Autonomous Profiling", className="text-info fw-bold"),
                                    html.P("Floats dive to 2000m depth, then surface to transmit data via satellite", 
                                           className="text-light small")
                                ], className="text-center")
                            ], md=4),
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-satellite fa-2x text-warning mb-3"),
                                    html.H5("Real-time Data", className="text-info fw-bold"),
                                    html.P("Continuous monitoring provides real-time ocean condition updates", 
                                           className="text-light small")
                                ], className="text-center")
                            ], md=4),
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-globe fa-2x text-success mb-3"),
                                    html.H5("Global Network", className="text-info fw-bold"),
                                    html.P("Over 4000 floats worldwide create comprehensive ocean coverage", 
                                           className="text-light small")
                                ], className="text-center")
                            ], md=4)
                        ])
                    ])
                ], className="bg-dark shadow-lg border-secondary")
            ])
        ], className="mb-5"),
        
        # Ocean science importance
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3([
                            html.I(className="fas fa-microscope text-warning me-3"),
                            "Why Ocean Data Matters"
                        ], className="text-light mb-4"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-cloud-sun fa-2x text-info mb-3"),
                                        html.H6("Climate Monitoring", className="text-light fw-bold"),
                                        html.P(
                                            "Track climate change through ocean temperature and salinity patterns", 
                                            className="text-light small mb-0"
                                        )
                                    ], className="text-center")
                                ], className="bg-primary border-0 h-100")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-fish fa-2x text-success mb-3"),
                                        html.H6("Marine Ecosystems", className="text-light fw-bold"),
                                        html.P("Understand how ocean conditions affect marine life and ecosystems", 
                                               className="text-light small mb-0")
                                    ], className="text-center")
                                ], className="bg-secondary border-0 h-100")
                            ], md=6)
                        ], className="mb-3"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-hurricane fa-2x text-danger mb-3"),
                                        html.H6("Weather Prediction", className="text-light fw-bold"),
                                        html.P("Improve weather forecasting and extreme event prediction", 
                                               className="text-light small mb-0")
                                    ], className="text-center")
                                ], className="bg-secondary border-0 h-100")
                            ], md=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-shipping-fast fa-2x text-primary mb-3"),
                                        html.H6("Maritime Safety", className="text-light fw-bold"),
                                        html.P("Support safe navigation and maritime operations worldwide", 
                                               className="text-light small mb-0")
                                    ], className="text-center")
                                ], className="bg-secondary border-0 h-100")
                            ], md=6)
                        ])
                    ])
                ], className="bg-dark shadow-lg border-secondary")
            ])
        ], className="mb-5"),
        
        # Data table section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-table me-2"),
                            "Live Float Data"
                        ], className="mb-0 text-info")
                    ], className="bg-secondary"),
                    dbc.CardBody([
                        dbc.Alert([
                            html.I(className="fas fa-mouse-pointer me-2"),
                            html.Strong("Interactive Table: "),
                            "Click on any row to select a float and view detailed analysis below. ",
                            "Use column filters to search specific data."
                        ], color="white", className="mb-3"),
                        create_data_table(float_info)
                    ])
                ], className="bg-light shadow-lg border-secondary")
            ])
        ], className="mb-4"),
        
        # Selected float analysis section
        html.Div(id="selected-float-analysis")
    ])
