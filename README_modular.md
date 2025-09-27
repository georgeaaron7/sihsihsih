# 🌊 Modular Argo Float Dashboard

A comprehensive, modular oceanographic data visualization dashboard for monitoring Argo floats in the Indian Ocean region.

## 🏗️ Project Structure

```
final/
├── main.py                 # Main Dash application
├── requirements_modular.txt # Python dependencies
├── README_modular.md       # This file
├── 
├── app/                    # Main application package
│   ├── __init__.py
│   ├── data/              # Data management modules
│   │   ├── __init__.py
│   │   └── argo_data.py   # Argo data fetching and processing
│   ├── components/        # UI components
│   │   ├── __init__.py
│   │   ├── layout.py      # Navigation, footer, common layouts
│   │   └── visualizations.py # Maps, charts, tables
│   └── pages/             # Page modules
│       ├── __init__.py
│       ├── home.py        # Home page layout
│       ├── map_page.py    # Interactive map page
│       ├── charts.py      # Historical data analysis
│       └── chatbot.py     # AI assistant (coming soon)
├── 
├── api/                   # FastAPI backend
│   └── api_server.py      # REST API endpoints
├── 
└── assets/                # Static assets
    └── logo_placeholder.txt # Logo placeholder
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_modular.txt
```

### 2. Run the Dashboard
```bash
python main.py
```
Visit: http://127.0.0.1:8050

### 3. Run the API Server (optional)
```bash
cd api
python api_server.py
```
API Documentation: http://127.0.0.1:8001/docs

## 🎨 Features

### ✨ Modern UI
- **Gradient Design**: Beautiful gradients and modern styling
- **Responsive Layout**: Works on desktop and mobile devices
- **Smooth Animations**: Hover effects and transitions
- **Bootstrap Theme**: Professional component styling

### 🗺️ Interactive Map
- **Deep Ocean Positioning**: Floats positioned in actual ocean areas
- **Multiple Map Layers**: OpenStreetMap, Terrain, Toner options
- **Temperature Color Coding**: Visual temperature indicators
- **Detailed Popups**: Comprehensive float information
- **Layer Controls**: Switch between different map views

### 📊 Data Visualization
- **Profile Plots**: Temperature, salinity, and T-S diagrams
- **Time Series**: Historical trend analysis
- **Multi-Float Comparison**: Compare different floats
- **Interactive Charts**: Hover tooltips and zoom capabilities

### 🧭 Navigation
- **Home Page**: Overview with quick stats and analysis
- **Interactive Map**: Dedicated map exploration
- **Historical Charts**: Comprehensive data analysis
- **AI Assistant**: Coming soon preview

### 🔧 Technical Features
- **Modular Architecture**: Clean, maintainable code structure
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Data Export**: CSV and JSON export capabilities
- **Error Handling**: Robust error management
- **Type Hints**: Full Python type annotations

## 📡 API Endpoints

### Float Data
- `GET /floats` - Get all floats (with filters)
- `GET /floats/{id}` - Get specific float information
- `GET /floats/{id}/profiles` - Get float profile data
- `GET /floats/{id}/temperature-series` - Temperature time series

### Statistics
- `GET /stats` - Summary statistics
- `GET /stats/regional` - Regional breakdown
- `GET /profiles/latest` - Latest profiles for all floats

### Data Export
- `GET /export/json` - Export as JSON
- `GET /export/csv` - Export as CSV

## 🎯 Improvements Made

### 🌊 Ocean Positioning
- Fixed float coordinates to be in deep ocean waters
- Removed floats that were positioned on land
- Added more realistic regional coverage

### 🏗️ Code Organization
- Split 700+ line monolith into focused modules
- Separated concerns: data, UI, pages, API
- Improved maintainability and scalability

### 🎨 Enhanced UI
- Modern gradient design with animations
- Professional navigation with logo placeholder
- Team credits in footer
- Improved mobile responsiveness

### 📊 Better Data
- More realistic temperature and salinity profiles
- Seasonal variations in data
- Enhanced oceanographic accuracy
- Better time series generation

## 👥 Team Credits

**Made with ❤️ by:**
- Anuprabh
- Aaron  
- Manvitha
- Shreeya
- Ashish
- Disha

*Smart India Hackathon 2025 - Indian Ocean Research Initiative*

## 🔧 Development

### Adding New Pages
1. Create new page module in `app/pages/`
2. Import and add route in `main.py`
3. Add navigation link in `components/layout.py`

### Customization
- **Logo**: Replace `assets/logo_placeholder.txt` with `logo.png`
- **Colors**: Modify CSS variables in `main.py`
- **Data**: Extend `app/data/argo_data.py` for real data integration

### Real Data Integration
Uncomment `argopy` in requirements and modify data fetching methods to use real Argo data sources.

## 📄 License

This project is developed for the Smart India Hackathon 2025. Please ensure appropriate data usage permissions when deploying with real oceanographic data.
