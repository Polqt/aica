import { HttpClient } from './http-client';
import { AuthResponse, LoginCredentials, RegisterData } from '@/lib/types/api';
import { TokenManager } from '@/lib/utils/token-manager';

export class AuthService {
  constructor(private httpClient: HttpClient) {}

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const params = new URLSearchParams();
    params.append('username', credentials.email);
    params.append('password', credentials.password);

    const response = await this.httpClient.post<AuthResponse>(
      '/api/v1/login/access-token',
      params.toString(),
      {
        includeAuth: false,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      },
    );

    TokenManager.setAccessToken(response.access_token);

    return response;
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    const response = await this.httpClient.post<AuthResponse>(
      '/api/v1/users/',
      userData,
      { includeAuth: false },
    );

    TokenManager.setAccessToken(response.access_token);

    return response;
  }

  async logout(): Promise<void> {
    try {
      if (TokenManager.hasValidToken()) {
        await this.httpClient.post('/api/v1/logout', {}, { includeAuth: true });
      }
    } catch {
    } finally {
      TokenManager.clearTokens();
    }
  }

  isAuthenticated(): boolean {
    return TokenManager.hasValidToken();
  }
}
