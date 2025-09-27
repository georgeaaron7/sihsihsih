"""
Argo Float Data Management Module
Handles data fetching, processing, and sample data generation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ArgoFloatDashboard:
    def __init__(self):
        print("Initializing dashboard with sample data...")
        self.sample_data = self.create_sample_data()
        
    def create_sample_data(self):
        """Create comprehensive sample data for demonstration with better ocean positioning"""
        np.random.seed(42)
        
        # Sample float positions in DEEP OCEAN waters around Indian coast
        # These coordinates are specifically chosen to be in deep water, not on land
        float_positions = [
            {'lat': 15.0, 'lon': 68.0, 'name': 'Arabian Sea - Deep West'},
            {'lat': 12.0, 'lon': 70.5, 'name': 'Arabian Sea - Central'},
            {'lat': 18.0, 'lon': 84.5, 'name': 'Bay of Bengal - Deep East'},
            {'lat': 8.0, 'lon': 78.0, 'name': 'South Indian Ocean'},
            {'lat': 20.0, 'lon': 66.5, 'name': 'Arabian Sea - Northwest'},
            {'lat': 13.0, 'lon': 81.5, 'name': 'Bay of Bengal - Central'},
            {'lat': 16.0, 'lon': 87.0, 'name': 'Bay of Bengal - Northeast'},
            {'lat': 10.0, 'lon': 94.0, 'name': 'Andaman Sea - Deep'},
            {'lat': 14.0, 'lon': 72.0, 'name': 'Arabian Sea - Mid'},
            {'lat': 11.0, 'lon': 85.0, 'name': 'Bay of Bengal - South'},
            {'lat': 6.0, 'lon': 80.0, 'name': 'South Indian Ocean - Deep'},
            {'lat': 17.0, 'lon': 89.5, 'name': 'Bay of Bengal - Far East'}
        ]
        
        float_info_list = []
        profile_data_list = []
        
        for i, pos in enumerate(float_positions):
            platform_number = 1234567 + i
            
            # Generate realistic float summary info
            last_date = datetime.now() - timedelta(days=np.random.randint(1, 15))
            max_cycles = np.random.randint(25, 120)
            max_depth = np.random.randint(1800, 2000)
            
            # Temperature varies by location (Arabian Sea warmer than Bay of Bengal)
            base_temp = 28.5 if 'Arabian Sea' in pos['name'] else 27.2
            avg_temp = base_temp + np.random.normal(0, 1.8)
            
            # Salinity varies by region
            base_salinity = 35.2 if 'Arabian Sea' in pos['name'] else 34.1
            avg_salinity = base_salinity + np.random.normal(0, 0.4)
            
            float_info_list.append({
                'PLATFORM_NUMBER': platform_number,
                'LATITUDE': pos['lat'] + np.random.normal(0, 0.2),  # Small variation
                'LONGITUDE': pos['lon'] + np.random.normal(0, 0.2),
                'LAST_DATE': last_date,
                'MAX_CYCLE': max_cycles,
                'MAX_DEPTH': max_depth,
                'AVG_TEMP': avg_temp,
                'AVG_SALINITY': avg_salinity,
                'LOCATION': pos['name']
            })
            
            # Generate realistic profile data for each float
            n_profiles = np.random.randint(8, 15)  # Multiple profiles per float
            
            for profile in range(n_profiles):
                profile_date = datetime.now() - timedelta(days=np.random.randint(1, 200))
                cycle_number = profile + 1
                
                # Generate depth points with realistic oceanographic structure
                depths_shallow = np.arange(0, 200, 5)   # High resolution in upper 200m
                depths_mid = np.arange(200, 1000, 15)   # Medium resolution 200-1000m
                depths_deep = np.arange(1000, max_depth, 30)  # Lower resolution below 1000m
                depths = np.concatenate([depths_shallow, depths_mid, depths_deep])
                
                for depth in depths:
                    # More realistic temperature profile with seasonal variation
                    seasonal_factor = np.sin(2 * np.pi * profile_date.timetuple().tm_yday / 365) * 1.5
                    
                    if depth < 50:  # Mixed layer
                        temp = avg_temp + seasonal_factor + np.random.normal(0, 0.8)
                    elif depth < 200:  # Thermocline
                        temp = avg_temp + seasonal_factor * 0.5 - (depth - 50) * 0.15 + np.random.normal(0, 1.2)
                    elif depth < 1000:  # Deep water
                        temp = 15 - (depth - 200) * 0.012 + np.random.normal(0, 0.6)
                    else:  # Abyssal
                        temp = 3.5 - (depth - 1000) * 0.0015 + np.random.normal(0, 0.3)
                    
                    temp = max(temp, 1.8)  # Minimum temperature
                    
                    # More realistic salinity profile with halocline
                    if depth < 100:  # Surface layer
                        salinity = avg_salinity + np.random.normal(0, 0.15)
                    elif depth < 500:  # Subsurface maximum
                        salinity = avg_salinity + 0.4 + (depth - 100) * 0.0008 + np.random.normal(0, 0.12)
                    elif depth < 1500:  # Deep water
                        salinity = 34.7 + np.random.normal(0, 0.08)
                    else:  # Bottom water
                        salinity = 34.65 + np.random.normal(0, 0.05)
                    
                    profile_data_list.append({
                        'PLATFORM_NUMBER': platform_number,
                        'CYCLE_NUMBER': cycle_number,
                        'JULD': profile_date,
                        'LATITUDE': pos['lat'] + np.random.normal(0, 0.03),
                        'LONGITUDE': pos['lon'] + np.random.normal(0, 0.03),
                        'PRES': depth,
                        'TEMP': temp,
                        'PSAL': salinity
                    })
        
        float_info_df = pd.DataFrame(float_info_list)
        profile_data_df = pd.DataFrame(profile_data_list)
        
        return {
            'float_info': float_info_df,
            'profile_data': profile_data_df
        }
    
    def get_float_info(self):
        """Get float summary information"""
        return self.sample_data['float_info']
    
    def get_profile_data(self):
        """Get all profile data"""
        return self.sample_data['profile_data']
    
    def get_float_profile_data(self, platform_number):
        """Get profile data for a specific float"""
        return self.sample_data['profile_data'][
            self.sample_data['profile_data']['PLATFORM_NUMBER'] == int(platform_number)
        ]
    
    def get_summary_stats(self):
        """Get summary statistics"""
        float_info = self.sample_data['float_info']
        return {
            'total_floats': len(float_info),
            'avg_temp': float_info['AVG_TEMP'].mean(),
            'avg_salinity': float_info['AVG_SALINITY'].mean(),
            'max_depth': float_info['MAX_DEPTH'].max(),
            'date_range': {
                'start': float_info['LAST_DATE'].min(),
                'end': float_info['LAST_DATE'].max()
            }
        }
