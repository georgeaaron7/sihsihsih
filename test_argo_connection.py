#!/usr/bin/env python3
"""
Argo Data Test Script
This script tests the connection to Argo data servers and fetches sample data
for the Indian Ocean region.
"""

import argopy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration
INDIA_BBOX = [68, 8, 97, 30]  # [lon_min, lat_min, lon_max, lat_max] around India

def test_argo_connection():
    """Test connection to Argo data servers"""
    print("🌊 Testing Argo Data Connection...")
    print("-" * 50)
    
    try:
        # Initialize fetcher with explicit source
        fetcher = argopy.DataFetcher(src='erddap')
        print(f"✅ ArgoPy initialized successfully")
        print(f"📡 Data source: erddap (Ifremer server)")
        
        # Test basic connection
        print("\n🔍 Testing data fetch for Indian Ocean region...")
        print(f"📍 Bounding box: {INDIA_BBOX}")
        
        # Fetch data for a smaller region with time constraint (recent data)
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)  # Last 60 days
        
        # Test region: [lon_min, lon_max, lat_min, lat_max, pres_min, pres_max, start_date, end_date]
        test_region = [70, 85, 8, 25, 0, 2000, start_date.strftime('%Y-%m'), end_date.strftime('%Y-%m')]
        
        print(f"🎯 Test region: {test_region}")
        print("⏳ Fetching data (this may take a moment)...")
        
        ds = fetcher.region(test_region).load()
        print(f"✅ Successfully fetched data!")
        print(f"📦 Dataset info: {ds.dims}")
        
        # Convert to profile data
        profiles = ds.argo.point2profile()
        print(f"📊 Found {len(profiles)} data points")
        
        # Get unique floats
        unique_floats = profiles['PLATFORM_NUMBER'].unique()
        print(f"🚢 Found {len(unique_floats)} unique floats")
        
        if len(unique_floats) > 0:
            print(f"🔢 Float IDs: {unique_floats[:5]}...")  # Show first 5
            
            # Get float summary
            float_summary = profiles.groupby('PLATFORM_NUMBER').agg({
                'LATITUDE': 'last',
                'LONGITUDE': 'last',
                'JULD': 'last',
                'CYCLE_NUMBER': 'max',
                'PRES': lambda x: x.dropna().max() if len(x.dropna()) > 0 else np.nan,
                'TEMP': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan,
                'PSAL': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else np.nan
            }).reset_index()
            
            print(f"\n📋 Sample Float Data:")
            print(float_summary.head())
            
        return True, fetcher, profiles
        
    except Exception as e:
        print(f"❌ Error connecting to Argo data: {e}")
        print(f"🔍 Error details: {str(e)}")
        return False, None, None

def test_specific_float(fetcher, platform_number):
    """Test fetching data for a specific float"""
    try:
        print(f"\n🔍 Testing specific float data: {platform_number}")
        ds = fetcher.float(int(platform_number)).load()
        profiles = ds.argo.point2profile()
        
        float_data = profiles[profiles['PLATFORM_NUMBER'] == int(platform_number)]
        print(f"✅ Found {len(float_data)} profiles for float {platform_number}")
        
        # Show some statistics
        if not float_data.empty:
            print(f"📊 Cycles: {float_data['CYCLE_NUMBER'].min()} - {float_data['CYCLE_NUMBER'].max()}")
            print(f"🌡️ Temperature range: {float_data['TEMP'].min():.1f} - {float_data['TEMP'].max():.1f}°C")
            print(f"🧂 Salinity range: {float_data['PSAL'].min():.1f} - {float_data['PSAL'].max():.1f} PSU")
            print(f"🌊 Depth range: {float_data['PRES'].min():.1f} - {float_data['PRES'].max():.1f} dbar")
        
        return True, float_data
        
    except Exception as e:
        print(f"❌ Error fetching float data: {e}")
        return False, None

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 ARGO DATA CONNECTION TEST")
    print("=" * 60)
    
    # Test basic connection
    success, fetcher, data = test_argo_connection()
    
    if success and data is not None and not data.empty:
        print(f"\n✅ Connection test PASSED!")
        
        # Test specific float if we have data
        unique_floats = data['PLATFORM_NUMBER'].unique()
        if len(unique_floats) > 0:
            test_float = unique_floats[0]
            print(f"\n🔬 Testing detailed data fetch...")
            float_success, float_data = test_specific_float(fetcher, test_float)
            
            if float_success:
                print(f"✅ Float data test PASSED!")
            else:
                print(f"⚠️ Float data test failed, but basic connection works")
        
        print(f"\n🎉 Ready to run the dashboard with real data!")
        
    else:
        print(f"\n⚠️ Connection test FAILED - Dashboard will use sample data")
    
    print("\n" + "=" * 60)
    print("🚀 You can now run the dashboard:")
    print("   python argo_dashboard_enhanced.py")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    main()
