import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API Response wrapper type
export interface APIResponse<T = unknown> {
  success: boolean;
  message: string;
  data: T;
}

// Float data types
export interface FloatInfo {
  PLATFORM_NUMBER: number;
  LATITUDE: number;
  LONGITUDE: number;
  LAST_DATE: string;
  MAX_CYCLE: number;
  MAX_DEPTH: number;
  AVG_TEMP: number;
  AVG_SALINITY: number;
  LOCATION: string;
}

export interface ProfileData {
  PLATFORM_NUMBER: number;
  CYCLE_NUMBER: number;
  JULD: string;
  LATITUDE: number;
  LONGITUDE: number;
  PRES: number;
  TEMP: number;
  PSAL: number;
}

export interface FloatDetails {
  float_info: FloatInfo;
  profile_count: number;
  profiles: ProfileData[];
}

export interface TemperatureSeries {
  date: string;
  cycle: number;
  temperature: number;
  depth: number;
}

export interface SummaryStats {
  total_floats: number;
  avg_temp: number;
  avg_salinity: number;
  max_depth: number;
  date_range: {
    start: string;
    end: string;
  };
}

export interface LatestProfile {
  platform_number: number;
  cycle: number;
  date: string;
  latitude: number;
  longitude: number;
  temperature: number;
  salinity: number;
  pressure: number;
}

export interface ClickPayload {
  source: string;
  action: string;
}

// Create axios instance with base configuration
const createApiClient = (): AxiosInstance => {
  const baseURL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8061';
  
  const client = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor for logging
  client.interceptors.request.use(
    (config) => {
      console.log(`🌊 API Request: ${config.method?.toUpperCase()} ${config.url}`);
      return config;
    },
    (error) => {
      console.error('❌ API Request Error:', error);
      return Promise.reject(error);
    }
  );

  // Response interceptor for logging and error handling
  client.interceptors.response.use(
    (response: AxiosResponse<APIResponse>) => {
      console.log(`✅ API Response: ${response.status} ${response.config.url}`);
      return response;
    },
    (error) => {
      console.error('❌ API Response Error:', error.response?.data || error.message);
      return Promise.reject(error);
    }
  );

  return client;
};

export const apiClient = createApiClient();

// Utility function to safely extract data from API response
export const extractApiData = <T>(response: AxiosResponse<APIResponse<T>>): T => {
  if (response.data && typeof response.data === 'object' && 'data' in response.data) {
    return response.data.data;
  }
  // Fallback for responses that don't use the wrapper
  return response.data as unknown as T;
};

// API client class with typed methods
export class ArgoApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = apiClient;
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string; service: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Get all floats with optional filters
  async getFloats(params?: {
    region?: string;
    min_temp?: number;
    max_temp?: number;
  }): Promise<FloatInfo[]> {
    const response = await this.client.get<APIResponse<FloatInfo[]>>('/floats', { params });
    return extractApiData(response);
  }

  // Get specific float
  async getFloat(platformNumber: number): Promise<FloatInfo> {
    const response = await this.client.get<APIResponse<FloatInfo>>(`/floats/${platformNumber}`);
    return extractApiData(response);
  }

  // Get float details
  async getFloatDetails(platformNumber: number): Promise<FloatDetails> {
    const response = await this.client.get<APIResponse<FloatDetails>>(`/floats/${platformNumber}/details`);
    return extractApiData(response);
  }

  // Get float profiles
  async getFloatProfiles(
    platformNumber: number,
    params?: { cycle?: number; latest?: boolean }
  ): Promise<ProfileData[]> {
    const response = await this.client.get<APIResponse<ProfileData[]>>(
      `/floats/${platformNumber}/profiles`,
      { params }
    );
    return extractApiData(response);
  }

  // Get temperature series
  async getTemperatureSeries(platformNumber: number): Promise<TemperatureSeries[]> {
    const response = await this.client.get<APIResponse<TemperatureSeries[]>>(
      `/floats/${platformNumber}/temperature-series`
    );
    return extractApiData(response);
  }

  // Log float click
  async logFloatClick(platformNumber: number, payload: ClickPayload): Promise<unknown> {
    const response = await this.client.post<APIResponse>(
      `/floats/${platformNumber}/click`,
      payload
    );
    return extractApiData(response);
  }

  // Get summary stats
  async getSummaryStats(): Promise<SummaryStats> {
    const response = await this.client.get<APIResponse<SummaryStats>>('/stats');
    return extractApiData(response);
  }

  // Get latest profiles
  async getLatestProfiles(): Promise<LatestProfile[]> {
    const response = await this.client.get<APIResponse<LatestProfile[]>>('/profiles/latest');
    return extractApiData(response);
  }

  // Export data
  async exportData(format: 'json' | 'csv', params?: {
    platform_number?: number;
    data_type?: 'float_info' | 'profiles';
  }): Promise<unknown> {
    const response = await this.client.get(`/export/${format}`, { params });
    return response.data;
  }
}

// Export singleton instance
export const argoApi = new ArgoApiClient();
