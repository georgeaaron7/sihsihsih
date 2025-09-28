import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, MapPin, Thermometer, Droplets, Activity } from 'lucide-react';
import { argoApi } from '../lib/apiClient';
import Nav from '../components/Nav';
import Footer from '../components/Footer';
import LoadingSpinner from '../components/LoadingSpinner';

const FloatDetailPage: React.FC = () => {
  const { platformNumber } = useParams<{ platformNumber: string }>();
  const floatId = Number(platformNumber);

  const {
    data: details,
    isLoading,
    error
  } = useQuery({
    queryKey: ['floatDetails', floatId],
    queryFn: () => argoApi.getFloatDetails(floatId),
    enabled: !!floatId,
  });

  const {
    data: profiles,
    isLoading: profilesLoading
  } = useQuery({
    queryKey: ['floatProfiles', floatId],
    queryFn: () => argoApi.getFloatProfiles(floatId, { latest: true }),
    enabled: !!floatId,
  });

  // const {
  //   data: temperatureSeries,
  //   isLoading: seriesLoading
  // } = useQuery({
  //   queryKey: ['temperatureSeries', floatId],
  //   queryFn: () => argoApi.getTemperatureSeries(floatId),
  //   enabled: !!floatId,
  // });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-deep-950">
        <Nav />
        <div className="pt-20 flex justify-center items-center min-h-[60vh]">
          <LoadingSpinner size="large" text="Loading float details..." />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !details) {
    return (
      <div className="min-h-screen bg-deep-950">
        <Nav />
        <div className="pt-20 max-w-4xl mx-auto px-6 py-12">
          <div className="card p-8 text-center">
            <Activity className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-white mb-4">Float Not Found</h1>
            <p className="text-gray-400 mb-6">
              The requested float could not be found or there was an error loading the data.
            </p>
            <Link to="/dashboard" className="btn-primary">
              Back to Dashboard
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-deep-950">
      <Nav />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="pt-20"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-deep-900 to-deep-800 border-b border-deep-700">
          <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
            <div className="flex items-center gap-4 mb-6">
              <Link
                to="/dashboard"
                className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                Back to Dashboard
              </Link>
            </div>
            
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                  Float {details.float_info.PLATFORM_NUMBER}
                </h1>
                <div className="flex items-center gap-4 text-gray-400">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-4 h-4" />
                    <span>{details.float_info.LOCATION}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Activity className="w-4 h-4" />
                    <span>{details.profile_count} profiles</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Float Summary */}
            <div className="lg:col-span-1">
              <div className="card p-6 space-y-6">
                <h2 className="text-xl font-bold text-white">Float Summary</h2>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3 border-b border-deep-700">
                    <span className="text-gray-400">Position</span>
                    <span className="text-white font-medium">
                      {details.float_info.LATITUDE.toFixed(4)}°N, {details.float_info.LONGITUDE.toFixed(4)}°E
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-3 border-b border-deep-700">
                    <span className="text-gray-400 flex items-center gap-2">
                      <Thermometer className="w-4 h-4" />
                      Temperature
                    </span>
                    <span className="text-orange-400 font-medium">
                      {details.float_info.AVG_TEMP.toFixed(1)}°C
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-3 border-b border-deep-700">
                    <span className="text-gray-400 flex items-center gap-2">
                      <Droplets className="w-4 h-4" />
                      Salinity
                    </span>
                    <span className="text-cyan-400 font-medium">
                      {details.float_info.AVG_SALINITY.toFixed(1)} PSU
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-3">
                    <span className="text-gray-400">Max Depth</span>
                    <span className="text-indigo-400 font-medium">
                      {details.float_info.MAX_DEPTH.toFixed(0)}m
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Profiles and Charts */}
            <div className="lg:col-span-2 space-y-8">
              {/* Latest Profiles */}
              <div className="card p-6">
                <h2 className="text-xl font-bold text-white mb-6">Latest Profiles</h2>
                
                {profilesLoading ? (
                  <div className="flex justify-center py-8">
                    <LoadingSpinner text="Loading profiles..." />
                  </div>
                ) : profiles && profiles.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-deep-700">
                          <th className="text-left py-3 text-gray-400">Cycle</th>
                          <th className="text-left py-3 text-gray-400">Date</th>
                          <th className="text-left py-3 text-gray-400">Depth (m)</th>
                          <th className="text-left py-3 text-gray-400">Temp (°C)</th>
                          <th className="text-left py-3 text-gray-400">Salinity</th>
                        </tr>
                      </thead>
                      <tbody>
                        {profiles.slice(0, 10).map((profile, index) => (
                          <tr key={index} className="border-b border-deep-800 hover:bg-deep-800/30">
                            <td className="py-3 text-white">{profile.CYCLE_NUMBER}</td>
                            <td className="py-3 text-gray-300">
                              {new Date(profile.JULD).toLocaleDateString()}
                            </td>
                            <td className="py-3 text-indigo-400">{profile.PRES.toFixed(1)}</td>
                            <td className="py-3 text-orange-400">{profile.TEMP.toFixed(2)}</td>
                            <td className="py-3 text-cyan-400">{profile.PSAL.toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-gray-400 text-center py-8">No profile data available</p>
                )}
              </div>

              {/* Temperature Series Chart
              <div className="card p-6">
                <h2 className="text-xl font-bold text-white mb-6">Temperature Time Series</h2>
                
                {seriesLoading ? (
                  <div className="flex justify-center py-8">
                    <LoadingSpinner text="Loading temperature data..." />
                  </div>
                ) : temperatureSeries && temperatureSeries.length > 0 ? (
                  <div className="h-64 flex items-center justify-center bg-deep-800 rounded-lg">
                    <p className="text-gray-400">
                      Chart visualization will be rendered here
                      <br />
                      <span className="text-sm">({temperatureSeries.length} data points)</span>
                    </p>
                  </div>
                ) : (
                  <p className="text-gray-400 text-center py-8">No temperature series data available</p>
                )}
              </div> */}
            </div>
          </div>
        </main>
      </motion.div>

      <Footer />
    </div>
  );
};

export default FloatDetailPage;
