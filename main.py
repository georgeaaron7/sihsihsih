"""
Main Dash Application
Modular Argo Float Dashboard
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# Import modules
from app.data.argo_data import ArgoFloatDashboard
from app.components.layout import create_navbar, create_footer, create_loading_spinner, create_error_alert
from app.components.visualizations import create_profile_plots, create_time_series_plots
from app.pages.home import create_home_page
from app.pages.map_page import create_map_page
from app.pages.charts import create_charts_page
from app.pages.chatbot import create_chatbot_page

# Initialize the Dash app with modern theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    title="Argo Float Dashboard - Indian Ocean"
)

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            
            .navbar-modern {
                background: var(--primary-gradient) !important;
                backdrop-filter: blur(10px);
            }
            
            .nav-link-modern {
                transition: all 0.3s ease;
                border-radius: 8px;
                margin: 0 5px;
                font-weight: 500;
            }
            
            .nav-link-modern:hover {
                background-color: rgba(255, 255, 255, 0.2) !important;
                transform: translateY(-2px);
                color: white !important;
            }
            
            .nav-link-modern.active {
                background-color: rgba(255, 255, 255, 0.3) !important;
                color: white !important;
                font-weight: 600;
            }
            
            .card {
                border: none;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                background: rgba(255, 255, 255, 0.95);
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            }
            
            .card-hover:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
            }
            
            .btn {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                transform: translateY(-2px);
            }
            
            .badge {
                border-radius: 6px;
                font-weight: 500;
            }
            
            .alert {
                border: none;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            
            /* Dash table styling */
            .dash-table-container {
                border-radius: 12px;
                overflow: hidden;
            }
            
            /* Loading spinner */
            .dash-spinner {
                margin: 50px auto;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-gradient);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            /* Animation classes */
            .fade-in {
                animation: fadeIn 0.5s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Initialize dashboard data
dashboard = ArgoFloatDashboard()

# App layout
app.layout = html.Div([
    # Store for current page
    dcc.Store(id='current-page', data='home'),
    dcc.Store(id='selected-float', data=None),
    
    # Navigation
    create_navbar(),
    
    # Main content container
    dbc.Container([
        html.Div(id='page-content', className='fade-in')
    ], fluid=True, className='main-content'),
    
    # Footer
    create_footer()
])

# Navigation callback
@app.callback(
    [Output('current-page', 'data'),
     Output('page-content', 'children')],
    [Input('nav-home', 'n_clicks'),
     Input('nav-map', 'n_clicks'),
     Input('nav-charts', 'n_clicks'),
     Input('nav-chatbot', 'n_clicks')],
    [State('current-page', 'data')]
)
def navigate_pages(home_clicks, map_clicks, charts_clicks, chatbot_clicks, current_page):
    """Handle page navigation"""
    ctx = callback_context
    
    if not ctx.triggered:
        return 'home', create_home_page(dashboard)
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        if button_id == 'nav-home':
            return 'home', create_home_page(dashboard)
        elif button_id == 'nav-map':
            return 'map', create_map_page(dashboard)
        elif button_id == 'nav-charts':
            return 'charts', create_charts_page(dashboard)
        elif button_id == 'nav-chatbot':
            return 'chatbot', create_chatbot_page()
        else:
            return current_page, create_home_page(dashboard)
    except Exception as e:
        return current_page, create_error_alert(
            "Failed to load page content", 
            str(e)
        )

# Home page float selection callback
@app.callback(
    [Output('selected-float-analysis', 'children'),
     Output('selected-float', 'data')],
    [Input('float-table', 'selected_rows')],
    [State('current-page', 'data')]
)
def update_float_analysis(selected_rows, current_page):
    """Update float analysis when table row is selected"""
    if current_page != 'home' or not selected_rows:
        return html.Div(), None
    
    try:
        selected_idx = selected_rows[0]
        float_info = dashboard.get_float_info()
        selected_float = float_info.iloc[selected_idx]
        platform_number = selected_float['PLATFORM_NUMBER']
        
        # Get profile data
        profile_df = dashboard.get_float_profile_data(platform_number)
        
        # Create detailed analysis
        analysis_content = html.Div([
            # Float info card
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-ship me-2"),
                        f"Float {platform_number} - Detailed Analysis"
                    ], className="mb-0 text-primary")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("📍 Location Details", className="text-info mb-3"),
                            html.P([html.Strong("Platform ID: "), html.Code(str(platform_number))]),
                            html.P([html.Strong("Position: "), 
                                   f"{selected_float['LATITUDE']:.4f}°N, {selected_float['LONGITUDE']:.4f}°E"]),
                            html.P([html.Strong("Region: "), selected_float['LOCATION']]),
                            html.P([html.Strong("Last Update: "), 
                                   selected_float['LAST_DATE'].strftime('%Y-%m-%d')])
                        ], md=4),
                        dbc.Col([
                            html.H6("🔄 Operational Status", className="text-success mb-3"),
                            html.P([html.Strong("Total Cycles: "), str(selected_float['MAX_CYCLE'])]),
                            html.P([html.Strong("Max Depth: "), f"{selected_float['MAX_DEPTH']:.0f}m"]),
                            html.P([html.Strong("Status: "), 
                                   dbc.Badge("Active", color="success")]),
                            html.P([html.Strong("Data Quality: "), 
                                   dbc.Badge("Excellent", color="success")])
                        ], md=4),
                        dbc.Col([
                            html.H6("🌡️ Environmental Data", className="text-warning mb-3"),
                            html.P([html.Strong("Avg Temperature: "), 
                                   f"{selected_float['AVG_TEMP']:.2f}°C"]),
                            html.P([html.Strong("Avg Salinity: "), 
                                   f"{selected_float['AVG_SALINITY']:.2f} PSU"]),
                            html.P([html.Strong("Water Type: "), 
                                   "Tropical" if selected_float['AVG_TEMP'] > 26 else "Subtropical"]),
                            html.P([html.Strong("Profiles: "), 
                                   str(len(profile_df['CYCLE_NUMBER'].unique()))])
                        ], md=4)
                    ])
                ])
            ], className="shadow mb-4"),
            
            # Profile plots
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-area me-2"),
                        "Vertical Profile Analysis"
                    ], className="mb-0 text-success")
                ]),
                dbc.CardBody([
                    create_profile_plots(profile_df, platform_number)
                ])
            ], className="shadow mb-4"),
            
            # Time series plots
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-line me-2"),
                        "Time Series Analysis"
                    ], className="mb-0 text-info")
                ]),
                dbc.CardBody([
                    create_time_series_plots(profile_df, platform_number)
                ])
            ], className="shadow")
        ])
        
        return analysis_content, platform_number
        
    except Exception as e:
        return create_error_alert(
            "Failed to load float analysis", 
            str(e)
        ), None

# Charts page callback
@app.callback(
    Output('historical-charts-content', 'children'),
    [Input('charts-float-dropdown', 'value'),
     Input('analysis-type-dropdown', 'value')],
    [State('current-page', 'data')]
)
def update_charts_page(selected_float, analysis_type, current_page):
    """Update charts page content"""
    if current_page != 'charts' or not selected_float:
        return dbc.Alert([
            html.I(className="fas fa-info-circle fa-2x mb-3"),
            html.H5("Select a Float"),
            html.P("Choose a float from the dropdown above to view historical analysis.")
        ], color="info", className="text-center p-4")
    
    try:
        profile_df = dashboard.get_float_profile_data(selected_float)
        
        if analysis_type == 'complete':
            return html.Div([
                create_profile_plots(profile_df, selected_float),
                html.Hr(className="my-4"),
                create_time_series_plots(profile_df, selected_float)
            ])
        elif analysis_type == 'temperature':
            return create_time_series_plots(profile_df, selected_float)
        else:
            return create_profile_plots(profile_df, selected_float)
            
    except Exception as e:
        return create_error_alert(
            "Failed to load charts", 
            str(e)
        )

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌊 MODULAR ARGO FLOAT DASHBOARD - INDIAN OCEAN")
    print("="*70)
    print("📊 Mode: Enhanced Interactive Dashboard with Modular Architecture")
    print(f"🚢 Active Floats: {len(dashboard.get_float_info())}")
    print("🌍 Region: Indian Ocean (Deep Water Positioning)")
    print("🎨 UI: Modern Bootstrap Theme with Animations")
    print("⚡ Architecture: Modular Components & Pages")
    print("="*70)
    print("\n🚀 Starting dashboard server...")
    print("📱 Open your browser: http://127.0.0.1:8060")
    print("\n💡 New Features:")
    print("   • 🧩 Modular code architecture")
    print("   • 🎨 Modern UI with gradients & animations")
    print("   • 🗺️ Enhanced interactive map with layers")
    print("   • 📊 Comprehensive historical analysis")
    print("   • 🤖 AI assistant preview (coming soon)")
    print("   • 📱 Responsive design for mobile")
    print("   • 🎯 Deep ocean float positioning")
    print("\n👥 Team: Anuprabh, Aaron, Manvitha, Shreeya, Ashish, Disha")
    print("="*70)
    
    app.run_server(debug=True, port=8060, host='127.0.0.1')
