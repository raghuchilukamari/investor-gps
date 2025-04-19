const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface HealthStatus {
  status: string;
  timestamp: string;
}

export const api = {
  // Health check
  async getHealth(): Promise<HealthStatus> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Failed to fetch health status');
    }
    return response.json();
  },

  // Welcome message
  async getWelcome() {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) {
      throw new Error('Failed to fetch welcome message');
    }
    return response.json();
  }
}; 