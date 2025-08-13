'use client';

import { createContext, useContext, useState } from 'react';
import { ProfileUpdate, SkillCreate } from '../types/profile';
import { apiClient } from '../api';
import { toast } from 'sonner';

type OnboardingData = Omit<Partial<ProfileUpdate>, 'skills'> & {
  skills?: (string | SkillCreate)[];
};

interface OnboardingContextProps {
  data: OnboardingData;
  updateData: (partial: OnboardingData) => void;
  submitOnboardingData: () => Promise<{ success: boolean }>;
  clearData: () => void;
}

const OnboardingContext = createContext<OnboardingContextProps | undefined>(
  undefined,
);

export const OnboardingProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [data, setData] = useState<OnboardingData>({});

  const updateData = (partial: OnboardingData) => {
    setData(prev => ({
      ...prev,
      ...partial,
    }));
  };

  const clearData = () => setData({});
  const formatDate = (dateString: string | undefined): string | undefined => {
    if (!dateString || dateString.trim() === '') return undefined;

    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        console.warn('Invalid date format:', dateString);
        return undefined;
      }

      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    } catch (error) {
      console.warn('Error formatting date:', dateString, error);
      return undefined;
    }
  };
  const submitOnboardingData = async () => {
    try {
      console.log('Submitting onboarding data:', JSON.stringify(data, null, 2));

      const transformedData: ProfileUpdate = {
        ...data,

        skills:
          data.skills?.map(skill =>
            typeof skill === 'string' ? { name: skill } : skill,
          ) || [],

        educations: data.educations?.map(edu => ({
          ...edu,
          start_date: formatDate(edu.start_date) || '',
          end_date: formatDate(edu.end_date) || '',
        })),

        experiences: data.experiences?.map(exp => ({
          ...exp,
          start_date: formatDate(exp.start_date) || '',
          end_date: exp.end_date ? formatDate(exp.end_date) : undefined,
        })),

        certificates: data.certificates?.map(cert => ({
          ...cert,
          issue_date: cert.issue_date ? formatDate(cert.issue_date) : undefined,
        })),
      };

      console.log(
        'Transformed data for backend:',
        JSON.stringify(transformedData, null, 2),
      );
      await apiClient.profile.updateProfile(transformedData);

      toast.success('Profile Updated!', {
        description: 'Your profile has been saved successfully.',
      });

      clearData();
      return { success: true };
    } catch (error) {
      console.error('Failed to submit onboarding data:', error);

      const errorMessage =
        error instanceof Error
          ? error.message
          : 'Failed to save profile. Please try again.';
      toast.error('Profile Save Failed', {
        description: errorMessage,
      });

      throw error;
    }
  };

  return (
    <OnboardingContext.Provider
      value={{ data, updateData, submitOnboardingData, clearData }}
    >
      {children}
    </OnboardingContext.Provider>
  );
};

export const useOnboarding = () => {
  const context = useContext(OnboardingContext);

  if (!context) {
    throw new Error('useOnboarding must be used within an OnboardingProvider');
  }
  return context;
};
