# 🌊 Argo Float Dashboard - Indian Ocean

An interactive web dashboard for monitoring Argo oceanographic floats in the Indian Ocean region using real-time data from the Global Argo Data Assembly Centre.

## 🚀 Features

- **Interactive Map**: Leaflet-based map showing real-time float locations around India's coast
- **Detailed Float Information**: Click on floats to view comprehensive data including:
  - Profile plots (Temperature, Salinity, T-S diagrams)
  - Time series analysis
  - Data tables with filtering and sorting
  - Operational status and metadata
- **Real-time Data**: Fetches live data from Argo servers using the `argopy` library
- **Fallback Mode**: Uses sample data if real-time data is unavailable
- **Professional UI**: Bootstrap-based responsive interface

## 📦 Installation

1. **Clone or download the project files**

2. **Set up Python environment** (recommended: Python 3.9+):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Usage

### Option 1: Test Connection First (Recommended)
```bash
python test_argo_connection.py
```
This will test your connection to Argo data servers and show you what data is available.

### Option 2: Run the Dashboard Directly
```bash
python argo_dashboard_enhanced.py
```

### Option 3: Run Simple Dashboard
```bash
python argo_dashboard.py
```

After running, open your browser and go to: **http://127.0.0.1:8050**

## 🌊 How to Use the Dashboard

1. **Map View**: 
   - Floats are color-coded by temperature (Red: >28°C, Orange: 25-28°C, Blue: <25°C)
   - Click on markers for popup information
   - Use the legend to understand temperature ranges

2. **Data Table**: 
   - View all float information in tabular format
   - Sort by clicking column headers
   - Filter data using the search boxes
   - **Click on any row to select a float for detailed analysis**

3. **Detailed Analysis** (appears after selecting a float):
   - **Float Information**: Location, operational status, environmental data
   - **Profile Plots**: Temperature and salinity vs depth, T-S diagram
   - **Time Series**: Historical trends in temperature, salinity, and depth

## 📊 Data Sources

- **Argo Global Data Assembly Centre**: https://argo.ucsd.edu/
- **ArgoPy Library**: https://argopy.readthedocs.io/
- **Real-time oceanographic data** from autonomous floats in the Indian Ocean

## 🛠️ Technical Details

### Key Files:
- `argo_dashboard_enhanced.py`: Main dashboard application (recommended)
- `argo_dashboard.py`: Simpler version of the dashboard
- `test_argo_connection.py`: Connection testing utility
- `argo_test.py`: Basic argopy test script
- `requirements.txt`: Python package dependencies

### Dependencies:
- **argopy**: Argo data fetching and processing
- **dash**: Web application framework
- **plotly**: Interactive plotting
- **folium**: Interactive mapping
- **pandas/numpy**: Data manipulation
- **dash-bootstrap-components**: UI components

### Regional Coverage:
- **Bounding Box**: 68°E to 97°E, 8°N to 30°N
- **Areas**: Arabian Sea, Bay of Bengal, Southern Indian Ocean
- **Focus**: Coastal waters around India

## 🔍 Features in Detail

### Interactive Map
- Real-time float positions
- Temperature-based color coding
- Detailed popups with float information
- Zoom and pan capabilities
- Professional styling with legend

### Profile Analysis
- **Temperature Profiles**: Vertical temperature distribution
- **Salinity Profiles**: Vertical salinity distribution  
- **T-S Diagrams**: Water mass analysis
- Color-coded by depth/pressure

### Time Series Analysis
- Surface temperature trends over time
- Surface salinity variations
- Maximum depth reached per profile
- Historical data visualization

### Data Management
- Automatic fallback to sample data
- Error handling and user feedback
- Data quality indicators
- Export capabilities

## 🚨 Troubleshooting

### Common Issues:

1. **"No data available"**: 
   - Check internet connection
   - Run `test_argo_connection.py` to diagnose
   - Dashboard will automatically use sample data

2. **Slow loading**:
   - Argo servers can be slow
   - Try running during off-peak hours
   - Use sample data mode for testing

3. **Missing packages**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Port already in use**:
   - Change port in the dashboard script: `app.run_server(port=8051)`

## 🌐 Sample Data Mode

If real Argo data is unavailable, the dashboard automatically switches to sample data mode featuring:
- 8 simulated floats around Indian coast locations
- Realistic temperature and salinity profiles
- Time series data for demonstration
- All dashboard features remain functional

## 📈 Future Enhancements

- Real-time alerts for abnormal readings
- Export functionality for data and plots
- Additional oceanographic parameters
- Mobile-responsive improvements
- Data quality metrics
- Float trajectory tracking

## 📝 License

This project uses data from the Argo Global Data Assembly Centre and is intended for educational and research purposes.

## 🤝 Contributing

Feel free to submit issues, suggestions, or improvements to enhance this dashboard.

---

**Built with ❤️ for oceanographic research and education**
