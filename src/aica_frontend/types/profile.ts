export interface EducationCreate {
  institution_name: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date?: string;
}

export interface ExperienceCreate {
  job_title: string;
  company_name: string;
  start_date: string;
  end_date?: string;
  description: string[];
}

export interface CertificateCreate {
  name: string;
  issuing_organization: string;
  issue_date?: string;
}

export interface ProfileUpdate {
  first_name?: string;
  last_name?: string;
  professional_title?: string;
  contact_number?: string;
  address?: string;
  linkedin_url?: string;
  summary?: string;
  educations?: EducationCreate[];
  experiences?: ExperienceCreate[];
  skills?: string[];
  certificates?: CertificateCreate[];
}

export interface Profile extends ProfileUpdate {
  id: number,
  user_id: number,
}