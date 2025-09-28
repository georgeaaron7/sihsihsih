import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import { Play, ChevronRight } from 'lucide-react';

// Sample Lottie animation data for logo (replace with actual logo.json)
const sampleLogoAnimation = {
  v: "5.7.4",
  fr: 60,
  ip: 0,
  op: 120,
  w: 200,
  h: 200,
  nm: "Argo Logo",
  ddd: 0,
  assets: [],
  layers: [
    {
      ddd: 0,
      ind: 1,
      ty: 4,
      nm: "Circle",
      sr: 1,
      ks: {
        o: { a: 0, k: 100 },
        r: { a: 1, k: [
          { i: { x: [0.833], y: [0.833] }, o: { x: [0.167], y: [0.167] }, t: 0, s: [0] },
          { t: 120, s: [360] }
        ]},
        p: { a: 0, k: [100, 100, 0] },
        a: { a: 0, k: [0, 0, 0] },
        s: { a: 0, k: [100, 100, 100] }
      },
      ao: 0,
      shapes: [
        {
          ty: "el",
          p: { a: 0, k: [0, 0] },
          s: { a: 0, k: [80, 80] }
        },
        {
          ty: "fl",
          c: { a: 0, k: [0.054, 0.647, 0.914, 1] },
          o: { a: 0, k: 100 }
        }
      ],
      ip: 0,
      op: 120,
      st: 0
    }
  ]
};

interface LandingHeroProps {
  videoSrc?: string;
  posterSrc?: string;
  blurredPosterSrc?: string;
}

