export class HttpClient {
  private baseURL: string;
  private timeout: number;

  constructor(baseURL: string, timeout: number = 15000) {
    this.baseURL = baseURL.replace(/\/+$/, '');
    this.timeout = timeout;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    includeAuth: boolean = true,
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (includeAuth) {
      const token = this.getTokenFromCookie();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
        credentials: 'include',
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const contentType = response.headers.get('content-type') || '';
        if (contentType.includes('application/json')) {
          const errorData = await response.json().catch(() => ({} as unknown));
          const msg =
            (errorData.detail &&
              (Array.isArray(errorData.detail)
                ? errorData.detail[0]?.msg
                : errorData.detail)) ||
            errorData.message ||
            errorData.error ||
            `HTTP ${response.status}`;
          throw new Error(typeof msg === 'string' ? msg : 'Request failed');
        } else {
          const text = await response.text().catch(() => '');
          throw new Error(text || `HTTP ${response.status}`);
        }
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error or request timed out');
    }
  }

  private getTokenFromCookie(): string | null {
    if (typeof document === 'undefined') return null;

    // Prioritize localStorage as it's explicitly set by AuthContext on login.
    // This addresses potential timing issues where cookies might not be immediately available or updated.
    try {
      const lsToken = localStorage.getItem('access_token');
      if (lsToken) {
        return lsToken;
      }
    } catch {
      // If localStorage is not accessible, proceed to check cookies.
    }

    const cookieToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('access_token='))
      ?.split('=')[1];

    if (cookieToken && cookieToken.startsWith('Bearer ')) {
      return cookieToken.substring(7);
    }
    return null;
  }

  async get<T>(endpoint: string, includeAuth = true): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' }, includeAuth);
  }

  async post<T>(
    endpoint: string,
    data?: unknown,
    includeAuth = true,
  ): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
      },
      includeAuth,
    );
  }

  async put<T>(
    endpoint: string,
    data?: unknown,
    includeAuth = true,
  ): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'PUT',
        body: data ? JSON.stringify(data) : undefined,
      },
      includeAuth,
    );
  }
  async delete<T>(endpoint: string, includeAuth = true): Promise<T> {
    return this.request<T>(
      endpoint,
      {
        method: 'DELETE',
      },
      includeAuth,
    );
  }

  // Form data for login (meet the backend expectations)
  async postForm<T>(
    endpoint: string,
    formData: FormData,
    includeAuth = false,
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const headers: HeadersInit = {};
    if (includeAuth) {
      const token = this.getTokenFromCookie();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || 'An unknown error occurred.';
      throw new Error(errorMessage);
    }

    return await response.json();
  }
}
