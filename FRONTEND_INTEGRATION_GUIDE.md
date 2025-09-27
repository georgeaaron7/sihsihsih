# 🌊 Argo Float Dashboard - Frontend Integration Guide

This guide explains how to integrate external frontends (React, Vue, Angular, etc.) with the Argo Float Dashboard FastAPI backend.

## 🚀 Quick Start

### 1. Start the FastAPI Backend

```bash
# In the project directory
python3 api/api_server.py

# Server will start on: http://127.0.0.1:8061
# API Documentation: http://127.0.0.1:8061/docs
```

### 2. API Base URL
```
Base URL: http://127.0.0.1:8061
```

## 📋 Available API Endpoints

### Core Endpoints

#### 1. Get All Floats
```http
GET /floats
```

**Optional Query Parameters:**
- `region`: Filter by region (e.g., "Arabian Sea")
- `min_temp`: Minimum temperature filter
- `max_temp`: Maximum temperature filter

**Example:**
```javascript
fetch('http://127.0.0.1:8061/floats?region=Arabian%20Sea&min_temp=25')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### 2. Float Click Event (Important!)
```http
POST /floats/{platform_number}/click
```

**Purpose:** Logs user interactions with float markers
**Response:** Float details + click confirmation

**Example:**
```javascript
// When user clicks on float marker
const logFloatClick = async (platformNumber) => {
  try {
    const response = await fetch(`http://127.0.0.1:8061/floats/${platformNumber}/click`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    const data = await response.json();
    console.log('Float click logged:', data);
    return data;
  } catch (error) {
    console.error('API call failed:', error);
  }
};
```

#### 3. Get Float Details
```http
GET /floats/{platform_number}/details
```

**Returns:** Detailed information + profile data for specific float

#### 4. Get Float Profiles
```http
GET /floats/{platform_number}/profiles
```

**Optional Parameters:**
- `limit`: Number of profiles to return (default: 100)

#### 5. Export Data
```http
GET /export/floats
POST /export/profiles
```

## 🖥️ Frontend Integration Examples

### React Integration

#### 1. Setup API Service
```javascript
// services/argoAPI.js
const API_BASE_URL = 'http://127.0.0.1:8061';

class ArgoAPI {
  static async getAllFloats(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/floats?${params}`);
    return response.json();
  }

  static async logFloatClick(platformNumber) {
    const response = await fetch(`${API_BASE_URL}/floats/${platformNumber}/click`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
  }

  static async getFloatDetails(platformNumber) {
    const response = await fetch(`${API_BASE_URL}/floats/${platformNumber}/details`);
    return response.json();
  }
}

export default ArgoAPI;
```

#### 2. React Component Example
```jsx
// components/FloatMap.jsx
import React, { useState, useEffect } from 'react';
import ArgoAPI from '../services/argoAPI';

const FloatMap = () => {
  const [floats, setFloats] = useState([]);
  const [selectedFloat, setSelectedFloat] = useState(null);

  useEffect(() => {
    loadFloats();
  }, []);

  const loadFloats = async () => {
    try {
      const response = await ArgoAPI.getAllFloats();
      if (response.success) {
        setFloats(response.data);
      }
    } catch (error) {
      console.error('Failed to load floats:', error);
    }
  };

  const handleFloatClick = async (platformNumber) => {
    try {
      // Log the click event
      const clickResponse = await ArgoAPI.logFloatClick(platformNumber);
      console.log('Click logged:', clickResponse);

      // Get detailed information
      const detailsResponse = await ArgoAPI.getFloatDetails(platformNumber);
      if (detailsResponse.success) {
        setSelectedFloat(detailsResponse.data);
      }
    } catch (error) {
      console.error('Failed to handle float click:', error);
    }
  };

  return (
    <div>
      <h2>Argo Float Map</h2>
      <div className="float-grid">
        {floats.map(float => (
          <div 
            key={float.platform_number}
            className="float-marker"
            onClick={() => handleFloatClick(float.platform_number)}
          >
            Float {float.platform_number}
          </div>
        ))}
      </div>
      {selectedFloat && (
        <div className="float-details">
          <h3>Float {selectedFloat.float_info.platform_number}</h3>
          <p>Temperature: {selectedFloat.float_info.avg_temp}°C</p>
          <p>Location: {selectedFloat.float_info.location}</p>
        </div>
      )}
    </div>
  );
};

export default FloatMap;
```

### Vue.js Integration

#### 1. API Service
```javascript
// services/argoAPI.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8061',
  timeout: 10000
});

export default {
  async getAllFloats(filters = {}) {
    const response = await API.get('/floats', { params: filters });
    return response.data;
  },

  async logFloatClick(platformNumber) {
    const response = await API.post(`/floats/${platformNumber}/click`);
    return response.data;
  },

  async getFloatDetails(platformNumber) {
    const response = await API.get(`/floats/${platformNumber}/details`);
    return response.data;
  }
};
```

#### 2. Vue Component Example
```vue
<template>
  <div>
    <h2>Argo Float Dashboard</h2>
    <div class="float-controls">
      <select v-model="selectedRegion" @change="loadFloats">
        <option value="">All Regions</option>
        <option value="Arabian Sea">Arabian Sea</option>
        <option value="Bay of Bengal">Bay of Bengal</option>
      </select>
    </div>
    <div class="float-map">
      <div 
        v-for="float in floats" 
        :key="float.platform_number"
        @click="handleFloatClick(float.platform_number)"
        class="float-marker"
      >
        🚢 {{ float.platform_number }}
      </div>
    </div>
    <div v-if="selectedFloat" class="float-info">
      <h3>Float Details</h3>
      <p>Temperature: {{ selectedFloat.float_info.avg_temp }}°C</p>
      <p>Salinity: {{ selectedFloat.float_info.avg_salinity }} PSU</p>
    </div>
  </div>
</template>

<script>
import ArgoAPI from '../services/argoAPI';

export default {
  name: 'FloatDashboard',
  data() {
    return {
      floats: [],
      selectedFloat: null,
      selectedRegion: ''
    };
  },
  
  mounted() {
    this.loadFloats();
  },
  
  methods: {
    async loadFloats() {
      try {
        const filters = {};
        if (this.selectedRegion) {
          filters.region = this.selectedRegion;
        }
        
        const response = await ArgoAPI.getAllFloats(filters);
        if (response.success) {
          this.floats = response.data;
        }
      } catch (error) {
        console.error('Failed to load floats:', error);
      }
    },
    
    async handleFloatClick(platformNumber) {
      try {
        // Log click event
        await ArgoAPI.logFloatClick(platformNumber);
        
        // Get details
        const response = await ArgoAPI.getFloatDetails(platformNumber);
        if (response.success) {
          this.selectedFloat = response.data;
        }
      } catch (error) {
        console.error('Float click failed:', error);
      }
    }
  }
};
</script>
```

### Angular Integration

#### 1. Service
```typescript
// services/argo-api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ArgoApiService {
  private baseUrl = 'http://127.0.0.1:8061';

  constructor(private http: HttpClient) {}

  getAllFloats(filters: any = {}): Observable<any> {
    let params = new HttpParams();
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        params = params.set(key, filters[key]);
      }
    });
    
    return this.http.get(`${this.baseUrl}/floats`, { params });
  }

  logFloatClick(platformNumber: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/floats/${platformNumber}/click`, {});
  }

  getFloatDetails(platformNumber: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/floats/${platformNumber}/details`);
  }
}
```

#### 2. Component
```typescript
// components/float-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { ArgoApiService } from '../services/argo-api.service';

@Component({
  selector: 'app-float-dashboard',
  template: `
    <h2>Argo Float Dashboard</h2>
    <div class="float-grid">
      <div 
        *ngFor="let float of floats" 
        (click)="handleFloatClick(float.platform_number)"
        class="float-marker"
      >
        🚢 Float {{ float.platform_number }}
      </div>
    </div>
    <div *ngIf="selectedFloat" class="float-details">
      <h3>Float {{ selectedFloat.float_info.platform_number }}</h3>
      <p>Temperature: {{ selectedFloat.float_info.avg_temp }}°C</p>
      <p>Location: {{ selectedFloat.float_info.location }}</p>
    </div>
  `
})
export class FloatDashboardComponent implements OnInit {
  floats: any[] = [];
  selectedFloat: any = null;

  constructor(private argoApi: ArgoApiService) {}

  ngOnInit() {
    this.loadFloats();
  }

  loadFloats() {
    this.argoApi.getAllFloats().subscribe(
      response => {
        if (response.success) {
          this.floats = response.data;
        }
      },
      error => console.error('Failed to load floats:', error)
    );
  }

  handleFloatClick(platformNumber: number) {
    // Log click
    this.argoApi.logFloatClick(platformNumber).subscribe(
      response => console.log('Click logged:', response)
    );

    // Get details
    this.argoApi.getFloatDetails(platformNumber).subscribe(
      response => {
        if (response.success) {
          this.selectedFloat = response.data;
        }
      },
      error => console.error('Failed to get float details:', error)
    );
  }
}
```

## 🌍 Map Integration Examples

### Leaflet Integration
```javascript
// For Leaflet maps
import L from 'leaflet';
import ArgoAPI from './argoAPI';

const map = L.map('map').setView([15, 78], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Load floats and add markers
ArgoAPI.getAllFloats().then(response => {
  if (response.success) {
    response.data.forEach(float => {
      const marker = L.marker([float.latitude, float.longitude])
        .addTo(map)
        .bindPopup(`Float ${float.platform_number}`)
        .on('click', async () => {
          // Log click to API
          await ArgoAPI.logFloatClick(float.platform_number);
          console.log(`Clicked float ${float.platform_number}`);
        });
    });
  }
});
```

### Google Maps Integration
```javascript
// Google Maps example
function initMap() {
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 5,
    center: { lat: 15, lng: 78 }
  });

  ArgoAPI.getAllFloats().then(response => {
    if (response.success) {
      response.data.forEach(float => {
        const marker = new google.maps.Marker({
          position: { lat: float.latitude, lng: float.longitude },
          map: map,
          title: `Float ${float.platform_number}`
        });

        marker.addListener('click', async () => {
          await ArgoAPI.logFloatClick(float.platform_number);
          console.log(`Clicked float ${float.platform_number}`);
        });
      });
    }
  });
}
```

## 🔧 Advanced Configuration

### CORS Configuration
The API server is configured to accept requests from any origin during development. For production, update the CORS settings in `api/api_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://your-frontend-domain.com"],  # Specify your domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Error Handling
```javascript
const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    console.error('API Error:', error.response.status, error.response.data);
  } else if (error.request) {
    // Request was made but no response received
    console.error('Network Error:', error.message);
  } else {
    // Something else happened
    console.error('Error:', error.message);
  }
};
```

### Real-time Updates
For real-time float data updates, consider implementing WebSocket connections or polling:

```javascript
// Polling example
const pollFloatData = () => {
  setInterval(async () => {
    try {
      const response = await ArgoAPI.getAllFloats();
      if (response.success) {
        updateFloatMarkers(response.data);
      }
    } catch (error) {
      console.error('Polling failed:', error);
    }
  }, 30000); // Poll every 30 seconds
};
```

## 📊 Data Structure Reference

### Float Object Structure
```json
{
  "platform_number": 1234567,
  "latitude": 12.345,
  "longitude": 67.890,
  "last_date": "2024-01-15T10:30:00",
  "max_cycle": 156,
  "max_depth": 2000.0,
  "avg_temp": 28.5,
  "avg_salinity": 35.2,
  "location": "Arabian Sea"
}
```

### API Response Structure
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

## 🚀 Production Deployment

### Environment Variables
```bash
# .env file
API_BASE_URL=https://your-api-domain.com
CORS_ORIGINS=https://your-frontend-domain.com
LOG_LEVEL=INFO
```

### Docker Configuration
```dockerfile
# Frontend Dockerfile example
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 📋 Testing Your Integration

