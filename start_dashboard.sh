#!/bin/bash

# Argo Float Dashboard Startup Script
echo "🌊 Starting Argo Float Dashboard..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install/update required packages
echo "📥 Installing required packages..."
python3 -m pip install -q dash dash-bootstrap-components plotly pandas numpy folium fastapi uvicorn pydantic

# Start the main dashboard
echo "🚀 Starting main dashboard on http://127.0.0.1:8060..."
python3 main.py
