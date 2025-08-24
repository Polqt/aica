export interface ApiError {
  detail?: string;
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
  name?: string;
  created_at: string;
}
