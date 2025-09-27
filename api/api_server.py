"""
FastAPI Backend for Argo Float Dashboard
Provides REST API endpoints for data access
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime
import uvicorn

# Import data module
import sys
sys.path.append('..')
from app.data.argo_data import ArgoFloatDashboard

# Initialize FastAPI app
app = FastAPI(
    title="Argo Float Dashboard API",
    description="REST API for Argo oceanographic data in the Indian Ocean",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize dashboard
dashboard = ArgoFloatDashboard()

# Pydantic models for API responses
class FloatInfo(BaseModel):
    platform_number: int
    latitude: float
    longitude: float
    last_date: datetime
    max_cycle: int
    max_depth: float
    avg_temp: float
    avg_salinity: float
    location: str

class ProfileData(BaseModel):
    platform_number: int
    cycle_number: int
    date: datetime
    latitude: float
    longitude: float
    pressure: float
    temperature: float
    salinity: float

class SummaryStats(BaseModel):
    total_floats: int
    avg_temp: float
    avg_salinity: float
    max_depth: float
    date_range: Dict[str, datetime]

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any

# Root endpoint
@app.get("/", response_model=Dict[str, str])
async def root():
    """API root endpoint"""
    return {
        "message": "Argo Float Dashboard API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "active"
    }

# Health check endpoint
@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "argo-float-api"
    }

# Get all floats
@app.get("/floats", response_model=APIResponse)
async def get_all_floats(
    region: Optional[str] = Query(None, description="Filter by region"),
    min_temp: Optional[float] = Query(None, description="Minimum temperature filter"),
    max_temp: Optional[float] = Query(None, description="Maximum temperature filter")
):
    """Get all float information with optional filters"""
    try:
        float_info = dashboard.get_float_info()
        
        # Apply filters
        if region:
            float_info = float_info[float_info['LOCATION'].str.contains(region, case=False)]
        
        if min_temp is not None:
            float_info = float_info[float_info['AVG_TEMP'] >= min_temp]
            
        if max_temp is not None:
            float_info = float_info[float_info['AVG_TEMP'] <= max_temp]
        
        # Convert to dict and handle datetime serialization
        float_data = float_info.to_dict('records')
        for record in float_data:
            if 'LAST_DATE' in record:
                record['LAST_DATE'] = record['LAST_DATE'].isoformat()
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(float_data)} floats",
            data=float_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get specific float
@app.get("/floats/{platform_number}", response_model=APIResponse)
async def get_float(platform_number: int):
    """Get information for a specific float"""
    try:
        float_info = dashboard.get_float_info()
        float_data = float_info[float_info['PLATFORM_NUMBER'] == platform_number]
        
        if float_data.empty:
            raise HTTPException(status_code=404, detail="Float not found")
        
        # Convert to dict
        result = float_data.iloc[0].to_dict()
        if 'LAST_DATE' in result:
            result['LAST_DATE'] = result['LAST_DATE'].isoformat()
        
        return APIResponse(
            success=True,
            message=f"Retrieved float {platform_number}",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get float profile data
@app.get("/floats/{platform_number}/profiles", response_model=APIResponse)
async def get_float_profiles(
    platform_number: int,
    cycle: Optional[int] = Query(None, description="Specific cycle number"),
    latest: bool = Query(False, description="Get only the latest profile")
):
    """Get profile data for a specific float"""
    try:
        profile_data = dashboard.get_float_profile_data(platform_number)
        
        if profile_data.empty:
            raise HTTPException(status_code=404, detail="No profile data found for this float")
        
        # Apply filters
        if cycle is not None:
            profile_data = profile_data[profile_data['CYCLE_NUMBER'] == cycle]
        elif latest:
            latest_cycle = profile_data['CYCLE_NUMBER'].max()
            profile_data = profile_data[profile_data['CYCLE_NUMBER'] == latest_cycle]
        
        # Convert to dict
        profiles = profile_data.to_dict('records')
        for record in profiles:
            if 'JULD' in record:
                record['JULD'] = record['JULD'].isoformat()
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(profiles)} profile records",
            data=profiles
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get summary statistics
@app.get("/stats", response_model=APIResponse)
async def get_summary_stats():
    """Get summary statistics for all floats"""
    try:
        stats = dashboard.get_summary_stats()
        
        # Convert datetime objects to ISO format
        stats['date_range']['start'] = stats['date_range']['start'].isoformat()
        stats['date_range']['end'] = stats['date_range']['end'].isoformat()
        
        return APIResponse(
            success=True,
            message="Retrieved summary statistics",
            data=stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get regional statistics
@app.get("/stats/regional", response_model=APIResponse)
async def get_regional_stats():
    """Get statistics grouped by region"""
    try:
        float_info = dashboard.get_float_info()
        
        # Group by region
        regional_stats = []
        for region in float_info['LOCATION'].str.extract('([^-]+)')[0].unique():
            region_data = float_info[float_info['LOCATION'].str.contains(region)]
            
            stats = {
                'region': region.strip(),
                'float_count': len(region_data),
                'avg_temperature': round(region_data['AVG_TEMP'].mean(), 2),
                'avg_salinity': round(region_data['AVG_SALINITY'].mean(), 2),
                'max_depth': int(region_data['MAX_DEPTH'].max()),
                'temperature_range': {
                    'min': round(region_data['AVG_TEMP'].min(), 2),
                    'max': round(region_data['AVG_TEMP'].max(), 2)
                }
            }
            regional_stats.append(stats)
        
        return APIResponse(
            success=True,
            message=f"Retrieved statistics for {len(regional_stats)} regions",
            data=regional_stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get temperature time series
@app.get("/floats/{platform_number}/temperature-series", response_model=APIResponse)
async def get_temperature_series(platform_number: int):
    """Get temperature time series for a specific float"""
    try:
        profile_data = dashboard.get_float_profile_data(platform_number)
        
        if profile_data.empty:
            raise HTTPException(status_code=404, detail="No data found for this float")
        
        # Get surface temperature data (pressure < 50)
        surface_data = profile_data[profile_data['PRES'] <= 50]
        
        # Group by date/cycle
        time_series = surface_data.groupby(['JULD', 'CYCLE_NUMBER']).agg({
            'TEMP': 'mean',
            'PRES': 'mean'
        }).reset_index()
        
        time_series = time_series.sort_values('JULD')
        
        # Convert to dict
        series_data = []
        for _, row in time_series.iterrows():
            series_data.append({
                'date': row['JULD'].isoformat(),
                'cycle': int(row['CYCLE_NUMBER']),
                'temperature': round(row['TEMP'], 2),
                'depth': round(row['PRES'], 1)
            })
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(series_data)} temperature records",
            data=series_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get latest profiles for all floats
@app.get("/profiles/latest", response_model=APIResponse)
async def get_latest_profiles():
    """Get the latest profile for each float"""
    try:
        float_info = dashboard.get_float_info()
        profile_data = dashboard.get_profile_data()
        
        latest_profiles = []
        
        for platform_number in float_info['PLATFORM_NUMBER']:
            float_profiles = profile_data[profile_data['PLATFORM_NUMBER'] == platform_number]
            if not float_profiles.empty:
                latest_cycle = float_profiles['CYCLE_NUMBER'].max()
                latest_profile = float_profiles[float_profiles['CYCLE_NUMBER'] == latest_cycle]
                
                # Get surface data
                surface_data = latest_profile[latest_profile['PRES'] <= 10].iloc[0] if not latest_profile[latest_profile['PRES'] <= 10].empty else latest_profile.iloc[0]
                
                latest_profiles.append({
                    'platform_number': int(platform_number),
                    'cycle': int(latest_cycle),
                    'date': surface_data['JULD'].isoformat(),
                    'latitude': round(surface_data['LATITUDE'], 4),
                    'longitude': round(surface_data['LONGITUDE'], 4),
                    'temperature': round(surface_data['TEMP'], 2),
                    'salinity': round(surface_data['PSAL'], 2),
                    'pressure': round(surface_data['PRES'], 1)
                })
        
        return APIResponse(
            success=True,
            message=f"Retrieved latest profiles for {len(latest_profiles)} floats",
            data=latest_profiles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export data endpoint
@app.get("/export/{format}")
async def export_data(
    format: str,
    platform_number: Optional[int] = Query(None, description="Specific float to export"),
    data_type: str = Query("float_info", description="Type of data: float_info, profiles, or both")
):
    """Export data in various formats"""
    try:
        if format not in ['json', 'csv']:
            raise HTTPException(status_code=400, detail="Supported formats: json, csv")
        
        # Get data based on type
        if data_type == "float_info":
            data = dashboard.get_float_info()
            if platform_number:
                data = data[data['PLATFORM_NUMBER'] == platform_number]
        elif data_type == "profiles":
            if platform_number:
                data = dashboard.get_float_profile_data(platform_number)
            else:
                data = dashboard.get_profile_data()
        else:
            raise HTTPException(status_code=400, detail="Supported data_type: float_info, profiles")
        
        if format == 'json':
            # Convert datetime to string for JSON serialization
            data_dict = data.to_dict('records')
            for record in data_dict:
                for key, value in record.items():
                    if isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()
            
            return JSONResponse(content={
                "success": True,
                "format": "json",
                "data_type": data_type,
                "record_count": len(data_dict),
                "data": data_dict
            })
        
        # For CSV, return as downloadable content
        csv_content = data.to_csv(index=False)
        from fastapi.responses import Response
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=argo_data_{data_type}.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Resource not found",
            "detail": str(exc.detail) if hasattr(exc, 'detail') else "Not found"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 ARGO FLOAT DASHBOARD API")
    print("="*60)
    print("📡 FastAPI Backend Server")
    print("🌐 Endpoints: http://127.0.0.1:8061")
    print("📚 Documentation: http://127.0.0.1:8061/docs")
    print("🔄 Interactive API: http://127.0.0.1:8061/redoc")
    print("="*60)
    print("\n🛠️ Available Endpoints:")
    print("   • GET  /floats - All float information")
    print("   • GET  /floats/{id} - Specific float data")
    print("   • GET  /floats/{id}/profiles - Profile data")
    print("   • GET  /stats - Summary statistics")
    print("   • GET  /stats/regional - Regional statistics")
    print("   • GET  /profiles/latest - Latest profiles")
    print("   • GET  /export/{format} - Data export")
    print("="*60)
    
    uvicorn.run(
        "api_server:app",
        host="127.0.0.1", 
        port=8061, 
        reload=True,
        log_level="info"
    )
