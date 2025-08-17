export interface ApiError {
  detail?: string | Array<{ msg: string; loc?: string[] }>;
  message?: string;
}

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

export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface RequestConfig extends RequestInit {
  timeout?: number;
  includeAuth?: boolean;
}

export interface HttpClientConfig {
  baseURL: string;
  timeout?: number;
}
