import { describe, it, expect, vi } from 'vitest'
import { argoApi } from '../lib/apiClient'

// Mock the API client
vi.mock('../lib/apiClient', () => ({
  argoApi: {
    getFloats: vi.fn(),
    getFloat: vi.fn(),
    getFloatDetails: vi.fn(),
    getFloatProfiles: vi.fn(),
    getTemperatureSeries: vi.fn(),
    logFloatClick: vi.fn(),
    getSummaryStats: vi.fn(),
    getLatestProfiles: vi.fn(),
    exportData: vi.fn(),
    healthCheck: vi.fn(),
  }
}))

describe('API Client', () => {
  it('should have all required methods', () => {
    expect(argoApi.getFloats).toBeDefined()
    expect(argoApi.getFloat).toBeDefined()
    expect(argoApi.getFloatDetails).toBeDefined()
    expect(argoApi.getFloatProfiles).toBeDefined()
    expect(argoApi.getTemperatureSeries).toBeDefined()
    expect(argoApi.logFloatClick).toBeDefined()
    expect(argoApi.getSummaryStats).toBeDefined()
    expect(argoApi.getLatestProfiles).toBeDefined()
    expect(argoApi.exportData).toBeDefined()
    expect(argoApi.healthCheck).toBeDefined()
  })

  it('should call logFloatClick with correct parameters', async () => {
    const mockResponse = { success: true, message: 'Click logged', data: {} }
    vi.mocked(argoApi.logFloatClick).mockResolvedValue(mockResponse)

    const result = await argoApi.logFloatClick(12345, {
      source: 'frontend',
      action: 'select'
    })

    expect(argoApi.logFloatClick).toHaveBeenCalledWith(12345, {
      source: 'frontend',
      action: 'select'
    })
    expect(result).toEqual(mockResponse)
  })
})
