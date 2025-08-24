import { HttpClient } from './http-client';
import {
  LoginCredentials,
  RegisterData,
  AuthResponse,
  User,
} from '../types/api';
import { ProfileUpdate, Profile } from '../types/profile';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private http: HttpClient;

  constructor() {
    this.http = new HttpClient(`${API_BASE_URL}/api/v1`);
  }

  auth = {
    login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
      const formData = new FormData();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);

      return this.http.postForm<AuthResponse>('/login/access-token', formData);
    },

    register: async (data: RegisterData): Promise<AuthResponse> => {
      return this.http.post<AuthResponse>('/users/', data, false);
    },

    logout: async (): Promise<{ message: string }> => {
      return this.http.post<{ message: string }>('/logout');
    },

    refresh: async (): Promise<AuthResponse> => {
      return this.http.post<AuthResponse>('/refresh');
    },

    verify: async (): Promise<{ valid: boolean; user: User }> => {
      return this.http.get<{ valid: boolean; user: User }>('/verify');
    },

    getCurrentUser: async (): Promise<User> => {
      return this.http.get<User>('/users/me');
    },
  };

  profile = {
    get: async (): Promise<Profile> => {
      return this.http.get<Profile>('/profile');
    },

    update: async (data: ProfileUpdate): Promise<Profile> => {
      return this.http.put<Profile>('/profile', data);
    },
  };
}

export const apiClient = new ApiClient();
