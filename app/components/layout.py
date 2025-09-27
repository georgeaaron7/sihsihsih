"""
Navigation and Layout Components
"""

import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    """Create the top navigation bar with logo and menu items"""
    return dbc.Navbar(
        dbc.Container([
            # Logo section (left side)
            dbc.Row([
                dbc.Col([
                    dbc.NavbarBrand([
                        html.Img(
                            src="/assets/logo.png",  # Placeholder for your logo
                            height="40px",
                            className="me-2",
                            style={'object-fit': 'contain'}
                        ),
                        html.Span([
                            html.I(className="fas fa-anchor me-2"),
                            "Argo Dashboard"
                        ], style={'font-weight': 'bold', 'font-size': '1.4rem'})
                    ], href="/", className="text-white text-decoration-none")
                ])
            ], align="center", className="flex-grow-1"),
            
            # Navigation menu (right side)
            dbc.Nav([
                dbc.NavItem([
                    dbc.NavLink([
                        html.I(className="fas fa-home me-2"),
                        "Home"
                    ], 
                    href="#", 
                    id="nav-home",
                    className="nav-link-modern",
                    active=True)
                ]),
                dbc.NavItem([
                    dbc.NavLink([
                        html.I(className="fas fa-map-marked-alt me-2"),
                        "Interactive Map"
                    ], 
                    href="#", 
                    id="nav-map",
                    className="nav-link-modern")
                ]),
                dbc.NavItem([
                    dbc.NavLink([
                        html.I(className="fas fa-chart-line me-2"),
                        "Historical Data"
                    ], 
                    href="#", 
                    id="nav-charts",
                    className="nav-link-modern")
                ]),
                dbc.NavItem([
                    dbc.NavLink([
                        html.I(className="fas fa-robot me-2"),
                        "AI Assistant",
                        dbc.Badge("Soon", color="warning", className="ms-2", style={'font-size': '0.7rem'})
                    ], 
                    href="#", 
                    id="nav-chatbot",
                    className="nav-link-modern",
                    disabled=True,
                    style={'opacity': '0.7'})
                ])
            ], navbar=True, className="ms-auto")
        ], fluid=True),
        color="primary",
        dark=True,
        className="shadow-sm navbar-modern",
        style={'min-height': '70px'}
    )

def create_footer():
    """Create the footer with team credits"""
    return html.Footer([
        dbc.Container([
            html.Hr(className="my-4"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("🌊 Argo Float Dashboard", className="text-primary mb-3"),
                        html.P([
                            "Real-time oceanographic data visualization for the Indian Ocean region. ",
                            "Powered by Argo Global Data Assembly Centre."
                        ], className="text-muted small mb-3"),
                        html.P([
                            html.Strong("Data Sources: "),
                            html.A("Argo GDAC", href="https://argo.ucsd.edu/", target="_blank", className="text-decoration-none"),
                            " • ",
                            html.A("ERDDAP", href="https://coastwatch.pfeg.noaa.gov/erddap/", target="_blank", className="text-decoration-none")
                        ], className="text-muted small")
                    ])
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.H6("🚀 Technologies", className="text-success mb-3"),
                        html.Div([
                            dbc.Badge("Python", color="info", className="me-2 mb-1"),
                            dbc.Badge("Dash", color="primary", className="me-2 mb-1"),
                            dbc.Badge("Plotly", color="secondary", className="me-2 mb-1"),
                            dbc.Badge("ArgoPy", color="success", className="me-2 mb-1"),
                            dbc.Badge("FastAPI", color="warning", className="me-2 mb-1"),
                            dbc.Badge("Bootstrap", color="dark", className="me-2 mb-1")
                        ])
                    ])
                ], md=6)
            ], className="mb-4"),
            
            # Team credits
            html.Div([
                html.Hr(className="my-3"),
                html.P([
                    html.I(className="fas fa-heart text-danger me-2"),
                    "Made with love by ",
                    html.Strong("Anuprabh, Aaron, Manvitha, Shreeya, Ashish and Disha"),
                    " 💙"
                ], className="text-center text-muted mb-2"),
                html.P([
                    html.Small([
                        "© 2025 Argo Dashboard Team • ",
                        "Smart India Hackathon 2025 • ",
                        "Indian Ocean Research Initiative"
                    ])
                ], className="text-center text-muted")
            ])
        ])
    ], className="bg-light mt-5 py-4")

def create_loading_spinner():
    """Create a loading spinner component"""
    return dbc.Spinner(
        html.Div([
            html.I(className="fas fa-water fa-2x text-primary mb-3"),
            html.H5("Loading oceanographic data...", className="text-muted")
        ], className="text-center p-4"),
        color="primary"
    )

def create_error_alert(message, details=None):
    """Create an error alert component"""
    content = [
        html.H5([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Oops! Something went wrong"
        ], className="alert-heading"),
        html.P(message, className="mb-0")
    ]
    
    if details:
        content.extend([
            html.Hr(),
            html.P([
                html.Strong("Details: "),
                html.Code(str(details))
            ], className="mb-0 small")
        ])
    
    return dbc.Alert(content, color="danger", className="m-4")

def create_info_card(title, value, icon, color="primary", subtitle=None):
    """Create an info card component"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.I(className=f"fas {icon} fa-2x text-{color}")
                ], className="text-center mb-2"),
                html.H3(str(value), className=f"text-{color} mb-1 text-center font-weight-bold"),
                html.P(title, className="text-muted mb-0 text-center small"),
                html.P(subtitle, className="text-muted mb-0 text-center x-small") if subtitle else None
            ])
        ])
    ], className="text-center shadow-sm h-100 card-hover")

def create_page_header(title, subtitle, badge_text=None, badge_color="info"):
    """Create a consistent page header"""
    return html.Div([
        html.Div([
            html.H1([
                title
            ], className="display-5 text-center mb-2 text-primary font-weight-bold"),
            html.H4(subtitle, className="text-center text-muted mb-3"),
            html.Div([
                dbc.Badge(badge_text, color=badge_color, className="mb-4")
            ], className="text-center") if badge_text else None
        ], className="text-center mb-4")
    ])
