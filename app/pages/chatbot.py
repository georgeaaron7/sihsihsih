"""
AI Assistant/Chatbot Page Layout
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.layout import create_page_header

def create_chatbot_page():
    """Create the AI assistant/chatbot page"""
    return html.Div([
        create_page_header(
            "🤖 AI Ocean Assistant",
            "Intelligent analysis and insights coming soon",
            "Under Development",
            "warning"
        ),
        
        # Coming soon section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-robot", style={'fontSize': '4rem', 'color': '#6c757d'}),
                            html.H3("AI Assistant Coming Soon!", className="mt-3 mb-3"),
                            html.P([
                                "We're developing an intelligent assistant to help you analyze oceanographic data ",
                                "and answer questions about Argo floats and ocean conditions."
                            ], className="lead text-muted")
                        ], className="text-center mb-4"),
                        
                        html.Hr(),
                        
                        html.H5("🚀 Planned Features:", className="text-primary mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-comments fa-2x text-primary mb-2"),
                                        html.H6("Natural Language Queries", className="card-title"),
                                        html.P("Ask questions in plain English about ocean data, float status, and trends.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-chart-line fa-2x text-success mb-2"),
                                        html.H6("Automated Analysis", className="card-title"),
                                        html.P("Get instant insights about temperature anomalies, trends, and data quality.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-brain fa-2x text-info mb-2"),
                                        html.H6("Smart Recommendations", className="card-title"),
                                        html.P("Receive suggestions for further analysis and data exploration.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4)
                        ], className="mb-4"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-book fa-2x text-warning mb-2"),
                                        html.H6("Educational Content", className="card-title"),
                                        html.P("Learn about oceanography concepts and Argo float technology.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-code fa-2x text-danger mb-2"),
                                        html.H6("API Integration", className="card-title"),
                                        html.P("Connect with external oceanographic databases and research tools.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.I(className="fas fa-bell fa-2x text-primary mb-2"),
                                        html.H6("Smart Alerts", className="card-title"),
                                        html.P("Get notified about significant changes in ocean conditions.", 
                                               className="card-text small")
                                    ])
                                ], className="text-center h-100 border-0 shadow-sm")
                            ], md=4)
                        ])
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-4"),
        
        # Mock chatbot interface preview
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-eye me-2"),
                            "Interface Preview"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.P("Here's what the AI assistant interface will look like:", className="text-muted mb-3"),
                        
                        # Mock chat interface
                        dbc.Card([
                            dbc.CardHeader([
                                html.H6([
                                    html.I(className="fas fa-robot me-2 text-primary"),
                                    "Ocean AI Assistant",
                                    dbc.Badge("PREVIEW", color="warning", className="ms-2")
                                ], className="mb-0")
                            ]),
                            dbc.CardBody([
                                # Chat messages
                                html.Div([
                                    # AI message
                                    dbc.Alert([
                                        html.Div([
                                            html.Strong([
                                                html.I(className="fas fa-robot me-2"),
                                                "Ocean AI:"
                                            ]),
                                            html.P([
                                                "Hello! I'm your Ocean AI Assistant. I can help you understand Argo float data, ",
                                                "explain oceanographic concepts, and provide insights about marine conditions. ",
                                                "What would you like to know?"
                                            ], className="mb-0 mt-2")
                                        ])
                                    ], color="light", className="mb-3"),
                                    
                                    # User message
                                    dbc.Alert([
                                        html.Div([
                                            html.Strong([
                                                html.I(className="fas fa-user me-2"),
                                                "You:"
                                            ]),
                                            html.P("What causes the temperature to drop with depth in the ocean?", 
                                                   className="mb-0 mt-2")
                                        ])
                                    ], color="primary", className="mb-3"),
                                    
                                    # AI response
                                    dbc.Alert([
                                        html.Div([
                                            html.Strong([
                                                html.I(className="fas fa-robot me-2"),
                                                "Ocean AI:"
                                            ]),
                                            html.P([
                                                "Great question! Ocean temperature decreases with depth due to several factors: ",
                                                "1) Solar heating primarily affects surface waters, 2) Density stratification keeps ",
                                                "warm water on top, and 3) Limited mixing between layers. This creates the ",
                                                "'thermocline' - a zone of rapid temperature change typically between 200-1000m depth."
                                            ], className="mb-0 mt-2")
                                        ])
                                    ], color="light", className="mb-3")
                                ], style={
                                    'height': '300px', 
                                    'overflowY': 'auto', 
                                    'border': '1px solid #dee2e6', 
                                    'padding': '15px', 
                                    'backgroundColor': '#f8f9fa',
                                    'borderRadius': '8px'
                                }),
                                
                                html.Hr(),
                                
                                # Input area (disabled)
                                dbc.InputGroup([
                                    dbc.Input(
                                        placeholder="Ask me about ocean data, Argo floats, or oceanography...", 
                                        disabled=True,
                                        style={'borderRadius': '20px 0 0 20px'}
                                    ),
                                    dbc.Button([
                                        html.I(className="fas fa-paper-plane")
                                    ], color="primary", disabled=True, style={'borderRadius': '0 20px 20px 0'})
                                ])
                            ])
                        ], className="shadow-sm")
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-4"),
        
        # Development timeline
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-calendar-alt me-2"),
                            "Development Timeline"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            html.H6("Phase 1", className="text-primary"),
                                            html.P("Basic Q&A functionality", className="small mb-1"),
                                            dbc.Progress(value=75, color="primary", className="mb-2"),
                                            html.Small("Expected: Q1 2025", className="text-muted")
                                        ])
                                    ], className="text-center border-0 shadow-sm")
                                ], md=3),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            html.H6("Phase 2", className="text-info"),
                                            html.P("Data analysis automation", className="small mb-1"),
                                            dbc.Progress(value=40, color="info", className="mb-2"),
                                            html.Small("Expected: Q2 2025", className="text-muted")
                                        ])
                                    ], className="text-center border-0 shadow-sm")
                                ], md=3),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            html.H6("Phase 3", className="text-warning"),
                                            html.P("Advanced ML insights", className="small mb-1"),
                                            dbc.Progress(value=15, color="warning", className="mb-2"),
                                            html.Small("Expected: Q3 2025", className="text-muted")
                                        ])
                                    ], className="text-center border-0 shadow-sm")
                                ], md=3),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            html.H6("Phase 4", className="text-success"),
                                            html.P("Full AI integration", className="small mb-1"),
                                            dbc.Progress(value=5, color="success", className="mb-2"),
                                            html.Small("Expected: Q4 2025", className="text-muted")
                                        ])
                                    ], className="text-center border-0 shadow-sm")
                                ], md=3)
                            ])
                        ])
                    ])
                ], className="shadow border-0")
            ])
        ], className="mb-4"),
        
        # Contact section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6([
                            html.I(className="fas fa-envelope me-2"),
                            "Stay Updated"
                        ], className="text-primary mb-3"),
                        html.P("Want to be notified when the AI assistant is ready?", className="mb-3"),
                        dbc.InputGroup([
                            dbc.Input(placeholder="Enter your email for updates..."),
                            dbc.Button("Notify Me", color="primary")
                        ], className="mb-3"),
                        html.Small("We'll only send updates about major feature releases.", className="text-muted")
                    ])
                ], className="shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6([
                            html.I(className="fas fa-lightbulb me-2"),
                            "Suggest Features"
                        ], className="text-success mb-3"),
                        html.P("Have ideas for the AI assistant?", className="mb-3"),
                        dbc.Textarea(placeholder="Tell us what features you'd like to see..."),
                        dbc.Button("Submit Suggestion", color="success", className="mt-3", size="sm")
                    ])
                ], className="shadow-sm")
            ], md=6)
        ])
    ])
