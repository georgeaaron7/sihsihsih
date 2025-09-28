import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, Area, AreaChart } from 'recharts';
import { TrendingUp, Thermometer, Droplets, Activity, Calendar, BarChart3, Map, Download } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { argoApi, FloatInfo, ProfileData, TemperatureSeries } from '../lib/apiClient';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorBoundary from '../components/ErrorBoundary';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

const FloatAnalysisPage: React.FC = () => {
  const [selectedFloatId, setSelectedFloatId] = useState<number | null>(null);
  const [analysisType, setAnalysisType] = useState<'profiles' | 'timeseries' | 'comparison'>('profiles');

  // Get all floats
  const { data: floats = [], isLoading: floatsLoading } = useQuery({
    queryKey: ['floats'],
    queryFn: () => argoApi.getFloats(),
    staleTime: 5 * 60 * 1000,
  });

  // Get selected float details
  const { data: floatDetails, isLoading: detailsLoading } = useQuery({
    queryKey: ['float-details', selectedFloatId],
    queryFn: () => selectedFloatId ? argoApi.getFloatDetails(selectedFloatId) : null,
    enabled: !!selectedFloatId,
  });

  // Get temperature time series
  const { data: temperatureSeries, isLoading: seriesLoading } = useQuery({
    queryKey: ['temperature-series', selectedFloatId],
    queryFn: () => selectedFloatId ? argoApi.getTemperatureSeries(selectedFloatId) : null,
    enabled: !!selectedFloatId,
  });

  // Process profile data for charts
  const profileChartData = useMemo(() => {
    if (!floatDetails?.profiles || floatDetails.profiles.length === 0) {
      return { temperature: [], salinity: [], tsData: [] };
    }

    const profiles = floatDetails.profiles;
    const latestCycle = Math.max(...profiles.map(p => p.CYCLE_NUMBER));
    const latestProfile = profiles.filter(p => p.CYCLE_NUMBER === latestCycle);

    // Sort by pressure (depth) and filter out invalid data
    const sortedProfile = latestProfile
      .filter(p => p.PRES >= 0 && !isNaN(p.PRES) && !isNaN(p.TEMP) && !isNaN(p.PSAL))
      .sort((a, b) => a.PRES - b.PRES);

    const temperature = sortedProfile
      .filter(p => p.TEMP !== null && p.TEMP !== undefined)
      .map(p => ({
        depth: -p.PRES, // Negative for proper depth display
        temperature: Number(p.TEMP.toFixed(2)),
        pressure: p.PRES
      }));

    const salinity = sortedProfile
      .filter(p => p.PSAL !== null && p.PSAL !== undefined)
      .map(p => ({
        depth: -p.PRES,
        salinity: Number(p.PSAL.toFixed(3)),
        pressure: p.PRES
      }));

    const tsData = sortedProfile
      .filter(p => p.TEMP !== null && p.TEMP !== undefined && p.PSAL !== null && p.PSAL !== undefined)
      .map(p => ({
        salinity: Number(p.PSAL.toFixed(3)),
        temperature: Number(p.TEMP.toFixed(2)),
        pressure: p.PRES
      }));

    return { temperature, salinity, tsData };
  }, [floatDetails]);

  // Process time series data
  const timeSeriesData = useMemo(() => {
    if (!temperatureSeries) return [];

    return temperatureSeries.map(item => ({
      date: new Date(item.date).toLocaleDateString(),
      temperature: item.temperature,
      depth: item.depth,
      cycle: item.cycle
    }));
  }, [temperatureSeries]);

  const selectedFloat = floats.find(f => f.PLATFORM_NUMBER === selectedFloatId);

  const isLoading = floatsLoading || detailsLoading || seriesLoading;

  if (floatsLoading) {
    return (
      <div className="min-h-screen bg-deep-950 pt-20 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-deep-950">
        <Nav />
        <div className="pt-20">
        {/* Header */}
        <div className="bg-deep-900 border-b border-deep-700">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">Float Analysis Dashboard</h1>
                <p className="text-gray-400">
                  Comprehensive analysis of oceanographic data from Argo floats
                </p>
              </div>
              
              {selectedFloat && (
                <div className="flex items-center gap-4">
                  <button className="flex items-center gap-2 px-4 py-2 bg-ocean-600 hover:bg-ocean-700 text-white rounded-lg transition-colors">
                    <Download className="w-4 h-4" />
                    Export Data
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-8">
          {/* Float Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Select Float for Analysis</h2>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {floats.map((float) => (
                  <button
                    key={float.PLATFORM_NUMBER}
                    onClick={() => setSelectedFloatId(float.PLATFORM_NUMBER)}
                    className={`p-4 rounded-lg border transition-all duration-300 text-left ${
                      selectedFloatId === float.PLATFORM_NUMBER
                        ? 'border-ocean-500 bg-ocean-500/10'
                        : 'border-deep-600 bg-deep-700 hover:border-deep-500'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-white">Float {float.PLATFORM_NUMBER}</span>
                      <div className="flex items-center gap-1">
                        <Thermometer className="w-4 h-4 text-red-400" />
                        <span className="text-sm text-gray-300">{float.AVG_TEMP.toFixed(1)}°C</span>
                      </div>
                    </div>
                    <div className="text-sm text-gray-400 mb-1">{float.LOCATION}</div>
                    <div className="text-xs text-gray-500">
                      Last update: {new Date(float.LAST_DATE).toLocaleDateString()}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Analysis Type Selector */}
          {selectedFloat && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="mb-8"
            >
              <div className="flex flex-wrap gap-3 justify-center">
                <button
                  onClick={() => setAnalysisType('profiles')}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg border transition-all duration-300 ${
                    analysisType === 'profiles'
                      ? 'bg-ocean-600 text-white border-ocean-500'
                      : 'bg-deep-800 text-gray-300 border-deep-700 hover:bg-deep-700'
                  }`}
                >
                  <BarChart3 className="w-4 h-4" />
                  Vertical Profiles
                </button>
                <button
                  onClick={() => setAnalysisType('timeseries')}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg border transition-all duration-300 ${
                    analysisType === 'timeseries'
                      ? 'bg-ocean-600 text-white border-ocean-500'
                      : 'bg-deep-800 text-gray-300 border-deep-700 hover:bg-deep-700'
                  }`}
                >
                  <TrendingUp className="w-4 h-4" />
                  Time Series
                </button>
                <button
                  onClick={() => setAnalysisType('comparison')}
                  className={`flex items-center gap-2 px-6 py-3 rounded-lg border transition-all duration-300 ${
                    analysisType === 'comparison'
                      ? 'bg-ocean-600 text-white border-ocean-500'
                      : 'bg-deep-800 text-gray-300 border-deep-700 hover:bg-deep-700'
                  }`}
                >
                  <Activity className="w-4 h-4" />
                  T-S Analysis
                </button>
              </div>
            </motion.div>
          )}

          {/* Float Information Panel */}
          {selectedFloat && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mb-8"
            >
              <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
                <h3 className="text-xl font-semibold text-white mb-4">
                  Float {selectedFloat.PLATFORM_NUMBER} - Overview
                </h3>
                
                <div className="grid md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-red-500/10 rounded-lg mx-auto mb-3">
                      <Thermometer className="w-6 h-6 text-red-400" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">
                      {selectedFloat.AVG_TEMP.toFixed(1)}°C
                    </div>
                    <div className="text-sm text-gray-400">Avg Temperature</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-blue-500/10 rounded-lg mx-auto mb-3">
                      <Droplets className="w-6 h-6 text-blue-400" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">
                      {selectedFloat.AVG_SALINITY.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-400">Avg Salinity (PSU)</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-green-500/10 rounded-lg mx-auto mb-3">
                      <Activity className="w-6 h-6 text-green-400" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">
                      {selectedFloat.MAX_DEPTH.toFixed(0)}m
                    </div>
                    <div className="text-sm text-gray-400">Max Depth</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-purple-500/10 rounded-lg mx-auto mb-3">
                      <Calendar className="w-6 h-6 text-purple-400" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-1">
                      {selectedFloat.MAX_CYCLE}
                    </div>
                    <div className="text-sm text-gray-400">Total Cycles</div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Analysis Charts */}
          {selectedFloat && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center py-20">
                  <LoadingSpinner />
                </div>
              ) : (
                <div className="space-y-8">
                  {/* Vertical Profiles */}
                  {analysisType === 'profiles' && (
                    <div className="grid lg:grid-cols-2 gap-8">
                      {/* Temperature Profile */}
                      <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
                        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                          <Thermometer className="w-5 h-5 text-red-400" />
                          Temperature Profile
                        </h3>
                        <div className="h-80">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={profileChartData.temperature}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                              <XAxis 
                                dataKey="temperature" 
                                stroke="#9CA3AF"
                                domain={['dataMin', 'dataMax']}
                                type="number"
                                tickFormatter={(value) => `${value.toFixed(1)}°C`}
                                label={{ value: 'Temperature (°C)', position: 'insideBottom', offset: -10 }}
                              />
                              <YAxis 
                                dataKey="depth" 
                                stroke="#9CA3AF"
                                domain={['dataMin', 'dataMax']}
                                type="number"
                                tickFormatter={(value) => `${Math.abs(value).toFixed(0)}m`}
                                label={{ value: 'Depth (m)', angle: -90, position: 'insideLeft' }}
                              />
                              <Tooltip 
                                contentStyle={{ 
                                  backgroundColor: '#1F2937', 
                                  border: '1px solid #374151',
                                  borderRadius: '8px'
                                }}
                                labelStyle={{ color: '#F3F4F6' }}
                                formatter={(value: any, name: string) => [
                                  name === 'temperature' ? `${value.toFixed(1)}°C` : value,
                                  name === 'temperature' ? 'Temperature' : name
                                ]}
                                labelFormatter={(label) => `Depth: ${Math.abs(Number(label)).toFixed(0)}m`}
                              />
                              <Line 
                                type="monotone" 
                                dataKey="temperature" 
                                stroke="#EF4444" 
                                strokeWidth={3}
                                dot={{ fill: '#EF4444', strokeWidth: 2, r: 4 }}
                                connectNulls={false}
                              />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </div>

                      {/* Salinity Profile */}
                      <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
                        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                          <Droplets className="w-5 h-5 text-blue-400" />
                          Salinity Profile
                        </h3>
                        <div className="h-80">
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={profileChartData.salinity}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                              <XAxis 
                                dataKey="salinity" 
                                stroke="#9CA3AF"
                                domain={['dataMin', 'dataMax']}
                                type="number"
                                tickFormatter={(value) => `${value.toFixed(1)} PSU`}
                                label={{ value: 'Salinity (PSU)', position: 'insideBottom', offset: -10 }}
                              />
                              <YAxis 
                                dataKey="depth" 
                                stroke="#9CA3AF"
                                domain={['dataMin', 'dataMax']}
                                type="number"
                                tickFormatter={(value) => `${Math.abs(value).toFixed(0)}m`}
                                label={{ value: 'Depth (m)', angle: -90, position: 'insideLeft' }}
                              />
                              <Tooltip 
                                contentStyle={{ 
                                  backgroundColor: '#1F2937', 
                                  border: '1px solid #374151',
                                  borderRadius: '8px'
                                }}
                                labelStyle={{ color: '#F3F4F6' }}
                                formatter={(value: any, name: string) => [
                                  name === 'salinity' ? `${value.toFixed(2)} PSU` : value,
                                  name === 'salinity' ? 'Salinity' : name
                                ]}
                                labelFormatter={(label) => `Depth: ${Math.abs(Number(label)).toFixed(0)}m`}
                              />
                              <Line 
                                type="monotone" 
                                dataKey="salinity" 
                                stroke="#3B82F6" 
                                strokeWidth={3}
                                dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                                connectNulls={false}
                              />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Time Series */}
                  {analysisType === 'timeseries' && (
                    <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
                      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-green-400" />
                        Temperature Time Series
                      </h3>
                      <div className="h-96">
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={timeSeriesData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis 
                              dataKey="date" 
                              stroke="#9CA3AF"
                              angle={-45}
                              textAnchor="end"
                              height={80}
                            />
                            <YAxis 
                              stroke="#9CA3AF"
                              label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
                            />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: '#1F2937', 
                                border: '1px solid #374151',
                                borderRadius: '8px'
                              }}
                              labelStyle={{ color: '#F3F4F6' }}
                            />
                            <Area 
                              type="monotone" 
                              dataKey="temperature" 
                              stroke="#10B981" 
                              fill="url(#colorTemp)"
                              strokeWidth={2}
                            />
                            <defs>
                              <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                              </linearGradient>
                            </defs>
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}

                  {/* T-S Diagram */}
                  {analysisType === 'comparison' && (
                    <div className="bg-deep-800 rounded-xl border border-deep-700 p-6">
                      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Activity className="w-5 h-5 text-purple-400" />
                        Temperature-Salinity Diagram
                      </h3>
                      <div className="h-96">
                        <ResponsiveContainer width="100%" height="100%">
                          <ScatterChart data={profileChartData.tsData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis 
                              dataKey="salinity" 
                              stroke="#9CA3AF"
                              domain={['dataMin', 'dataMax']}
                              type="number"
                              tickFormatter={(value) => `${value.toFixed(1)}`}
                              label={{ value: 'Salinity (PSU)', position: 'insideBottom', offset: -10 }}
                            />
                            <YAxis 
                              dataKey="temperature" 
                              stroke="#9CA3AF"
                              domain={['dataMin', 'dataMax']}
                              type="number"
                              tickFormatter={(value) => `${value.toFixed(1)}`}
                              label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }}
                            />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: '#1F2937', 
                                border: '1px solid #374151',
                                borderRadius: '8px'
                              }}
                              labelStyle={{ color: '#F3F4F6' }}
                              formatter={(value: any, name: string) => [
                                `${value.toFixed(2)} ${name === 'temperature' ? '°C' : 'PSU'}`,
                                name === 'temperature' ? 'Temperature' : 'Salinity'
                              ]}
                              labelFormatter={(_label, payload) => {
                                if (payload && payload[0]) {
                                  return `Pressure: ${payload[0].payload.pressure.toFixed(0)} dbar`;
                                }
                                return '';
                              }}
                            />
                            <Scatter 
                              dataKey="temperature" 
                              fill="#8B5CF6"
                              r={4}
                            />
                          </ScatterChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          )}

          {/* No Float Selected */}
          {!selectedFloat && (
            <div className="text-center py-20">
              <Map className="w-20 h-20 text-gray-600 mx-auto mb-6" />
              <h3 className="text-2xl font-semibold text-white mb-4">Select a Float to Begin Analysis</h3>
              <p className="text-gray-400 max-w-md mx-auto">
                Choose an Argo float from the selection above to view detailed oceanographic analysis including 
                vertical profiles, time series data, and temperature-salinity relationships.
              </p>
            </div>
          )}
        </div>
        </div>
        <Footer />
      </div>
    </ErrorBoundary>
  );
};

export default FloatAnalysisPage;
