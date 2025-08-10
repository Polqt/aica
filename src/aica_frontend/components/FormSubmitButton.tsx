'use client';

import React from 'react';
import { Button } from './ui/button';
import { ArrowRight } from 'lucide-react';


interface FormSubmitButtonProps {
  isSubmitting: boolean;
  isDisabled?: boolean;
  submitText?: string;
  submittingText?: string;
  className?: string;
  icon?: React.ReactNode;
}

export default function FormSubmitButton({
  isSubmitting,
  isDisabled = false,
  submitText = 'Submit',
  submittingText = 'Submitting...',
  className = '',
  icon = <ArrowRight className="w-4 h-4" />,
}: FormSubmitButtonProps) {
  return (
    <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
      <Button
        type="submit"
        disabled={isSubmitting || isDisabled}
        className={`w-full h-12 text-base font-medium bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 transition-all duration-200 flex items-center justify-center gap-2 ${className}`}
      >
        {isSubmitting ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            {submittingText}
          </>
        ) : (
          <>
            {submitText}
            {icon}
          </>
        )}
      </Button>
    </div>
  );
}