const LandingHero: React.FC<LandingHeroProps> = ({
  videoSrc = '/videos/ocean-background.mp4',
  posterSrc = '/images/ocean-poster.jpg',
  blurredPosterSrc = '/images/ocean-poster-blur.jpg'
}) => {
  const navigate = useNavigate();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [showPlayButton, setShowPlayButton] = useState(false);
  const [logoAnimationComplete, setLogoAnimationComplete] = useState(false);
  
  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth < 768;

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleCanPlay = () => {
      setVideoLoaded(true);
      // Try to autoplay
      const playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise.catch(() => {
          // Autoplay was prevented
          setShowPlayButton(true);
        });
      }
    };

    const handleLoadedData = () => {
      setVideoLoaded(true);
    };

    video.addEventListener('canplay', handleCanPlay);
    video.addEventListener('loadeddata', handleLoadedData);

    return () => {
      video.removeEventListener('canplay', handleCanPlay);
      video.removeEventListener('loadeddata', handleLoadedData);
    };
  }, []);

  const handlePlayVideo = () => {
    if (videoRef.current) {
      videoRef.current.play();
      setShowPlayButton(false);
    }
  };

  const handleNavigateToDashboard = () => {
    navigate('/dashboard');
  };

  const heroVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        ease: "easeOut"
      }
    }
  };

  const contentVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        delay: 0.3,
        ease: "easeOut"
      }
    }
  };

  const logoVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        duration: 1,
        ease: "easeOut"
      }
    }
  };

  return (
    <motion.section
      className="relative min-h-screen flex items-center justify-start overflow-hidden"
      variants={heroVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Background Video */}
      <div className="absolute inset-0 z-0">
        {/* Blurred placeholder that loads first */}
        {!videoLoaded && (
          <img
            src={blurredPosterSrc}
            alt="Ocean background placeholder"
            className="absolute inset-0 w-full h-full object-cover filter blur-sm"
            style={{ zIndex: -2 }}
          />
        )}
        
        <video
          ref={videoRef}
          className="absolute inset-0 w-full h-full object-cover"
          style={{ zIndex: -1 }}
          autoPlay
          muted
          loop
          playsInline
          poster={posterSrc}
          preload="metadata"
        >
          <source src={videoSrc} type="video/mp4" />
          <img src={posterSrc} alt="Ocean background fallback" />
        </video>

        {/* Play button overlay when autoplay is blocked */}
        {showPlayButton && (
          <motion.button
            className="absolute inset-0 flex items-center justify-center bg-black/30 backdrop-blur-sm z-10"
            onClick={handlePlayVideo}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            aria-label="Play background video"
          >
            <div className="bg-white/20 rounded-full p-6 backdrop-blur-md border border-white/30">
              <Play className="w-12 h-12 text-white ml-1" fill="currentColor" />
            </div>
          </motion.button>
        )}

        {/* Gradient overlay */}
        <div 
          className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-transparent"
          style={{ zIndex: 1 }}
        />
      </div>

      {/* Content */}
      <div className="relative z-20 max-w-7xl mx-auto px-6 lg:px-8 flex items-center min-h-screen">
        <div className="grid lg:grid-cols-2 gap-12 items-center w-full">
          {/* Left side - Text content */}
          <motion.div
            className="space-y-8"
            variants={contentVariants}
            initial="hidden"
            animate="visible"
          >
            <div className="space-y-6">
              <motion.h1 
                className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
              >
                <span className="text-white">Explore the</span>
                <br />
                <span className="text-gradient">Deep Ocean</span>
              </motion.h1>

              <motion.p 
                className="text-xl md:text-2xl text-gray-300 max-w-2xl leading-relaxed"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.7 }}
              >
                Discover real-time oceanographic data from Argo floats across the Indian Ocean. 
                Monitor temperature, salinity, and ocean currents with interactive visualizations.
              </motion.p>
            </div>

            <motion.div
              className="flex flex-col sm:flex-row gap-4"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.9 }}
            >
              <button
                onClick={handleNavigateToDashboard}
                className="btn-primary text-lg px-8 py-4 flex items-center gap-3 group"
              >
                Explore Dashboard
                <ChevronRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
              </button>
              
              <button className="btn-secondary text-lg px-8 py-4">
                Learn More
              </button>
            </motion.div>

            {/* Stats */}
            <motion.div 
              className="grid grid-cols-3 gap-6 pt-8 border-t border-white/20"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.1 }}
            >
              <div className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-ocean-400">50+</div>
                <div className="text-sm text-gray-400">Active Floats</div>
              </div>
              <div className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-ocean-400">24/7</div>
                <div className="text-sm text-gray-400">Monitoring</div>
              </div>
              <div className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-ocean-400">1000+</div>
                <div className="text-sm text-gray-400">Data Points</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Right side - Logo animation */}
          <motion.div
            className="flex justify-center lg:justify-end"
            variants={logoVariants}
            initial="hidden"
            animate="visible"
          >
            <div className="relative">
              {(!prefersReducedMotion && !isMobile) ? (
                <Lottie
                  animationData={sampleLogoAnimation}
                  className="w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96"
                  loop={logoAnimationComplete}
                  autoplay={true}
                  onComplete={() => setLogoAnimationComplete(true)}
                />
              ) : (
                // Static logo for reduced motion or mobile
                <div className="w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 bg-gradient-to-br from-ocean-500 to-ocean-700 rounded-full flex items-center justify-center">
                  <div className="text-white text-6xl md:text-8xl font-bold">A</div>
                </div>
              )}
              
              {/* Floating particles effect */}
              {!prefersReducedMotion && (
                <div className="absolute inset-0 pointer-events-none">
                  {[...Array(6)].map((_, i) => (
                    <motion.div
                      key={i}
                      className="absolute w-2 h-2 bg-ocean-400 rounded-full opacity-60"
                      style={{
                        left: `${20 + i * 10}%`,
                        top: `${30 + (i % 3) * 20}%`,
                      }}
                      animate={{
                        y: [-10, 10, -10],
                        opacity: [0.6, 1, 0.6],
                      }}
                      transition={{
                        duration: 3 + i * 0.5,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 right-8 text-white/60"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
      >
        <div className="flex flex-col items-center gap-2">
          <span className="text-sm">Scroll to explore</span>
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-1 h-8 bg-gradient-to-b from-transparent via-white to-transparent opacity-60"
          />
        </div>
      </motion.div>
    </motion.section>
  );
};

export default LandingHero;
