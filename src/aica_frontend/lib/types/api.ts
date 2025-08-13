// Core API Types
export interface ApiError {
  detail?: string | Array<{ msg: string; loc?: string[] }>;
  message?: string;
}

// Authentication Types
export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in?: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

// User Types
export interface User {
  id: number;
  email: string;
  created_at: string;
}

// HTTP Client Configuration (simplified)
export interface RequestConfig extends RequestInit {
  timeout?: number;
  includeAuth?: boolean;
}

export interface HttpClientConfig {
  baseURL: string;
  timeout?: number;
}
