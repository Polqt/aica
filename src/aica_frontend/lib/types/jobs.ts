export interface Job {
  id: number;
  job_title: string;
  company_name: string;
  source_url: string;
  source_site: string;
}

export interface MatchedJobsResponse {
  matches: Job[];
}

export interface JobMatchingState {
  jobs: Job[];
  isLoading: boolean;
  error: string | null;
  lastFetched: Date | null;
}
