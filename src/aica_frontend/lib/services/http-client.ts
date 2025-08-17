import { RequestConfig, HttpClientConfig } from '@/lib/types/api';
import { TokenManager } from '@/lib/utils/token-manager';
import { ApiErrorHandler, HTTP_STATUS } from '@/lib/utils/error-handler';

export class HttpClient {
  private readonly baseURL: string;
  private readonly defaultTimeout: number;

  constructor(config: HttpClientConfig) {
    this.baseURL = config.baseURL;
    this.defaultTimeout = config.timeout || 30000;
  }

  async request<T>(endpoint: string, config: RequestConfig = {}): Promise<T> {
    const {
      timeout = this.defaultTimeout,
      includeAuth = true,
      ...requestOptions
    } = config;

    const url = this.buildUrl(endpoint);
    const headers = this.buildHeaders(requestOptions.headers, includeAuth);

    if (requestOptions.body instanceof FormData) {
      delete (headers as Record<string, string>)['Content-Type'];
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...requestOptions,
        headers,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        await this.handleErrorResponse(response, endpoint);
      }

      return await this.parseResponse<T>(response);
    } catch (error) {
      console.error('HttpClient Error:', error);
      throw ApiErrorHandler.handleUnknownError(error);
    }
  }

  async get<T>(endpoint: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'GET' });
  }

  async post<T>(
    endpoint: string,
    data?: unknown,
    config?: RequestConfig,
  ): Promise<T> {
    const serializedBody = this.serializeBody(data, config?.headers);

    return this.request<T>(endpoint, {
      ...config,
      method: 'POST',
      body: serializedBody,
    });
  }

  async put<T>(
    endpoint: string,
    data?: unknown,
    config?: RequestConfig,
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: 'PUT',
      body: this.serializeBody(data, config?.headers),
    });
  }

  async delete<T>(endpoint: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: 'DELETE' });
  }

  private buildUrl(endpoint: string): string {
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${this.baseURL}${cleanEndpoint}`;
  }

  private buildHeaders(
    customHeaders?: HeadersInit,
    includeAuth = true,
  ): HeadersInit {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };

    if (includeAuth) {
      const authHeader = TokenManager.formatAuthHeader();
      if (authHeader) {
        headers['Authorization'] = authHeader;
      }
    }

    if (customHeaders) {
      if (customHeaders instanceof Headers) {
        customHeaders.forEach((value, key) => {
          headers[key] = value;
        });
      } else if (Array.isArray(customHeaders)) {
        customHeaders.forEach(([key, value]) => {
          headers[key] = value;
        });
      } else {
        Object.assign(headers, customHeaders);
      }
    }

    return headers;
  }

  private serializeBody(
    data: unknown,
    headers?: HeadersInit,
  ): string | FormData | URLSearchParams | undefined {
    if (!data) return undefined;

    if (data instanceof FormData || data instanceof URLSearchParams) {
      return data;
    }

    if (typeof data === 'string') {
      return data;
    }

    const contentType = this.getContentType(headers);
    if (contentType?.includes('application/json')) {
      return JSON.stringify(data);
    }

    return JSON.stringify(data);
  }

  private getContentType(headers?: HeadersInit): string | undefined {
    if (!headers) return undefined;

    if (headers instanceof Headers) {
      return headers.get('Content-Type') || undefined;
    }

    if (Array.isArray(headers)) {
      const contentTypeHeader = headers.find(
        ([key]) => key.toLowerCase() === 'content-type',
      );
      return contentTypeHeader?.[1];
    }

    return (
      (headers as Record<string, string>)['Content-Type'] ||
      (headers as Record<string, string>)['content-type']
    );
  }

  private async parseResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('Content-Type');

    if (contentType?.includes('application/json')) {
      return response.json();
    }

    if (response.status === HTTP_STATUS.NO_CONTENT) {
      return {} as T;
    }

    const text = await response.text();
    try {
      return JSON.parse(text);
    } catch {
      return text as unknown as T;
    }
  }

  private async handleErrorResponse(
    response: Response,
    endpoint?: string,
  ): Promise<never> {
    let errorData;

    try {
      errorData = await response.json();
    } catch {
      errorData = { message: response.statusText };
    }

    throw ApiErrorHandler.createHttpError(response.status, errorData, endpoint);
  }
}
