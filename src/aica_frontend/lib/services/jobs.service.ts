import { HttpClient } from './http-client';
import { MatchedJobsResponse } from '@/lib/types/jobs';

export class JobsService {
  constructor(private httpClient: HttpClient) {}

  async getJobRecommendations(params?: {
    limit?: number;
    threshold?: number;
  }): Promise<MatchedJobsResponse> {
    const searchParams = new URLSearchParams();

    if (params?.limit) {
      searchParams.append('limit', params.limit.toString());
    }

    if (params?.threshold) {
      searchParams.append('threshold', params.threshold.toString());
    }

    const queryString = searchParams.toString();
    const endpoint = `/api/v1/matching/profile-to-jobs${
      queryString ? `?${queryString}` : ''
    }`;

    return this.httpClient.get<MatchedJobsResponse>(endpoint);
  }

  async getJobById(jobId: number) {
    return this.httpClient.get(`/api/v1/jobs/${jobId}`);
  }

  async searchJobs(filters?: {
    skip?: number;
    limit?: number;
    location?: string;
    work_type?: string;
    employment_type?: string;
    experience_level?: string;
    salary_min?: number;
    salary_max?: number;
  }) {
    const searchParams = new URLSearchParams();

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, value.toString());
        }
      });
    }

    const queryString = searchParams.toString();
    const endpoint = `/api/v1/jobs${queryString ? `?${queryString}` : ''}`;

    return this.httpClient.get(endpoint);
  }

  async getSimilarJobs(jobId: number, limit = 10) {
    return this.httpClient.get(
      `/api/v1/matching/jobs/${jobId}/similar?limit=${limit}`,
    );
  }

  async analyzeJobMatch(jobId: number) {
    return this.httpClient.get(`/api/v1/matching/jobs/${jobId}/match-analysis`);
  }
}
