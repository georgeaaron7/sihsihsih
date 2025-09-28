import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Thermometer, Droplets, Activity, Filter, Search, Maximize2, Info } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { argoApi, FloatInfo } from '../lib/apiClient';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorBoundary from '../components/ErrorBoundary';
import Nav from '../components/Nav';
import Footer from '../components/Footer';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { LatLngExpression, Icon, divIcon } from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface MapFilters {
  minTemp: number;
  maxTemp: number;
  minDepth: number;
  maxDepth: number;
  region: string;
  searchTerm: string;
}

const InteractiveMapPage: React.FC = () => {
  const [selectedFloat, setSelectedFloat] = useState<FloatInfo | null>(null);
  const [mapFilters, setMapFilters] = useState<MapFilters>({
    minTemp: 0,
    maxTemp: 35,
    minDepth: 0,
    maxDepth: 5000,
    region: 'all',
    searchTerm: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  const [mapView, setMapView] = useState<'satellite' | 'terrain' | 'street'>('satellite');

  const { data: floats = [], isLoading, error } = useQuery({
    queryKey: ['floats'],
    queryFn: () => argoApi.getFloats(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Filter floats based on current filters
  const filteredFloats = floats.filter((float: FloatInfo) => {
    const matchesTemp = float.AVG_TEMP >= mapFilters.minTemp && float.AVG_TEMP <= mapFilters.maxTemp;
    const matchesDepth = float.MAX_DEPTH >= mapFilters.minDepth && float.MAX_DEPTH <= mapFilters.maxDepth;
    const matchesRegion = mapFilters.region === 'all' || float.LOCATION.toLowerCase().includes(mapFilters.region.toLowerCase());
    const matchesSearch = mapFilters.searchTerm === '' || 
      float.PLATFORM_NUMBER.toString().includes(mapFilters.searchTerm) ||
      float.LOCATION.toLowerCase().includes(mapFilters.searchTerm.toLowerCase());
    
    return matchesTemp && matchesDepth && matchesRegion && matchesSearch;
  });

  const handleFloatClick = async (float: FloatInfo) => {
    setSelectedFloat(float);
    
    // Log the click to the API
    try {
      await argoApi.logFloatClick(float.PLATFORM_NUMBER, {
        source: 'interactive-map',
        action: 'click'
      });
    } catch (error) {
      console.warn('Failed to log float click:', error);
    }
  };

  const getFloatColor = (temp: number) => {
    if (temp > 28) return '#ef4444'; // red
    if (temp > 26) return '#f97316'; // orange
    if (temp > 24) return '#eab308'; // yellow
    if (temp > 22) return '#22c55e'; // green
    return '#3b82f6'; // blue
  };

  const getTemperatureCategory = (temp: number) => {
    if (temp > 28) return 'Very Warm';
    if (temp > 26) return 'Warm';
    if (temp > 24) return 'Moderate';
    if (temp > 22) return 'Cool';
    return 'Cold';
  };

  // Create custom marker icons based on temperature
  const createMarkerIcon = (float: FloatInfo) => {
    const color = getFloatColor(float.AVG_TEMP);
    return divIcon({
      html: `
        <div style="
          width: 24px;
          height: 24px;
          background-color: ${color};
          border: 2px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 10px;
          font-weight: bold;
          color: white;
          cursor: pointer;
        ">⚓</div>
      `,
      className: 'custom-marker',
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });
  };

  const regions = [
    { value: 'all', label: 'All Regions' },
    { value: 'arabian', label: 'Arabian Sea' },
    { value: 'bay of bengal', label: 'Bay of Bengal' },
    { value: 'indian ocean', label: 'Indian Ocean' },
    { value: 'andaman', label: 'Andaman Sea' },
  ];

  // Center map on Indian Ocean
  const mapCenter: LatLngExpression = [15, 75];
  const mapZoom = 6;

  if (isLoading) {
    return (
      <>
        <Nav />
        <div className="min-h-screen bg-deep-950 pt-20 flex items-center justify-center">
          <LoadingSpinner />
        </div>
        <Footer />
      </>
    );
  }

  if (error) {
    return (
      <>
        <Nav />
        <div className="min-h-screen bg-deep-950 pt-20 flex items-center justify-center">
          <div className="text-center">
            <MapPin className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-2">Failed to Load Map Data</h2>
            <p className="text-gray-400">Please try refreshing the page</p>
          </div>
        </div>
        <Footer />
      </>
    );
  }

  return (
    <ErrorBoundary>
      <Nav />
      <div className="min-h-screen bg-deep-950 pt-20">
        {/* Header */}
        <div className="bg-deep-900 border-b border-deep-700">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">Interactive Float Map</h1>
                <p className="text-gray-400">
                  Explore {filteredFloats.length} of {floats.length} active Argo floats in real-time
                </p>
              </div>
              
              {/* Map Controls */}
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center gap-2 px-4 py-2 bg-deep-800 text-white rounded-lg hover:bg-deep-700 transition-colors"
                >
                  <Filter className="w-4 h-4" />
                  Filters
                </button>
                
                <select
                  value={mapView}
                  onChange={(e) => setMapView(e.target.value as any)}
                  className="px-3 py-2 bg-deep-800 text-white rounded-lg border border-deep-700 focus:border-ocean-500 focus:outline-none"
                >
                  <option value="satellite">Satellite</option>
                  <option value="terrain">Terrain</option>
                  <option value="street">Street</option>
                </select>
                
                <button className="p-2 bg-deep-800 text-white rounded-lg hover:bg-deep-700 transition-colors">
                  <Maximize2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            {/* Filters Panel */}
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-6 p-4 bg-deep-800 rounded-lg border border-deep-700"
              >
                <div className="grid md:grid-cols-4 gap-4">
                  {/* Search */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Search</label>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Float ID or location..."
                        value={mapFilters.searchTerm}
                        onChange={(e) => setMapFilters(prev => ({ ...prev, searchTerm: e.target.value }))}
                        className="w-full pl-10 pr-3 py-2 bg-deep-700 text-white rounded-lg border border-deep-600 focus:border-ocean-500 focus:outline-none"
                      />
                    </div>
                  </div>
                  
                  {/* Region */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Region</label>
                    <select
                      value={mapFilters.region}
                      onChange={(e) => setMapFilters(prev => ({ ...prev, region: e.target.value }))}
                      className="w-full px-3 py-2 bg-deep-700 text-white rounded-lg border border-deep-600 focus:border-ocean-500 focus:outline-none"
                    >
                      {regions.map(region => (
                        <option key={region.value} value={region.value}>{region.label}</option>
                      ))}
                    </select>
                  </div>
                  
                  {/* Temperature Range */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Temperature: {mapFilters.minTemp}°C - {mapFilters.maxTemp}°C
                    </label>
                    <div className="flex gap-2">
                      <input
                        type="range"
                        min="0"
                        max="35"
                        value={mapFilters.minTemp}
                        onChange={(e) => setMapFilters(prev => ({ ...prev, minTemp: Number(e.target.value) }))}
                        className="flex-1"
                      />
                      <input
                        type="range"
                        min="0"
                        max="35"
                        value={mapFilters.maxTemp}
                        onChange={(e) => setMapFilters(prev => ({ ...prev, maxTemp: Number(e.target.value) }))}
                        className="flex-1"
                      />
                    </div>
                  </div>
                  
                  {/* Depth Range */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Max Depth: {mapFilters.minDepth}m - {mapFilters.maxDepth}m
                    </label>
                    <div className="flex gap-2">
                      <input
                        type="range"
                        min="0"
                        max="5000"
                        step="100"
                        value={mapFilters.minDepth}
                        onChange={(e) => setMapFilters(prev => ({ ...prev, minDepth: Number(e.target.value) }))}
                        className="flex-1"
                      />
                      <input
                        type="range"
                        min="0"
                        max="5000"
                        step="100"
                        value={mapFilters.maxDepth}
                        onChange={(e) => setMapFilters(prev => ({ ...prev, maxDepth: Number(e.target.value) }))}
                        className="flex-1"
                      />
                    </div>
                  </div>
                </div>
                
                {/* Clear Filters */}
                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => setMapFilters({
                      minTemp: 0,
                      maxTemp: 35,
                      minDepth: 0,
                      maxDepth: 5000,
                      region: 'all',
                      searchTerm: ''
                    })}
                    className="px-4 py-2 text-ocean-400 hover:text-ocean-300 transition-colors"
                  >
                    Clear All Filters
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        <div className="flex h-[calc(100vh-200px)]">
          {/* Map Area */}
          <div className="flex-1 relative bg-deep-900">
            {/* Temperature Legend */}
            <div className="absolute top-4 left-4 z-10 bg-deep-800/90 backdrop-blur rounded-lg p-4 border border-deep-700">
              <h3 className="text-sm font-semibold text-white mb-3">Temperature Legend</h3>
              <div className="space-y-2">
                {[
                  { color: '#ef4444', range: '> 28°C', label: 'Very Warm' },
                  { color: '#f97316', range: '26-28°C', label: 'Warm' },
                  { color: '#eab308', range: '24-26°C', label: 'Moderate' },
                  { color: '#22c55e', range: '22-24°C', label: 'Cool' },
                  { color: '#3b82f6', range: '< 22°C', label: 'Cold' },
                ].map((item, index) => (
                  <div key={index} className="flex items-center gap-2 text-xs">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-gray-300">{item.range}</span>
                    <span className="text-gray-400">({item.label})</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Real Interactive Map */}
            <div className="w-full h-full relative">
              {isLoading ? (
                <div className="w-full h-full bg-deep-900 flex items-center justify-center">
                  <LoadingSpinner size="large" />
                </div>
              ) : (
                <MapContainer
                  center={mapCenter}
                  zoom={mapZoom}
                  style={{ height: '100%', width: '100%' }}
                  className="z-0"
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  
                  {/* Render float markers */}
                  {filteredFloats.map((float) => (
                    <Marker
                      key={float.PLATFORM_NUMBER}
                      position={[float.LATITUDE, float.LONGITUDE]}
                      icon={createMarkerIcon(float)}
                      eventHandlers={{
                        click: () => handleFloatClick(float),
                      }}
                    >
                      <Popup>
                        <div className="p-2 min-w-[200px]">
                          <h4 className="font-semibold text-deep-900 mb-2">
                            🚢 Float {float.PLATFORM_NUMBER}
                          </h4>
                          <div className="space-y-1 text-sm">
                            <p><strong>📍 Position:</strong> {float.LATITUDE.toFixed(3)}°N, {float.LONGITUDE.toFixed(3)}°E</p>
                            <p><strong>🌡️ Temperature:</strong> {float.AVG_TEMP.toFixed(1)}°C</p>
                            <p><strong>🧂 Salinity:</strong> {float.AVG_SALINITY.toFixed(1)} PSU</p>
                            <p><strong>🌊 Max Depth:</strong> {float.MAX_DEPTH.toFixed(0)}m</p>
                            <p><strong>🔄 Cycles:</strong> {float.MAX_CYCLE}</p>
                            <p><strong>📅 Last Update:</strong> {new Date(float.LAST_DATE).toLocaleDateString()}</p>
                            <p><strong>📍 Location:</strong> {float.LOCATION}</p>
                          </div>
                        </div>
                      </Popup>
                    </Marker>
                  ))}
                </MapContainer>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="w-80 bg-deep-900 border-l border-deep-700 overflow-y-auto">
            {selectedFloat ? (
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Float Details</h3>
                  <button
                    onClick={() => setSelectedFloat(null)}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    ×
                  </button>
                </div>
                
                <div className="space-y-4">
                  {/* Float ID */}
                  <div className="p-4 bg-deep-800 rounded-lg">
                    <div className="text-sm text-gray-400 mb-1">Platform Number</div>
                    <div className="text-xl font-bold text-white">{selectedFloat.PLATFORM_NUMBER}</div>
                  </div>
                  
                  {/* Location */}
                  <div className="p-4 bg-deep-800 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <MapPin className="w-4 h-4 text-ocean-400" />
                      <span className="text-sm text-gray-400">Location</span>
                    </div>
                    <div className="text-white font-medium mb-1">{selectedFloat.LOCATION}</div>
                    <div className="text-sm text-gray-400">
                      {selectedFloat.LATITUDE.toFixed(4)}°N, {selectedFloat.LONGITUDE.toFixed(4)}°E
                    </div>
                  </div>
                  
                  {/* Temperature */}
                  <div className="p-4 bg-deep-800 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Thermometer className="w-4 h-4 text-red-400" />
                      <span className="text-sm text-gray-400">Temperature</span>
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">
                      {selectedFloat.AVG_TEMP.toFixed(1)}°C
                    </div>
                    <div className="text-sm" style={{ color: getFloatColor(selectedFloat.AVG_TEMP) }}>
                      {getTemperatureCategory(selectedFloat.AVG_TEMP)}
                    </div>
                  </div>
                  
                  {/* Salinity */}
                  <div className="p-4 bg-deep-800 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Droplets className="w-4 h-4 text-blue-400" />
                      <span className="text-sm text-gray-400">Salinity</span>
                    </div>
                    <div className="text-2xl font-bold text-white">
                      {selectedFloat.AVG_SALINITY.toFixed(2)} PSU
                    </div>
                  </div>
                  
                  {/* Activity */}
                  <div className="p-4 bg-deep-800 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Activity className="w-4 h-4 text-green-400" />
                      <span className="text-sm text-gray-400">Activity</span>
                    </div>
                    <div className="space-y-1">
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-300">Max Depth:</span>
                        <span className="text-sm text-white">{selectedFloat.MAX_DEPTH.toFixed(0)}m</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-300">Cycles:</span>
                        <span className="text-sm text-white">{selectedFloat.MAX_CYCLE}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-gray-300">Last Update:</span>
                        <span className="text-sm text-white">
                          {new Date(selectedFloat.LAST_DATE).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Action Buttons */}
                  <div className="space-y-2">
                    <button className="w-full px-4 py-2 bg-ocean-600 hover:bg-ocean-700 text-white rounded-lg transition-colors">
                      View Detailed Analysis
                    </button>
                    <button className="w-full px-4 py-2 bg-deep-800 hover:bg-deep-700 text-white rounded-lg border border-deep-600 transition-colors">
                      Download Data
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-6 text-center text-gray-400">
                <Info className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Click on a float marker to view detailed information</p>
              </div>
            )}
          </div>
        </div>
      </div>
      <Footer />
    </ErrorBoundary>
  );
};

export default InteractiveMapPage;
