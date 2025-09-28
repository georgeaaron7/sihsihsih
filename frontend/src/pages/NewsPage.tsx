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
    setError(null);

    const API_KEY = 'f59e5da706a54cbe860ad58c679bbbae';
    const query = 'ocean OR maritime OR climate OR research OR technology';
    const pageSize = 50;
    const url = `https://newsapi.org/v2/everything?q=${encodeURIComponent(query)}&language=en&pageSize=${pageSize}&apiKey=${API_KEY}`;

    const response = await fetch(url);
    const data = await response.json();

    if (data.status !== 'ok') {
      throw new Error(data.message || 'Failed to fetch news');
    }

    // Transform NewsAPI articles to your NewsArticle type
    const transformedArticles: NewsArticle[] = data.articles.map((article: any, index: number) => ({
  id: index.toString(),
  title: article.title,
  summary: article.description || '',
  content: article.content || '',
  source: article.source.name || 'Unknown',
  publishedAt: article.publishedAt,
  category: article.title.toLowerCase().includes('maritime') ? 'maritime'
               : article.title.toLowerCase().includes('ocean') ? 'oceanography'
               : article.title.toLowerCase().includes('climate') ? 'climate'
               : article.title.toLowerCase().includes('research') ? 'research'
               : 'technology',
  importance: 'medium',
  imageUrl: article.urlToImage,  // <-- here
  url: article.url,
}))

    setArticles(transformedArticles);
    setLoading(false);
  } catch (err: any) {
    setError(err.message);
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
            <div className="aspect-video bg-gray-800 flex items-center justify-center overflow-hidden">
              {article.imageUrl ? (
                <img
                  src={article.imageUrl}
                  alt={article.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <Waves className="w-12 h-12 text-ocean-400/50" />
              )}
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
