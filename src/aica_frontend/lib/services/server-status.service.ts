import { API_BASE_URL } from '../api';

export interface ServerStatus {
  status: string;
  environment: string;
  timestamp: string;
  version?: string;
  database_status: string;
  ai_services_status: {
    matching_service: string;
    rag_service: string;
  };
}

export class ServerStatusService {
  private static baseUrl = API_BASE_URL;

  static async getServerStatus(): Promise<ServerStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch server status:', error);
      throw error;
    }
  }

  static async getAISystemStatus(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/ai/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch AI system status:', error);
      throw error;
    }
  }

  static async getPipelineStatus(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/pipeline/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch pipeline status:', error);
      throw error;
    }
  }
}
