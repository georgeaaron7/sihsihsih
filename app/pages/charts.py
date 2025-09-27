"""
Historical Charts Page Layout
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.layout import create_page_header

def create_charts_page(dashboard):
    """Create the historical charts and analysis page"""
    float_info = dashboard.get_float_info()
    
    return html.Div([
        create_page_header(
            "📈 Historical Data Analysis",
            "Comprehensive time series analysis and trends",
            "Data Analytics Dashboard",
            "success"
        ),
        
        # Float selection section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-search me-2"),
                            "Select Float for Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("🚢 Choose Float:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='charts-float-dropdown',
                                    options=[
                                        {
                                            'label': f'Float {row["PLATFORM_NUMBER"]} - {row["LOCATION"]} ({row["AVG_TEMP"]:.1f}°C)', 
                                            'value': row["PLATFORM_NUMBER"]
                                        } 
                                        for _, row in float_info.iterrows()
                                    ],
                                    placeholder="Select a float to analyze...",
                                    className="mb-3"
                                )
                            ], md=6),
                            dbc.Col([
                                html.Label("📊 Analysis Type:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='analysis-type-dropdown',
                                    options=[
                                        {'label': '🌡️ Temperature Analysis', 'value': 'temperature'},
                                        {'label': '🧂 Salinity Analysis', 'value': 'salinity'},
                                        {'label': '🌊 Depth Analysis', 'value': 'depth'},
                                        {'label': '📈 Complete Analysis', 'value': 'complete'}
                                    ],
                                    value='complete',
                                    className="mb-3"
                                )
                            ], md=6)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label("📅 Time Range:", className="fw-bold"),
                                dcc.DatePickerRange(
                                    id='date-range-picker',
                                    start_date=(dashboard.get_summary_stats()['date_range']['start']),
                                    end_date=(dashboard.get_summary_stats()['date_range']['end']),
                                    display_format='YYYY-MM-DD',
                                    className="mb-3"
                                )
                            ], md=6),
                            dbc.Col([
                                html.Label("⚙️ Options:", className="fw-bold"),
                                dbc.Checklist(
                                    id='chart-options',
                                    options=[
                                        {"label": " Show trends", "value": "trends"},
                                        {"label": " Show anomalies", "value": "anomalies"},
                                        {"label": " Compare profiles", "value": "compare"}
                                    ],
                                    value=["trends"],
                                    className="mb-3"
                                )
                            ], md=6)
                        ])
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        # Charts section
        dbc.Row([
            dbc.Col([
                html.Div(id="historical-charts-content")
            ])
        ], className="mb-4"),
        
        # Comparative analysis section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-balance-scale me-2"),
                            "Multi-Float Comparison"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select floats to compare:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='comparison-floats-dropdown',
                                    options=[
                                        {
                                            'label': f'Float {row["PLATFORM_NUMBER"]} - {row["LOCATION"]}', 
                                            'value': row["PLATFORM_NUMBER"]
                                        } 
                                        for _, row in float_info.iterrows()
                                    ],
                                    placeholder="Choose multiple floats...",
                                    multi=True,
                                    className="mb-3"
                                )
                            ], md=8),
                            dbc.Col([
                                html.Label("Comparison metric:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='comparison-metric',
                                    options=[
                                        {'label': '🌡️ Temperature', 'value': 'temperature'},
                                        {'label': '🧂 Salinity', 'value': 'salinity'},
                                        {'label': '🌊 Profile Depth', 'value': 'depth'}
                                    ],
                                    value='temperature',
                                    className="mb-3"
                                )
                            ], md=4)
                        ]),
                        html.Div(id="comparison-charts")
                    ])
                ], className="shadow-sm")
            ])
        ], className="mb-4"),
        
        # Data export section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6([
                            html.I(className="fas fa-download me-2"),
                            "Export Data"
                        ], className="text-primary mb-3"),
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fas fa-file-csv me-1"),
                                "Export CSV"
                            ], color="success", outline=True),
                            dbc.Button([
                                html.I(className="fas fa-file-image me-1"),
                                "Export Charts"
                            ], color="info", outline=True),
                            dbc.Button([
                                html.I(className="fas fa-file-pdf me-1"),
                                "Generate Report"
                            ], color="danger", outline=True)
                        ])
                    ])
                ], className="shadow-sm")
            ])
        ])
    ])
