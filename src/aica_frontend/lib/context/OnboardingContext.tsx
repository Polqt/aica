'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { ProfileUpdate, SkillCreate, ProfileCompletionStatus } from '../types/profile';
import { toast } from 'sonner';
import { apiClient } from '../services/api-client';

type OnboardingData = Omit<Partial<ProfileUpdate>, 'skills'> & {
  skills?: (string | SkillCreate)[];
};

interface OnboardingContextProps {
  data: OnboardingData;
  updateData: (partial: OnboardingData) => void;
  submitOnboardingData: (
    partial?: OnboardingData,
  ) => Promise<{ success: boolean }>;
  clearData: () => void;
  completionStatus: ProfileCompletionStatus | null;
  refreshCompletionStatus: () => Promise<void>;
  isLoadingStatus: boolean;
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
  const [completionStatus, setCompletionStatus] = useState<ProfileCompletionStatus | null>(null);
  const [isLoadingStatus, setIsLoadingStatus] = useState(false);

  // Load completion status on mount
  useEffect(() => {
    refreshCompletionStatus();
  }, []);

  const updateData = (partial: OnboardingData) => {
    setData(prev => ({
      ...prev,
      ...partial,
    }));
  };

  const refreshCompletionStatus = async () => {
    try {
      setIsLoadingStatus(true);
      const status = await apiClient.profile.getCompletionStatus();
      setCompletionStatus(status);
    } catch (error) {
      console.error('Failed to fetch completion status:', error);
      // Don't show error toast for status checks
    } finally {
      setIsLoadingStatus(false);
    }
  };

  const clearData = () => setData({});
  const formatDate = (dateString: string | undefined): string | undefined => {
    if (!dateString || dateString.trim() === '') return undefined;

    if (dateString.length === 7 && dateString.includes('-')) {
      return `${dateString}-01`;
    }
    return dateString;
  };

  const submitOnboardingData = async (partial?: OnboardingData) => {
    try {
      const source = { ...data, ...(partial || {}) } as OnboardingData;

      const skills = (source.skills || [])
        .map(s => (typeof s === 'string' ? { name: s } : s))
        .filter(s => s && typeof s.name === 'string' && s.name.trim() !== '');

      const educations = (source.educations || [])
        .filter(
          e =>
            e &&
            e.institution_name &&
            e.institution_name.trim() !== '' &&
            e.address &&
            e.address.trim() !== '' &&
            e.degree &&
            e.degree.trim() !== '' &&
            e.start_date &&
            e.end_date,
        )
        .map(e => ({
          ...e,
          start_date: formatDate(e.start_date)!,
          end_date: formatDate(e.end_date)!,
        }));

      const experiences = (source.experiences || [])
        .filter(
          ex =>
            ex &&
            ex.job_title &&
            ex.job_title.trim() !== '' &&
            ex.company_name &&
            ex.company_name.trim() !== '' &&
            ex.start_date,
        )
        .map(ex => ({
          ...ex,
          start_date: formatDate(ex.start_date)!,
          end_date: ex.end_date ? formatDate(ex.end_date) : undefined,
        }));

      const certificates = (source.certificates || [])
        .filter(
          c =>
            c &&
            c.name &&
            c.name.trim() !== '' &&
            c.issuing_organization &&
            c.issuing_organization.trim() !== '',
        )
        .map(c => ({
          ...c,
          issue_date: c.issue_date ? formatDate(c.issue_date) : undefined,
        }));

      const transformedData: ProfileUpdate = {
        ...(source as ProfileUpdate),
        skills,
        educations,
        experiences,
        certificates,
      };

      await apiClient.profile.update(transformedData);

      toast.success('Profile Updated!', {
        description: 'Your profile has been saved successfully.',
      });

      // Refresh completion status after successful update
      await refreshCompletionStatus();

      // Keep data until final step navigation completes
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
      value={{
        data,
        updateData,
        submitOnboardingData,
        clearData,
        completionStatus,
        refreshCompletionStatus,
        isLoadingStatus
      }}
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
