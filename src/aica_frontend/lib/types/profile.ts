export interface SkillCreate {
  name: string;
}

export interface EducationCreate {
  institution_name: string;
  degree: string;
  address: string;
  field_of_study?: string;
  start_date: string;
  end_date: string;
}

export interface ExperienceCreate {
  job_title: string;
  company_name: string;
  start_date: string;
  end_date?: string;
  description?: string[];
  is_current: boolean;
}

export interface CertificateCreate {
  name?: string;
  issuing_organization?: string;
  issue_date?: string;
  credential_url?: string;
  credential_id?: string;
}

export interface ProfileUpdate {
  first_name?: string;
  last_name?: string;
  professional_title?: string;
  contact_number?: string;
  address?: string;
  linkedin_url?: string;
  summary?: string;
  profile_picture?: string;
  educations?: EducationCreate[];
  experiences?: ExperienceCreate[];
  skills?: SkillCreate[];
  certificates?: CertificateCreate[];
}

export interface Profile extends ProfileUpdate {
  id: number;
  user_id: number;
  first_name: string;
  last_name: string;
  professional_title: string;
  contact_number: string;
  address: string;
  educations: EducationCreate[];
  experiences: ExperienceCreate[];
  skills: SkillCreate[];
}
