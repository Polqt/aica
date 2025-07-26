import { ProfileUpdate } from '@/lib/types/profile';
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface OnboardingState {
  profileData: ProfileUpdate;
  setPersonalDetails: (data: Partial<ProfileUpdate>) => void;
  setEducations: (data: ProfileUpdate['educations']) => void;
  setExperiences: (data: ProfileUpdate['experiences']) => void;
  setSkillsAndSummary: (data: {
    skills?: string[] | ProfileUpdate['skills'];
    summary?: string;
  }) => void;
  getCombinedProfileData: () => ProfileUpdate;
  resetOnboarding: () => void;
}

const initialState: ProfileUpdate = {
  first_name: '',
  last_name: '',
  professional_title: '',
  contact_number: '',
  address: '',
  linkedin_url: '',
  summary: '',
  educations: [],
  experiences: [],
  skills: [],
  certificates: [],
};

export const useOnboardingStore = create<OnboardingState>()(
  devtools(
    persist(
      (set, get) => ({
        profileData: initialState,

        setPersonalDetails: data =>
          set(state => ({
            profileData: {
              ...state.profileData,
              ...data,
            },
          })),

        setEducations: educations =>
          set(state => ({
            profileData: {
              ...state.profileData,
              educations,
            },
          })),

        setExperiences: experiences =>
          set(state => ({
            profileData: {
              ...state.profileData,
              experiences,
            },
          })),

        setSkillsAndSummary: data =>
          set(state => ({
            profileData: {
              ...state.profileData,
              // Convert string[] to SkillCreate[] if needed
              ...(data.skills && {
                skills:
                  Array.isArray(data.skills) &&
                  typeof data.skills[0] === 'string'
                    ? (data.skills as string[]).map(name => ({ name }))
                    : (data.skills as ProfileUpdate['skills']),
              }),
              ...(data.summary && { summary: data.summary }),
            },
          })),

        getCombinedProfileData: () => {
          return get().profileData;
        },

        resetOnboarding: () => {
          set({ profileData: initialState });
        },
      }),
      {
        name: 'onboarding-storage',
      },
    ),
  ),
);
