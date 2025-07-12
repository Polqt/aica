'use client';

import { usePathname } from 'next/navigation';
import React from 'react';

const steps = [
  { path: '/profile', name: 'Personal Details', step: 1 },
  { path: '/education', name: 'Education', step: 2 },
  { path: '/experience', name: 'Work Experience', step: 3 },
  { path: '/skills', name: 'Skills & Summary', step: 4 },
];

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const currentStep = steps.find(s => s.path === pathname);

  return (
    <div className="container mx-auto max-w-2xl py-12">
      <div className="mb-8">
        {currentStep && (
          <>
            <p className="text-sm font-semibold text-primary">
              STEP {currentStep.step} OF {steps.length}
            </p>
            <h1 className="text-3xl font-bold">{currentStep.name}</h1>
          </>
        )}
      </div>
      {children}
    </div>
  );
}
