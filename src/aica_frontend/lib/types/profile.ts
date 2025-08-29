export interface SkillCreate {
  name: string;
}

export interface Skill extends SkillCreate {
  id: number;
}

export interface EducationCreate {
  institution_name: string;
  degree: string;
  address: string;
  field_of_study?: string;
  start_date: string;
  end_date: string;
  description?: string;
}

export interface Education extends EducationCreate {
  id: number;
  profile_id: number;
}

export interface ExperienceCreate {
  job_title: string;
  company_name: string;
  start_date: string;
  end_date?: string;
  description?: string[];
  is_current: boolean;
}

export interface Experience extends ExperienceCreate {
  id: number;
  profile_id: number;
}

export interface CertificateCreate {
  name?: string;
  issuing_organization?: string;
  issue_date?: string;
  credential_url?: string;
  credential_id?: string;
}

export interface Certificate extends CertificateCreate {
  id: number;
  profile_id: number;
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

export interface Profile {
  id: number;
  user_id: number;
  first_name: string;
  last_name: string;
  professional_title: string;
  contact_number: string;
  address: string;
  linkedin_url?: string;
  summary?: string;
  profile_picture?: string;
  created_at: string;
  updated_at: string;
  educations: Education[];
  experiences: Experience[];
  skills: Skill[];
  certificates: Certificate[];
}

export interface ProfileFlags {
  has_experiences: boolean;
  has_certificates: boolean;
}
