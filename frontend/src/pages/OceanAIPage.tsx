import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, MessageCircle, Send, Lightbulb, TrendingUp, AlertTriangle, Waves, Sparkles } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import Nav from '../components/Nav';
import Footer from '../components/Footer';
// ❌ removed GoogleGenAI import

interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  insights?: string[];
}

const OceanAIPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'ai',
      content: "Hello! I'm your Ocean AI assistant. I can help you analyze oceanographic data, understand float measurements, and provide insights about marine conditions. What would you like to explore today?",
      timestamp: new Date(),
      insights: [
        "Ask about temperature anomalies",
        "Analyze salinity patterns",
        "Compare float performance",
        "Predict oceanographic trends"
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const predefinedQuestions = [
    {
      icon: TrendingUp,
      title: "Ocean Temperature Trends",
      question: "What are the current temperature trends in the Indian Ocean?",
      color: "text-red-400"
    },
    {
      icon: Waves,
      title: "Salinity Analysis",
      question: "Analyze the salinity patterns from recent Argo float data",
      color: "text-blue-400"
    },
    {
      icon: AlertTriangle,
      title: "Anomaly Detection",
      question: "Are there any unusual oceanographic anomalies I should be aware of?",
      color: "text-yellow-400"
    },
    {
      icon: Lightbulb,
      title: "Data Insights",
      question: "What insights can you provide from the latest float measurements?",
      color: "text-green-400"
    }
  ];

  const mockAIResponses = [
    {
      keywords: ['temperature', 'trend', 'warm'],
      response: "Based on the latest Argo float data, I've observed some interesting temperature trends:\n\n• The Arabian Sea shows consistently higher temperatures (28-30°C) compared to the Bay of Bengal (26-28°C)\n• There's a noticeable thermocline at approximately 150-200m depth across all monitored regions\n• Surface temperatures have increased by 0.3°C over the past 6 months\n• The warmest readings are coming from float 1234567 near Mumbai coast",
      insights: ["Temperature stratification is strongest in coastal areas", "Monitor float 1234567 for continued warming trends", "Consider additional floats in thermocline zones"]
    },
    {
      keywords: ['salinity', 'salt', 'psu'],
      response: "Salinity analysis reveals fascinating patterns in the Indian Ocean:\n\n• Average salinity ranges from 34.1 PSU in the Bay of Bengal to 35.2 PSU in the Arabian Sea\n• Freshwater influence from river discharge is evident in coastal Bay of Bengal areas\n• Deep water salinity remains stable at ~34.7 PSU across all regions\n• Seasonal monsoon impacts are clearly visible in surface salinity variations",
      insights: ["River discharge significantly affects coastal salinity", "Deep water masses show remarkable stability", "Monsoon timing correlates with salinity drops"]
    },
    {
      keywords: ['anomaly', 'unusual', 'strange', 'abnormal'],
      response: "I've detected several noteworthy anomalies in the recent data:\n\n🔴 **High Priority**: Float 1234569 (Andaman Sea) showing temperature spike of 3°C above normal\n🟡 **Medium Priority**: Unusual salinity drop in southern Bay of Bengal region\n🟢 **Low Priority**: Minor depth measurement inconsistencies in 2 floats\n\n**Recommendations**: Immediate validation of Float 1234569 data and possible recalibration needed.",
      insights: ["Temperature spikes may indicate instrument drift", "Cross-validate with satellite data", "Consider emergency float deployment if trends continue"]
    },
    {
      keywords: ['insight', 'analysis', 'pattern'],
      response: "Here are key insights from the comprehensive data analysis:\n\n**Water Mass Characteristics:**\n• Clear distinction between Arabian Sea and Bay of Bengal water masses\n• Thermocline depth varies from 120m (coastal) to 180m (open ocean)\n• Mixing layer extends to 50-80m depending on location\n\n**Seasonal Patterns:**\n• Pre-monsoon warming evident in surface layers\n• Salinity stratification increasing in preparation for monsoon season\n\n**Float Performance:**\n• 98% data quality across all active floats\n• Average cycle completion rate: 85%\n• Recommended maintenance for floats older than 4 years",
      insights: ["Water mass boundaries are well-defined", "Seasonal cycles are highly predictable", "Float network coverage is optimal for current monitoring needs"]
    }
  ];

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const exactMatch = predefinedQuestions.find(q => 
        q.question.toLowerCase() === currentInput.toLowerCase()
      );

      if (exactMatch) {
        const matchedResponse = mockAIResponses.find(response => 
          response.keywords.some(keyword => currentInput.toLowerCase().includes(keyword))
        );
        
        if (matchedResponse) {
          setTimeout(() => {
            const aiResponse: ChatMessage = {
              id: (Date.now() + 1).toString(),
              type: 'ai',
              content: matchedResponse.response,
              timestamp: new Date(),
              insights: matchedResponse.insights
            };
            setMessages(prev => [...prev, aiResponse]);
            setIsLoading(false);
          }, 2000);
        } else {
          throw new Error('No mock response found, using Gemini');
        }
      } else {
        const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
        if (!apiKey || apiKey === 'your-gemini-api-key-here') {
          throw new Error('Gemini API key not configured');
        }

        const prompt = `You are an Ocean AI assistant specializing in oceanographic data analysis, Argo floats, and marine science.  

        When answering:
        - Be concise and factual
        - Start directly with the answer, no intro or filler
        - Use clear bullet points with values, patterns, or observations
        - Keep output short, structured, and focused only on the user’s question
        - If the question is unrelated to oceanography, briefly redirect to ocean topics

        User Question: ${currentInput}`;

        // ✅ direct fetch instead of SDK
        const response = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }]
            }),
          }
        );

        const data = await response.json();
        const text =
          data?.candidates?.[0]?.content?.parts?.[0]?.text ||
          "I'm sorry, I couldn't generate a response. Please try again.";

        const aiResponse: ChatMessage = {
          id: (Date.now() + 1).toString(),
          type: 'ai',
          content: text,
          timestamp: new Date(),
          insights: ["Response generated by Gemini AI", "Ask follow-up questions for more details", "I can help with specific oceanographic parameters"]
        };

        setMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Error with Gemini API:', error);
      
      const errorMessage = error instanceof Error ? error.message : String(error);
      
      const errorResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: `I apologize, but I encountered an error while processing your request.\n\nError Details:\n${errorMessage}\n\nPlease try asking about specific oceanographic topics like temperature trends, salinity patterns, or Argo float data.`,
        timestamp: new Date(),
        insights: ["Check if Gemini API key is configured correctly", "Try asking about ocean temperature or salinity", "Check your internet connection"]
      };

      setMessages(prev => [...prev, errorResponse]);
      setIsLoading(false);
    }
  };

  const handlePredefinedQuestion = (question: string) => {
    setInputMessage(question);
  };

  const formatContent = (content: string) => {
    return content.split('\n').map((line, index) => {
      if (line.startsWith('•')) {
        return (
          <li key={index} className="ml-4 text-gray-300">
            {line.substring(1).trim()}
          </li>
        );
      }
      if (line.startsWith('**') && line.endsWith('**')) {
        return (
          <h4 key={index} className="font-semibold text-ocean-400 mt-3 mb-1">
            {line.replace(/\*\*/g, '')}
          </h4>
        );
      }
      if (line.includes('🔴') || line.includes('🟡') || line.includes('🟢')) {
        return (
          <div key={index} className="bg-deep-700 p-2 rounded-lg mt-2 text-sm">
            {line}
          </div>
        );
      }
      if (line.trim()) {
        return (
          <p key={index} className="text-gray-300 mb-2">
            {line}
          </p>
        );
      }
      return <br key={index} />;
    });
  };

  return (
    <div className="min-h-screen bg-deep-950">
      <Nav />
      <div className="pt-20">
      {/* Header */}
      <div className="bg-deep-900 border-b border-deep-700">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white">Ocean AI Assistant</h1>
              <Sparkles className="w-6 h-6 text-yellow-400" />
            </div>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Powered by advanced AI, I can help you analyze oceanographic data, detect patterns, 
              and provide insights from Argo float measurements. Ask me anything about ocean science!
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Predefined Questions */}
          <div className="lg:col-span-1">
            <div className="bg-deep-800 rounded-xl border border-deep-700 p-6 sticky top-24">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-400" />
                Quick Questions
              </h3>
              
              <div className="space-y-3">
                {predefinedQuestions.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={index}
                      onClick={() => handlePredefinedQuestion(item.question)}
                      className="w-full p-3 text-left bg-deep-700 hover:bg-deep-600 rounded-lg border border-deep-600 hover:border-deep-500 transition-all duration-300 group"
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <Icon className={`w-4 h-4 ${item.color}`} />
                        <span className="text-sm font-medium text-white group-hover:text-ocean-400">
                          {item.title}
                        </span>
                      </div>
                      <p className="text-xs text-gray-400 line-clamp-2">
                        {item.question}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <div className="bg-deep-800 rounded-xl border border-deep-700 h-[70vh] flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex gap-4 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {message.type === 'ai' && (
                      <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                    )}
                    
                    <div className={`max-w-3xl ${message.type === 'user' ? 'bg-ocean-600' : 'bg-deep-700'} rounded-lg p-4`}>
                      <div className="prose prose-invert max-w-none">
                        {typeof message.content === 'string' ? formatContent(message.content) : message.content}
                      </div>
                      
                      {message.insights && (
                        <div className="mt-4 p-3 bg-deep-600 rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <Lightbulb className="w-4 h-4 text-yellow-400" />
                            <span className="text-sm font-medium text-yellow-400">AI Insights</span>
                          </div>
                          <ul className="text-xs text-gray-300 space-y-1">
                            {message.insights.map((insight, index) => (
                              <li key={index}>• {insight}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="text-xs text-gray-500 mt-2">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>

                    {message.type === 'user' && (
                      <div className="w-8 h-8 bg-ocean-600 rounded-full flex items-center justify-center flex-shrink-0">
                        <MessageCircle className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </motion.div>
                ))}

                {isLoading && (
                  <div className="flex gap-4">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-deep-700 rounded-lg p-4">
                      <LoadingSpinner />
                      <p className="text-gray-400 text-sm mt-2">Analyzing oceanographic data...</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="border-t border-deep-700 p-6">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Ask about ocean data, patterns, or analysis..."
                    className="flex-1 px-4 py-3 bg-deep-700 text-white rounded-lg border border-deep-600 focus:border-ocean-500 focus:outline-none"
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={isLoading || !inputMessage.trim()}
                    className="px-6 py-3 bg-ocean-600 hover:bg-ocean-700 disabled:bg-deep-600 text-white rounded-lg transition-colors flex items-center gap-2"
                  >
                    <Send className="w-4 h-4" />
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      <Footer />
    </div>
  );
};

export default OceanAIPage;
