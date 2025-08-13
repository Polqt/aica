import { z } from 'zod';

export const commonValidations = {
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address')
    .max(254, 'Email is too long'),

  password: z
    .string()
    .min(8, 'Password must be at least 8 characters long')
    .max(128, 'Password is too long')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(
      /[!@#$%^&*(),.?":{}|<>]/,
      'Password must contain at least one special character',
    ),

  confirmPassword: z.string().min(1, 'Please confirm your password'),

  firstName: z
    .string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters')
    .regex(
      /^[A-Za-z\s\-']+$/,
      'First name should only contain letters, spaces, hyphens, and apostrophes',
    ),

  lastName: z
    .string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters')
    .regex(
      /^[A-Za-z\s\-']+$/,
      'Last name should only contain letters, spaces, hyphens, and apostrophes',
    ),

  phoneNumber: z
    .string()
    .min(7, 'Invalid contact number')
    .max(20, 'Contact number is too long')
    .regex(/^[\+\d\s\-\(\)]+$/, 'Please enter a valid phone number'),

  url: z.string().url('Please enter a valid URL').optional().or(z.literal('')),

  requiredString: (fieldName: string, minLength = 1, maxLength = 100) =>
    z
      .string()
      .min(minLength, `${fieldName} is required`)
      .max(maxLength, `${fieldName} must be less than ${maxLength} characters`),

  optionalString: (maxLength = 100) =>
    z
      .string()
      .max(maxLength, `Must be less than ${maxLength} characters`)
      .optional(),

  dateString: z
    .string()
    .min(1, 'Date is required')
    .regex(
      /^\d{4}-\d{2}-\d{2}$/,
      'Please enter a valid date in YYYY-MM-DD format',
    ),

  optionalDateString: z
    .string()
    .regex(
      /^\d{4}-\d{2}-\d{2}$/,
      'Please enter a valid date in YYYY-MM-DD format',
    )
    .optional()
    .or(z.literal('')),
};

// Authentication schemas
export const loginSchema = z.object({
  email: commonValidations.email,
  password: z.string().min(1, 'Password is required'),
});

export const registerSchema = z
  .object({
    email: commonValidations.email,
    password: commonValidations.password,
    confirmPassword: commonValidations.confirmPassword,
  })
  .refine(data => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'],
  });

// Profile schemas
export const profileSchema = z.object({
  first_name: commonValidations.firstName,
  last_name: commonValidations.lastName,
  professional_title: commonValidations.requiredString('Professional title'),
  contact_number: commonValidations.phoneNumber,
  address: commonValidations.optionalString(255),
  linkedin_url: commonValidations.url,
  summary: commonValidations.optionalString(1000),
});

// Skills schema
export const skillSchema = z.object({
  name: commonValidations.requiredString('Skill name', 1, 50),
});

export const skillsSchema = z.object({
  skills: z.array(skillSchema).min(1, 'At least one skill is required'),
});

// Education schemas
export const educationSchema = z.object({
  institution_name: commonValidations.requiredString(
    'Institution name',
    2,
    100,
  ),
  degree: commonValidations.requiredString('Degree', 2, 100),
  field_of_study: commonValidations.optionalString(100),
  address: commonValidations.requiredString('Address', 2, 255),
  start_date: commonValidations.dateString,
  end_date: commonValidations.dateString,
});

export const educationsSchema = z.object({
  educations: z
    .array(educationSchema)
    .min(1, 'At least one education entry is required'),
});

// Experience schemas
export const experienceSchema = z.object({
  job_title: commonValidations.requiredString('Job title', 2, 100),
  company_name: commonValidations.requiredString('Company name', 2, 100),
  start_date: commonValidations.dateString,
  end_date: commonValidations.optionalDateString,
  description: z
    .array(z.string().min(1, 'Description cannot be empty'))
    .min(1, 'At least one description is required')
    .optional(),
  is_current: z.boolean().default(false),
});

export const experiencesSchema = z.object({
  experiences: z.array(experienceSchema).optional().default([]),
});

// Certificate schemas
export const certificateSchema = z.object({
  name: commonValidations.optionalString(100),
  issuing_organization: commonValidations.optionalString(100),
  issue_date: commonValidations.optionalDateString,
  credential_url: commonValidations.url,
  credential_id: commonValidations.optionalString(50),
});

export const certificatesSchema = z.object({
  certificates: z.array(certificateSchema),
});

// Password change schema
export const passwordChangeSchema = z
  .object({
    currentPassword: z.string().min(1, 'Current password is required'),
    newPassword: commonValidations.password,
    confirmNewPassword: commonValidations.confirmPassword,
  })
  .refine(data => data.newPassword === data.confirmNewPassword, {
    message: "Passwords don't match",
    path: ['confirmNewPassword'],
  });

// Export types for TypeScript
export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type ProfileFormData = z.infer<typeof profileSchema>;
export type SkillsFormData = z.infer<typeof skillsSchema>;
export type EducationsFormData = z.infer<typeof educationsSchema>;
export type ExperiencesFormData = z.infer<typeof experiencesSchema>;
export type CertificatesFormData = z.infer<typeof certificatesSchema>;
export type PasswordChangeFormData = z.infer<typeof passwordChangeSchema>;
