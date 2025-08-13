import { ApiError } from '@/lib/types/api';

export class ApiErrorHandler {
  static parseErrorMessage(errorData: ApiError): string {
    if (typeof errorData.detail === 'string') {
      return errorData.detail;
    }

    if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
      const firstError = errorData.detail[0];
      if (firstError?.msg) {
        const field = firstError.loc?.join('.') || 'unknown field';
        return `${firstError.msg} (${field})`;
      }
    }

    if (typeof errorData.message === 'string') {
      return errorData.message;
    }

    return 'An unexpected error occurred';
  }

  static createHttpError(
    status: number,
    errorData: ApiError,
    endpoint?: string,
  ): Error {
    const errorMessage = this.parseErrorMessage(errorData);

    if (status === 401) {
      if (endpoint && endpoint.includes('/login/access-token')) {
        return new Error(errorMessage || 'Invalid email or password');
      }
      return new Error('Session expired. Please login again.');
    }

    // Handle common HTTP errors with user-friendly messages
    switch (status) {
      case 403:
        return new Error('Access denied. Insufficient permissions.');
      case 404:
        return new Error('Resource not found.');
      case 422:
        return new Error(`Validation error: ${errorMessage}`);
      case 429:
        return new Error('Too many requests. Please try again later.');
      case 500:
        return new Error('Server error. Please try again later.');
      default:
        return new Error(errorMessage || `HTTP error! status: ${status}`);
    }
  }

  static handleUnknownError(error: unknown): Error {
    if (error instanceof Error) {
      return error;
    }

    if (typeof error === 'string') {
      return new Error(error);
    }

    return new Error('An unexpected error occurred');
  }
}

// HTTP Status constants for the most commonly used ones (YAGNI principle)
export const HTTP_STATUS = {
  OK: 200,
  NO_CONTENT: 204,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const;
