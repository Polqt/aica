import { useState } from 'react';
import { toast } from 'sonner';

export interface UseFormSubmissionProps<T> {
  onSubmit: (data: T) => Promise<void> | void;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  successMessage?: string;
  errorMessage?: string;
}

export function useFormSubmission<T>({
  onSubmit,
  onSuccess,
  onError,
  successMessage,
  errorMessage,
}: UseFormSubmissionProps<T>) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async (data: T) => {
    if (isSubmitting) return;

    setIsSubmitting(true);
    setApiError(null);

    try {
      await onSubmit(data);

      if (successMessage) {
        toast.success(successMessage);
      }

      onSuccess?.(data);
    } catch (error) {
      const errorMsg =
        error instanceof Error ? error.message : 'An error occurred';
      setApiError(errorMsg);

      if (errorMessage) {
        toast.error(errorMessage);
      } else {
        toast.error(errorMsg);
      }

      onError?.(error instanceof Error ? error : new Error(errorMsg));
    } finally {
      setIsSubmitting(false);
    }
  };

  const clearApiError = () => setApiError(null);

  return {
    isSubmitting,
    apiError,
    handleSubmit,
    clearApiError,
    setApiError,
  };
}

export function useAsyncOperation() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async <T>(operation: () => Promise<T>): Promise<T | null> => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await operation();
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      toast.error(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const clearError = () => setError(null);

  return {
    isLoading,
    error,
    execute,
    clearError,
  };
}
