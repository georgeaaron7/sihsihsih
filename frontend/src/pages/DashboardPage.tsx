import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Grid, List, Filter, Settings } from 'lucide-react';
import FloatList from '../components/FloatList';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

const DashboardPage: React.FC = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filters, setFilters] = useState({
    region: '',
    minTemp: undefined as number | undefined,
    maxTemp: undefined as number | undefined,
  });
  const [showFilters, setShowFilters] = useState(false);

  const handleFilterChange = (key: string, value: string | number | undefined) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const clearFilters = () => {
    setFilters({
      region: '',
      minTemp: undefined,
      maxTemp: undefined,
    });
  };

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
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                  Float Dashboard
                </h1>
                <p className="text-gray-400 text-lg">
                  Explore Argo floats across the Indian Ocean
                </p>
              </div>
              
              {/* Controls */}
              <div className="flex items-center gap-4">
                {/* View Mode Toggle */}
                <div className="flex items-center bg-deep-800 p-1 rounded-lg border border-deep-600">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded transition-colors ${
                      viewMode === 'grid'
                        ? 'bg-ocean-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                    aria-label="Grid view"
                  >
                    <Grid className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded transition-colors ${
                      viewMode === 'list'
                        ? 'bg-ocean-600 text-white'
                        : 'text-gray-400 hover:text-white'
                    }`}
                    aria-label="List view"
                  >
                    <List className="w-5 h-5" />
                  </button>
                </div>

                {/* Filter Toggle */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className={`btn-secondary flex items-center gap-2 ${
                    showFilters ? 'bg-ocean-600 border-ocean-500' : ''
                  }`}
                >
                  <Filter className="w-4 h-4" />
                  Filters
                </button>

                {/* Settings */}
                <button className="btn-secondary p-3" aria-label="Settings">
                  <Settings className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-deep-900 border-b border-deep-700"
          >
            <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Region
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., Bay of Bengal"
                    value={filters.region}
                    onChange={(e) => handleFilterChange('region', e.target.value)}
                    className="w-full px-3 py-2 bg-deep-800 border border-deep-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Min Temperature (°C)
                  </label>
                  <input
                    type="number"
                    placeholder="20"
                    value={filters.minTemp || ''}
                    onChange={(e) => handleFilterChange('minTemp', e.target.value ? parseFloat(e.target.value) : undefined)}
                    className="w-full px-3 py-2 bg-deep-800 border border-deep-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Max Temperature (°C)
                  </label>
                  <input
                    type="number"
                    placeholder="30"
                    value={filters.maxTemp || ''}
                    onChange={(e) => handleFilterChange('maxTemp', e.target.value ? parseFloat(e.target.value) : undefined)}
                    className="w-full px-3 py-2 bg-deep-800 border border-deep-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
                  />
                </div>
                
                <div className="flex items-end">
                  <button
                    onClick={clearFilters}
                    className="w-full btn-secondary"
                  >
                    Clear Filters
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          <FloatList
            viewMode={viewMode}
            filters={filters}
          />
        </main>
      </motion.div>

      <Footer />
    </div>
  );
};

export default DashboardPage;
