export class TokenManager {
  private static readonly TOKEN_KEY = 'access_token';

  static getAccessToken(): string | null {
    if (typeof window === 'undefined') return null;

    try {
      return localStorage.getItem(this.TOKEN_KEY);
    } catch (error) {
      console.warn('Failed to retrieve access token:', error);
      return null;
    }
  }

  static setAccessToken(token: string): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.setItem(this.TOKEN_KEY, token);
    } catch (error) {
      console.warn('Failed to store access token:', error);
    }
  }

  static clearTokens(): void {
    if (typeof window === 'undefined') return;

    try {
      localStorage.removeItem(this.TOKEN_KEY);
    } catch (error) {
      console.warn('Failed to clear tokens:', error);
    }
  }

  static hasValidToken(): boolean {
    const token = this.getAccessToken();
    return Boolean(token && token.trim().length > 0);
  }

  static formatAuthHeader(token?: string): string | null {
    const accessToken = token || this.getAccessToken();
    if (!accessToken) return null;

    return accessToken.startsWith('Bearer ')
      ? accessToken
      : `Bearer ${accessToken}`;
  }
}
