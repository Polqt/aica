import { TokenManager } from './utils/token-manager';
import { HttpClient } from './services/http-client';

// Import centralized services
import { apiClient } from './services/api-client';
import { AuthService } from './services/auth.service';
import { ProfileService } from './services/profile.service';
import { JobsService } from './services/jobs.service';

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export { apiClient };

export { AuthService, ProfileService, JobsService };

export { TokenManager, HttpClient };

interface ApiError {
  detail?: string | Array<{ msg: string; loc?: string[] }>;
  message?: string;
}

export class ApiErrorUtils {
  static parseErrorMessage(errorData: ApiError): string {
    if (typeof errorData.detail === 'string') {
      return errorData.detail;
    }

    if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
      const firstError = errorData.detail[0];
      if (firstError?.msg) {
        const field = firstError.loc?.join('.') || 'unknown';
        return `${firstError.msg} (field: ${field})`;
      }
    }

    if (typeof errorData.message === 'string') {
      return errorData.message;
    }

    return 'An unexpected error occurred';
  }

  static createHttpError(response: Response, errorData: ApiError): Error {
    const errorMessage = this.parseErrorMessage(errorData);

    switch (response.status) {
      case 401:
        return new Error('Session expired. Please login again.');
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
        return new Error(
          errorMessage || `HTTP error! status: ${response.status}`,
        );
    }
  }
}
