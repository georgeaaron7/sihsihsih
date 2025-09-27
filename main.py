"""
Main Dash Application
Modular Argo Float Dashboard
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import requests

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
                --ocean-blue-gradient: linear-gradient(135deg, #0f4c75 0%, #3282b8 50%, #bbe1fa 100%);
                --deep-ocean-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4FC3F7 100%);
                --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f1419 0%, #1a252f 50%, #2c3e50 100%);
                min-height: 100vh;
                color: #e9ecef;
            }
            
            .navbar-modern {
                background: var(--deep-ocean-gradient) !important;
                backdrop-filter: blur(10px);
                border-bottom: 2px solid rgba(79, 195, 247, 0.3);
            }
            
            .nav-link-modern {
                transition: all 0.3s ease;
                border-radius: 8px;
                margin: 0 5px;
                font-weight: 500;
                color: #e9ecef !important;
            }
            
            .nav-link-modern:hover {
                background: linear-gradient(135deg, rgba(79, 195, 247, 0.2), rgba(50, 130, 184, 0.3)) !important;
                transform: translateY(-2px);
                color: white !important;
                box-shadow: 0 4px 15px rgba(79, 195, 247, 0.2);
            }
            
            .nav-link-modern.active {
                background: linear-gradient(135deg, rgba(79, 195, 247, 0.3), rgba(50, 130, 184, 0.4)) !important;
                color: white !important;
                font-weight: 600;
                box-shadow: 0 4px 20px rgba(79, 195, 247, 0.3);
            }
            
            .card {
                border: 1px solid rgba(79, 195, 247, 0.2);
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                transition: all 0.3s ease;
                background: linear-gradient(135deg, rgba(52, 73, 94, 0.9), rgba(44, 62, 80, 0.9)) !important;
                backdrop-filter: blur(10px);
                color: #e9ecef;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(79, 195, 247, 0.2);
                border-color: rgba(79, 195, 247, 0.4);
            }
            
            .card-hover:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 30px rgba(79, 195, 247, 0.15);
            }
            
            .btn {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .btn-primary {
                background: var(--deep-ocean-gradient) !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(79, 195, 247, 0.3);
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(79, 195, 247, 0.4) !important;
            }
            
            .badge {
                border-radius: 6px;
                font-weight: 500;
            }
            
            .alert {
                border: 1px solid rgba(79, 195, 247, 0.2);
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                background: linear-gradient(135deg, rgba(52, 73, 94, 0.8), rgba(44, 62, 80, 0.8)) !important;
            }
            
            /* Dash table styling */
            .dash-table-container {
                border-radius: 12px;
                overflow: hidden;
                background: rgba(52, 73, 94, 0.9) !important;
            }
            
            .dash-table-container .dash-spreadsheet-container {
                background: rgba(44, 62, 80, 0.9) !important;
            }
            
            /* Loading spinner */
            .dash-spinner {
                margin: 50px auto;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(44, 62, 80, 0.5);
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--deep-ocean-gradient);
                border-radius: 6px;
                border: 2px solid rgba(44, 62, 80, 0.5);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #4FC3F7, #3282b8);
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

# Map type selector callback
@app.callback(
    Output('interactive-map-container', 'children'),
    [Input('map-type-selector', 'value')],
    [State('current-page', 'data')]
)
def update_map_type(map_type, current_page):
    """Update map visualization based on selected type"""
    if current_page != 'map':
        return html.Div()
    
    try:
        float_info = dashboard.get_float_info()
        
        if map_type == 'plotly':
            from app.components.visualizations import create_plotly_interactive_map
            return create_plotly_interactive_map(float_info)
        else:
            from app.components.visualizations import create_interactive_map
            return create_interactive_map(float_info)
            
    except Exception as e:
        return create_error_alert(
            "Failed to load map", 
            str(e)
        )

# Float click callback for Plotly map
@app.callback(
    Output('float-click-info', 'children'),
    [Input('plotly-float-map', 'clickData')],
    [State('current-page', 'data')]
)
def handle_float_click(clickData, current_page):
    """Handle float marker clicks and make API call"""
    if current_page != 'map' or not clickData:
        return html.Div()
    
    try:
        # Extract platform number from click data
        platform_number = clickData['points'][0]['customdata']
        
        # Make API call to log the click
        api_url = "http://127.0.0.1:8061"  # FastAPI server URL
        try:
            response = requests.post(f"{api_url}/floats/{platform_number}/click", timeout=5)
            if response.status_code == 200:
                api_message = "✅ Click logged to API server"
                api_color = "success"
            else:
                api_message = f"⚠️ API response: {response.status_code}"
                api_color = "warning"
        except requests.exceptions.RequestException as e:
            api_message = f"❌ API server unavailable: {str(e)[:50]}..."
            api_color = "danger"
        
        # Get float details
        float_info = dashboard.get_float_info()
        float_data = float_info[float_info['PLATFORM_NUMBER'] == platform_number]
        
        if float_data.empty:
            return dbc.Alert("Float not found", color="danger")
        
        float_record = float_data.iloc[0]
        
        return dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-ship me-2"),
                    f"Float {platform_number} - Click Details"
                ], className="mb-0 text-primary")
            ]),
            dbc.CardBody([
                dbc.Alert(api_message, color=api_color, className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.H6("📍 Location", className="text-info mb-2"),
                        html.P([html.Strong("Coordinates: "), 
                               f"{float_record['LATITUDE']:.4f}°N, {float_record['LONGITUDE']:.4f}°E"]),
                        html.P([html.Strong("Region: "), float_record['LOCATION']])
                    ], md=4),
                    dbc.Col([
                        html.H6("🌡️ Measurements", className="text-warning mb-2"),
                        html.P([html.Strong("Temperature: "), f"{float_record['AVG_TEMP']:.2f}°C"]),
                        html.P([html.Strong("Salinity: "), f"{float_record['AVG_SALINITY']:.2f} PSU"])
                    ], md=4),
                    dbc.Col([
                        html.H6("📊 Statistics", className="text-success mb-2"),
                        html.P([html.Strong("Max Depth: "), f"{float_record['MAX_DEPTH']:.0f}m"]),
                        html.P([html.Strong("Cycles: "), str(float_record['MAX_CYCLE'])])
                    ], md=4)
                ])
            ])
        ], className="mt-3")
        
    except Exception as e:
        return dbc.Alert(f"Error processing click: {str(e)}", color="danger")

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
