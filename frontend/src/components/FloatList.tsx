import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, Variants } from 'framer-motion';
import { useQuery, useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { MapPin, Thermometer, Droplets, Activity, ChevronRight } from 'lucide-react';
import { argoApi, FloatInfo } from '../lib/apiClient';
import LoadingSpinner from './LoadingSpinner';

interface FloatListProps {
  viewMode?: 'grid' | 'list';
  filters?: {
    region?: string;
    minTemp?: number;
    maxTemp?: number;
  };
}

const FloatList: React.FC<FloatListProps> = ({ 
  viewMode = 'grid',
  filters 
}) => {
  const navigate = useNavigate();

  // Fetch floats data
  const {
    data: floats,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['floats', filters],
    queryFn: () => argoApi.getFloats(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });

  // Float click mutation
  const floatClickMutation = useMutation({
    mutationFn: (platformNumber: number) =>
      argoApi.logFloatClick(platformNumber, {
        source: 'frontend',
        action: 'select'
      }),
    onSuccess: (data, platformNumber) => {
      console.log(`✅ Float ${platformNumber} click logged`, data);
      // Navigate to detail page
      navigate(`/float/${platformNumber}`);
    },
    onError: (error, platformNumber) => {
      console.error(`❌ Failed to log click for float ${platformNumber}:`, error);
      toast.error(`Failed to log interaction with float ${platformNumber}`);
      // Still navigate even if logging fails
      navigate(`/float/${platformNumber}`);
    },
  });

  const handleFloatClick = (platformNumber: number) => {
    floatClickMutation.mutate(platformNumber);
  };

  const handleRetry = () => {
    refetch();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingSpinner size="large" text="Loading float data..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="card max-w-md mx-auto p-8">
          <div className="text-red-400 mb-4">
            <Activity className="w-12 h-12 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Failed to Load Floats</h3>
            <p className="text-gray-400 text-sm mb-4">
              Unable to fetch float data. Please check your connection and try again.
            </p>
          </div>
          <button onClick={handleRetry} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!floats || floats.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="card max-w-md mx-auto p-8">
          <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">No Floats Found</h3>
          <p className="text-gray-400 text-sm">
            No floats match your current filters. Try adjusting your search criteria.
          </p>
        </div>
      </div>
    );
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.4,
        ease: "easeOut"
      }
    }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className={`grid gap-6 ${
        viewMode === 'grid'
          ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
          : 'grid-cols-1'
      }`}
    >
      {floats.map((float) => (
        <FloatCard
          key={float.PLATFORM_NUMBER}
          float={float}
          viewMode={viewMode}
          onClick={() => handleFloatClick(float.PLATFORM_NUMBER)}
          isLoading={floatClickMutation.isLoading && 
                     floatClickMutation.variables === float.PLATFORM_NUMBER}
          variants={itemVariants}
        />
      ))}
    </motion.div>
  );
};

interface FloatCardProps {
  float: FloatInfo;
  viewMode: 'grid' | 'list';
  onClick: () => void;
  isLoading: boolean;
  variants: Variants;
}

const FloatCard: React.FC<FloatCardProps> = ({
  float,
  viewMode,
  onClick,
  isLoading,
  variants
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusColor = (temp: number) => {
    if (temp > 28) return 'text-red-400';
    if (temp > 25) return 'text-orange-400';
    if (temp > 20) return 'text-yellow-400';
    return 'text-blue-400';
  };

  return (
    <motion.div
      variants={variants}
      className={`card p-6 cursor-pointer group transition-all duration-300 ${
        isLoading ? 'opacity-50 cursor-wait' : 'hover:shadow-2xl hover:shadow-ocean-500/20'
      }`}
      onClick={onClick}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className={`${viewMode === 'list' ? 'flex items-center gap-6' : 'space-y-4'}`}>
        {/* Header */}
        <div className={`${viewMode === 'list' ? 'flex-shrink-0' : ''}`}>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xl font-bold text-white">
              Float {float.PLATFORM_NUMBER}
            </h3>
            <div className="flex items-center text-ocean-400">
              <ChevronRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
          
          <div className="flex items-center text-sm text-gray-400 mb-3">
            <MapPin className="w-4 h-4 mr-1" />
            <span>{float.LOCATION}</span>
          </div>
        </div>

        {/* Content */}
        <div className={`${viewMode === 'list' ? 'flex-1' : ''}`}>
          <div className={`grid ${viewMode === 'list' ? 'grid-cols-4' : 'grid-cols-2'} gap-4`}>
            {/* Position */}
            <div className="space-y-1">
              <div className="text-xs text-gray-500 uppercase tracking-wide">Position</div>
              <div className="text-sm font-medium">
                {float.LATITUDE.toFixed(2)}°N<br />
                {float.LONGITUDE.toFixed(2)}°E
              </div>
            </div>

            {/* Temperature */}
            <div className="space-y-1">
              <div className="text-xs text-gray-500 uppercase tracking-wide">Temperature</div>
              <div className={`text-sm font-medium flex items-center ${getStatusColor(float.AVG_TEMP)}`}>
                <Thermometer className="w-4 h-4 mr-1" />
                {float.AVG_TEMP.toFixed(1)}°C
              </div>
            </div>

            {/* Salinity */}
            <div className="space-y-1">
              <div className="text-xs text-gray-500 uppercase tracking-wide">Salinity</div>
              <div className="text-sm font-medium flex items-center text-cyan-400">
                <Droplets className="w-4 h-4 mr-1" />
                {float.AVG_SALINITY.toFixed(1)} PSU
              </div>
            </div>

            {/* Depth */}
            <div className="space-y-1">
              <div className="text-xs text-gray-500 uppercase tracking-wide">Max Depth</div>
              <div className="text-sm font-medium text-indigo-400">
                {float.MAX_DEPTH.toFixed(0)}m
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className={`${viewMode === 'list' ? 'mt-4' : 'mt-6'} pt-4 border-t border-gray-700 flex items-center justify-between`}>
            <div className="text-xs text-gray-500">
              Last update: {formatDate(float.LAST_DATE)}
            </div>
            <div className="text-xs text-ocean-400">
              {float.MAX_CYCLE} cycles
            </div>
          </div>
        </div>
      </div>

      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black/20 rounded-xl flex items-center justify-center">
          <LoadingSpinner size="small" />
        </div>
      )}
    </motion.div>
  );
};

export default FloatList;
