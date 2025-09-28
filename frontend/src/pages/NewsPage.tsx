import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, ExternalLink, Globe, Waves, TrendingUp, AlertCircle } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import Nav from '../components/Nav';
import Footer from '../components/Footer';

interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  content: string;
  source: string;
  publishedAt: string;
  category: 'oceanography' | 'maritime' | 'climate' | 'research' | 'technology';
  imageUrl?: string;
  url?: string;
  importance: 'high' | 'medium' | 'low';
}

const NewsPage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      // In a real implementation, you would fetch from news APIs or your backend
      // For now, we'll use mock data
      const mockNews: NewsArticle[] = [
        {
          id: '1',
          title: 'Major Breakthrough in Ocean Temperature Monitoring',
          summary: 'Scientists develop new autonomous sensors that can track temperature changes with unprecedented accuracy.',
          content: 'Researchers have unveiled a revolutionary sensor technology that can monitor ocean temperature variations...',
          source: 'Ocean Research Institute',
          publishedAt: '2024-01-15T10:30:00Z',
          category: 'research',
          importance: 'high',
          imageUrl: '/images/ocean-sensors.jpg',
          url: 'https://example.com/ocean-sensors'
        },
        {
          id: '2',
          title: 'Argo Float Network Expands to Cover Arctic Waters',
          summary: 'New deployment of 200 Argo floats in the Arctic Ocean provides critical climate data.',
          content: 'The global Argo float network has expanded its coverage to include previously unmapped Arctic regions...',
          source: 'Arctic Climate Research Center',
          publishedAt: '2024-01-14T14:20:00Z',
          category: 'oceanography',
          importance: 'high',
          imageUrl: '/images/arctic-floats.jpg',
          url: 'https://example.com/arctic-expansion'
        },
        {
          id: '3',
          title: 'AI-Powered Maritime Traffic Optimization',
          summary: 'New AI system reduces fuel consumption and emissions in global shipping routes.',
          content: 'A groundbreaking artificial intelligence system is transforming maritime logistics...',
          source: 'Maritime Technology Review',
          publishedAt: '2024-01-13T09:15:00Z',
          category: 'technology',
          importance: 'medium',
          imageUrl: '/images/ai-maritime.jpg',
          url: 'https://example.com/ai-maritime'
        },
        {
          id: '4',
          title: 'Ocean Acidification Reaches Critical Levels',
          summary: 'Latest measurements show accelerating ocean acidification threatening marine ecosystems.',
          content: 'New data from the global ocean monitoring network reveals alarming trends in ocean pH levels...',
          source: 'Climate Science Today',
          publishedAt: '2024-01-12T16:45:00Z',
          category: 'climate',
          importance: 'high',
          imageUrl: '/images/ocean-acidification.jpg',
          url: 'https://example.com/ocean-acidification'
        },
        {
          id: '5',
          title: 'Revolutionary Deep-Sea Exploration Vehicle Launched',
          summary: 'New submersible can reach depths of 12,000 meters with advanced scientific equipment.',
          content: 'The latest addition to deep-sea exploration technology promises to unlock ocean mysteries...',
          source: 'Deep Sea Research Foundation',
          publishedAt: '2024-01-11T12:00:00Z',
          category: 'technology',
          importance: 'medium',
          imageUrl: '/images/deep-sea-vehicle.jpg',
          url: 'https://example.com/deep-sea-vehicle'
        },
        {
          id: '6',
          title: 'Sustainable Maritime Fuel Initiative Gains Momentum',
          summary: 'International shipping companies commit to 50% reduction in carbon emissions by 2030.',
          content: 'A coalition of major shipping companies has announced ambitious targets for reducing maritime emissions...',
          source: 'Green Maritime Alliance',
          publishedAt: '2024-01-10T08:30:00Z',
          category: 'maritime',
          importance: 'medium',
          imageUrl: '/images/green-shipping.jpg',
          url: 'https://example.com/green-shipping'
        }
      ];

      // Simulate API delay
      setTimeout(() => {
        setArticles(mockNews);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch news articles');
      setLoading(false);
    }
  };

  const categories = [
    { key: 'all', label: 'All News', icon: Globe },
    { key: 'oceanography', label: 'Oceanography', icon: Waves },
    { key: 'maritime', label: 'Maritime', icon: TrendingUp },
    { key: 'climate', label: 'Climate', icon: AlertCircle },
    { key: 'research', label: 'Research', icon: Calendar },
    { key: 'technology', label: 'Technology', icon: ExternalLink },
  ];

  const filteredArticles = selectedCategory === 'all' 
    ? articles 
    : articles.filter(article => article.category === selectedCategory);

  const getCategoryColor = (category: string) => {
    const colors = {
      oceanography: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
      maritime: 'bg-green-500/10 text-green-400 border-green-500/20',
      climate: 'bg-red-500/10 text-red-400 border-red-500/20',
      research: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
      technology: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    };
    return colors[category as keyof typeof colors] || 'bg-gray-500/10 text-gray-400 border-gray-500/20';
  };

  const getImportanceIcon = (importance: string) => {
    switch (importance) {
      case 'high':
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      case 'medium':
        return <TrendingUp className="w-4 h-4 text-yellow-400" />;
      default:
        return <Globe className="w-4 h-4 text-gray-400" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-deep-950 pt-20 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-deep-950 pt-20 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Error Loading News</h2>
          <p className="text-gray-400 mb-4">{error}</p>
          <button
            onClick={fetchNews}
            className="px-6 py-2 bg-ocean-600 hover:bg-ocean-700 text-white rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-deep-950">
      <Nav />
      <div className="pt-20">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">
            Ocean & Maritime News
          </h1>
          <p className="text-xl text-gray-400">
            Stay updated with the latest developments in oceanography, maritime technology, and climate research
          </p>
        </motion.div>

        {/* Category Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="flex flex-wrap gap-3 mb-8 justify-center"
        >
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <button
                key={category.key}
                onClick={() => setSelectedCategory(category.key)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-300 ${
                  selectedCategory === category.key
                    ? 'bg-ocean-600 text-white border-ocean-500'
                    : 'bg-deep-800 text-gray-300 border-deep-700 hover:bg-deep-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                {category.label}
              </button>
            );
          })}
        </motion.div>

        {/* News Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredArticles.map((article, index) => (
            <motion.article
              key={article.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-deep-800 rounded-xl border border-deep-700 overflow-hidden hover:border-ocean-500/50 transition-all duration-300 group"
            >
              {/* Article Image */}
              <div className="aspect-video bg-gradient-to-br from-ocean-900 to-deep-900 flex items-center justify-center">
                <Waves className="w-12 h-12 text-ocean-400/50" />
              </div>

              <div className="p-6">
                {/* Category and Importance */}
                <div className="flex items-center justify-between mb-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getCategoryColor(article.category)}`}>
                    {article.category}
                  </span>
                  {getImportanceIcon(article.importance)}
                </div>

                {/* Title */}
                <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-ocean-400 transition-colors line-clamp-2">
                  {article.title}
                </h3>

                {/* Summary */}
                <p className="text-gray-400 text-sm mb-4 line-clamp-3">
                  {article.summary}
                </p>

                {/* Meta Info */}
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <div className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {formatDate(article.publishedAt)}
                  </div>
                  <div className="flex items-center gap-1">
                    <Globe className="w-3 h-3" />
                    {article.source}
                  </div>
                </div>

                {/* Read More Button */}
                {article.url && (
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 mt-4 text-ocean-400 hover:text-ocean-300 text-sm font-medium transition-colors"
                  >
                    Read Full Article
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </motion.article>
          ))}
        </div>

        {/* No Results */}
        {filteredArticles.length === 0 && (
          <div className="text-center py-12">
            <Globe className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">No articles found</h3>
            <p className="text-gray-400">Try selecting a different category</p>
          </div>
        )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default NewsPage;
