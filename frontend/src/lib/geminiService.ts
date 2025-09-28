import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY || '');

export interface GeminiResponse {
  text: string;
  searchResults?: string[];
}

export class GeminiService {
  private model;

  constructor() {
    const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
    if (!apiKey || apiKey === 'your_gemini_api_key_here') {
      throw new Error('Gemini API key not configured');
    }
    this.model = genAI.getGenerativeModel({ model: 'gemini-pro' });
  }

  async generateResponse(query: string): Promise<GeminiResponse> {
    try {
      // Short, focused system prompt for oceanography
      const systemPrompt = `Oceanography expert. Answer about ocean/Argo data, temperature, salinity, marine science. Max 120 words. Be precise.`;
      
      const fullPrompt = `${systemPrompt}\n\nQ: ${query}`;
      
      const result = await this.model.generateContent(fullPrompt);
      const response = await result.response;
      const text = response.text();

      if (!text) {
        throw new Error('Empty response from Gemini');
      }

      return {
        text: text.trim()
      };
    } catch (error: any) {
      console.error('Gemini API error:', error);
      
      if (error.message?.includes('API_KEY')) {
        throw new Error('Invalid Gemini API key. Please check your configuration.');
      }
      if (error.message?.includes('quota')) {
        throw new Error('Gemini API quota exceeded. Please try again later.');
      }
      
      throw new Error('AI service temporarily unavailable. Please try again.');
    }
  }

  async searchAndAnalyze(query: string): Promise<GeminiResponse> {
    try {
      // Enhanced prompt for web search simulation
      const searchPrompt = `Oceanography expert with current research access. Analyze: "${query}". Include recent findings, trends, 2-3 key sources (NOAA, NASA, Copernicus, etc). Max 150 words. Be specific.`;

      const result = await this.model.generateContent(searchPrompt);
      const response = await result.response;
      const text = response.text();

      if (!text) {
        throw new Error('Empty search response from Gemini');
      }

      // Extract potential sources mentioned in response
      const searchResults = this.extractSources(text);

      return {
        text: text.trim(),
        searchResults
      };
    } catch (error: any) {
      console.error('Gemini search error:', error);
      
      if (error.message?.includes('API_KEY')) {
        throw new Error('Invalid Gemini API key for search.');
      }
      if (error.message?.includes('quota')) {
        throw new Error('Search quota exceeded. Please try again later.');
      }
      
      throw new Error('Search service temporarily unavailable.');
    }
  }

  private extractSources(text: string): string[] {
    // Simple extraction of potential sources/databases mentioned
    const sources: string[] = [];
    const patterns = [
      /NOAA/gi,
      /NASA/gi,
      /Copernicus/gi,
      /Argo.*database/gi,
      /Ocean.*observatory/gi,
      /GODAE/gi,
      /World Ocean Database/gi,
      /Global Temperature Anomaly/gi
    ];

    patterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) {
        sources.push(...matches);
      }
    });

    return [...new Set(sources.slice(0, 3))]; // Remove duplicates, max 3
  }
}

// Create service instance with error handling
let geminiService: GeminiService | null = null;

try {
  geminiService = new GeminiService();
} catch (error) {
  console.warn('Gemini service not available:', error);
  geminiService = null;
}

export { geminiService };