### 1. Test API Connectivity
```javascript
// Test connection
fetch('http://127.0.0.1:8061/health')
  .then(response => response.json())
  .then(data => console.log('API Status:', data))
  .catch(error => console.error('API not available:', error));
```

### 2. Test Float Click Logging
```javascript
// Test float click
const testFloatClick = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8061/floats/1234567/click', {
      method: 'POST'
    });
    const data = await response.json();
    console.log('Click test result:', data);
  } catch (error) {
    console.error('Click test failed:', error);
  }
};
```

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the API server is running and CORS is properly configured
2. **Network Timeouts**: Check if the API server is accessible at `http://127.0.0.1:8061`
3. **Missing Data**: Verify the dashboard data is properly generated
4. **Click Events Not Logging**: Check browser console for API call failures

### Debug Mode
Enable debug logging in your frontend:
```javascript
const DEBUG = true;

const apiCall = async (url, options) => {
  if (DEBUG) console.log('API Call:', url, options);
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    if (DEBUG) console.log('API Response:', data);
    return data;
  } catch (error) {
    if (DEBUG) console.error('API Error:', error);
    throw error;
  }
};
```

## 📞 Support

For issues or questions:
1. Check the API documentation at `http://127.0.0.1:8061/docs`
2. Review the server logs in `argo_api.log`
3. Ensure both frontend and backend are running on correct ports

---

**Happy Coding! 🌊⚓**
