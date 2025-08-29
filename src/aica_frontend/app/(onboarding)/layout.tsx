'use client';

import { OnboardingProvider } from '@/lib/context/OnboardingContext';

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <OnboardingProvider>
      {children}
    </OnboardingProvider>
  );
}