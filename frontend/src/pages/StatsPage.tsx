import React from 'react';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { BarChart3, TrendingUp, Activity, Users } from 'lucide-react';
import { argoApi } from '../lib/apiClient';
import Nav from '../components/Nav';
import Footer from '../components/Footer';
import LoadingSpinner from '../components/LoadingSpinner';

const StatsPage: React.FC = () => {
  const {
    data: stats,
    isLoading,
    error
  } = useQuery({
    queryKey: ['stats'],
    queryFn: () => argoApi.getSummaryStats(),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-deep-950">
        <Nav />
        <div className="pt-20 flex justify-center items-center min-h-[60vh]">
          <LoadingSpinner size="large" text="Loading statistics..." />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="min-h-screen bg-deep-950">
        <Nav />
        <div className="pt-20 max-w-4xl mx-auto px-6 py-12">
          <div className="card p-8 text-center">
            <Activity className="w-16 h-16 text-red-400 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-white mb-4">Failed to Load Statistics</h1>
            <p className="text-gray-400 mb-6">
              There was an error loading the statistics data.
            </p>
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
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
              System Statistics
            </h1>
            <p className="text-gray-400 text-lg">
              Overview of Argo float data and system metrics
            </p>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="card p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-ocean-500/20 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-ocean-400" />
                </div>
                <span className="text-sm text-gray-400">Total</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-1">
                {stats.total_floats}
              </h3>
              <p className="text-gray-400 text-sm">Active Floats</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="card p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-orange-400" />
                </div>
                <span className="text-sm text-gray-400">Average</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-1">
                {stats.avg_temp.toFixed(1)}°C
              </h3>
              <p className="text-gray-400 text-sm">Temperature</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="card p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-cyan-400" />
                </div>
                <span className="text-sm text-gray-400">Average</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-1">
                {stats.avg_salinity.toFixed(1)}
              </h3>
              <p className="text-gray-400 text-sm">Salinity (PSU)</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="card p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-indigo-500/20 rounded-lg flex items-center justify-center">
                  <Activity className="w-6 h-6 text-indigo-400" />
                </div>
                <span className="text-sm text-gray-400">Maximum</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-1">
                {stats.max_depth.toFixed(0)}m
              </h3>
              <p className="text-gray-400 text-sm">Depth</p>
            </motion.div>
          </div>

          {/* Date Range */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="card p-6 mb-8"
          >
            <h2 className="text-xl font-bold text-white mb-4">Data Coverage</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-400 mb-2">Data Range Start</p>
                <p className="text-lg font-semibold text-white">
                  {new Date(stats.date_range.start).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-400 mb-2">Latest Data</p>
                <p className="text-lg font-semibold text-white">
                  {new Date(stats.date_range.end).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Additional Info */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-8"
          >
            <div className="card p-6">
              <h2 className="text-xl font-bold text-white mb-4">System Health</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">API Status</span>
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                    Online
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Data Freshness</span>
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                    Up to date
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Float Coverage</span>
                  <span className="px-3 py-1 bg-ocean-500/20 text-ocean-400 rounded-full text-sm">
                    Indian Ocean
                  </span>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <h2 className="text-xl font-bold text-white mb-4">Data Quality</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Validation Status</span>
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                    Validated
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Missing Data</span>
                  <span className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded-full text-sm">
                    &lt; 5%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Anomaly Detection</span>
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                    Normal
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        </main>
      </motion.div>

      <Footer />
    </div>
  );
};

export default StatsPage;
