import { HttpClient } from './http-client';
import { AuthService } from './auth.service';
import { ProfileService } from './profile.service';
import { JobsService } from './jobs.service';

export class ApiClient {
  private httpClient: HttpClient;

  public readonly auth: AuthService;
  public readonly profile: ProfileService;
  public readonly jobs: JobsService;

  constructor(baseURL?: string) {
    this.httpClient = new HttpClient({
      baseURL:
        baseURL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
    });

    this.auth = new AuthService(this.httpClient);
    this.profile = new ProfileService(this.httpClient);
    this.jobs = new JobsService(this.httpClient);
  }
  getHttpClient(): HttpClient {
    return this.httpClient;
  }
}

export const apiClient = new ApiClient();
