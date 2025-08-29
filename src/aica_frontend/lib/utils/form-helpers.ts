import { FieldError } from 'react-hook-form';
import { toast } from 'sonner';

export interface FormFieldProps {
  value?: string;
  onChange?: (value: string) => void;
  error?: FieldError;
  disabled?: boolean;
  required?: boolean;
}

export const computeFormCompletion = (
  watchedFields: Record<string, unknown>,
  requiredFields: string[]
): { percentage: number; completed: number; total: number } => {
  const completed = requiredFields.filter(field => {
    const value = watchedFields[field];
    return value && value.toString().trim() !== '';
  }).length;

  const percentage = Math.round((completed / requiredFields.length) * 100);

  return { percentage, completed, total: requiredFields.length };
};

export const showFormSuccess = (message: string, description?: string) => {
  toast.success(message, { description, duration: 3000 });
};

export const showFormError = (message: string, description?: string) => {
  toast.error(message, { description, duration: 5000 });
};

export const formatDateForDisplay = (dateString: string): string => {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
    });
  } catch {
    return dateString;
  }
};

export const validateFileSize = (file: File, maxSizeMB: number = 5): boolean => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  if (file.size > maxSizeBytes) {
    showFormError(
      'File too large',
      `Please select a file smaller than ${maxSizeMB}MB`
    );
    return false;
  }
  return true;
};

export const validateFileType = (file: File, allowedTypes: string[]): boolean => {
  if (!allowedTypes.some(type => file.type.startsWith(type))) {
    showFormError(
      'Invalid file type',
      `Please select a valid file type: ${allowedTypes.join(', ')}`
    );
    return false;
  }
  return true;
};

export const convertFileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      resolve(result);
    };
    reader.onerror = () => {
      reject(new Error('Failed to read file'));
    };
    reader.readAsDataURL(file);
  });
};

export const createFormFieldProps = (
  form: {
    watch: (name: string) => unknown;
    setValue: (name: string, value: unknown) => void;
    formState: { errors: Record<string, FieldError> };
  },
  fieldName: string,
  required: boolean = false
): FormFieldProps => {
  return {
    value: form.watch(fieldName) as string,
    onChange: (value: string) => form.setValue(fieldName, value),
    error: form.formState.errors[fieldName],
    required,
  };
};

export const getFieldErrorMessage = (error?: FieldError): string => {
  return error?.message || '';
};

export const isFieldValid = (error?: FieldError): boolean => {
  return !error;
};

export const getCharacterCount = (value?: string): number => {
  return value?.length || 0;
};

export const isFormStepComplete = (
  watchedFields: Record<string, unknown>,
  requiredFields: string[],
  additionalChecks: (() => boolean)[] = []
): boolean => {
  const allRequiredFieldsFilled = requiredFields.every(field => {
    const value = watchedFields[field];
    return value && value.toString().trim() !== '';
  });

  const allAdditionalChecksPass = additionalChecks.every(check => check());

  return allRequiredFieldsFilled && allAdditionalChecksPass;
};