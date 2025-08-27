'use client';

import { OnboardingProvider } from '@/lib/context/OnboardingContext';
import { usePathname } from 'next/navigation';
import { CheckCircle } from 'lucide-react';
import { User, GraduationCap, Briefcase, Cog, Award } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import React from 'react';

const steps = [
  {
    path: '/profile',
    name: 'Personal Info',
    step: 1,
    description: 'Tell us about yourself',
    icon: User,
  },
  {
    path: '/education',
    name: 'Education',
    step: 2,
    description: 'Share your academic background',
    icon: GraduationCap,
  },
  {
    path: '/experience',
    name: 'Work Experience',
    step: 3,
    description: 'Highlight your professional journey',
    icon: Briefcase,
  },
  {
    path: '/skills',
    name: 'Skills & Summary',
    step: 4,
    description: 'Showcase your technical abilities',
    icon: Cog,
  },
  {
    path: '/certificate',
    name: 'Certificates',
    step: 5,
    description: 'Add your certifications',
    icon: Award,
  },
];

export default function OnboardingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const currentStep = steps.find(s => s.path === pathname);
  const currentStepIndex = currentStep ? currentStep.step - 1 : 0;
  const totalSteps = steps.length;
  const progressPercentage = ((currentStepIndex + 1) / totalSteps) * 100;

  return (
    <OnboardingProvider>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
        <div className="container mx-auto max-w-4xl py-8 px-4">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-3 px-6 py-3 bg-blue-50 dark:bg-blue-900/20 rounded-full mb-6 border border-blue-200/50 dark:border-blue-800/50">
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse" />
              <span className="text-sm font-semibold text-blue-700 dark:text-blue-300">
                AICA Professional Profile Setup
              </span>
            </div>
            
            <h1 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-white mb-4">
              Build Your Professional Profile
            </h1>
            <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
              Complete your profile to unlock personalized career opportunities
            </p>
          </div>

          {/* Progress Card */}
          <Card className="mb-8 shadow-sm">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center shadow-sm">
                    <span className="text-white font-semibold text-lg">
                      {currentStepIndex + 1}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
                      Step {currentStepIndex + 1} of {totalSteps}
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-300">
                      {Math.round(progressPercentage)}% Complete
                    </p>
                  </div>
                </div>
                <Badge variant="secondary">
                  {totalSteps - currentStepIndex - 1} steps remaining
                </Badge>
              </div>

              {/* Progress Bar */}
              <div className="mb-6">
                <div className="w-full h-2 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-500 rounded-full transition-all duration-500"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>

              {/* Step Icons */}
              <div className="flex items-center justify-between">
                {steps.map((step, index) => {
                  const StepIcon = step.icon;
                  const isCompleted = index < currentStepIndex;
                  const isCurrent = index === currentStepIndex;
                  const isUpcoming = index > currentStepIndex;

                  return (
                    <React.Fragment key={step.path}>
                      <div className="flex flex-col items-center">
                        <div
                          className={cn(
                            'w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300',
                            isCompleted && 'bg-green-500 shadow-sm',
                            isCurrent && 'bg-blue-500 shadow-sm',
                            isUpcoming && 'bg-slate-200 dark:bg-slate-700'
                          )}
                        >
                          {isCompleted ? (
                            <CheckCircle className="w-6 h-6 text-white" />
                          ) : (
                            <StepIcon
                              className={cn(
                                'w-6 h-6',
                                isCurrent && 'text-white',
                                isUpcoming && 'text-slate-400 dark:text-slate-500'
                              )}
                            />
                          )}
                        </div>
                        <p className="text-xs font-medium mt-2 text-center">
                          {step.name}
                        </p>
                      </div>
                      {index < steps.length - 1 && (
                        <div className="flex-1 flex items-center justify-center px-2">
                          <div
                            className={cn(
                              'h-0.5 w-full transition-all duration-300',
                              index < currentStepIndex && 'bg-green-500',
                              index === currentStepIndex && 'bg-blue-500',
                              index > currentStepIndex && 'bg-slate-200 dark:bg-slate-600'
                            )}
                          />
                        </div>
                      )}
                    </React.Fragment>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Current Step Info */}
          {currentStep && (
            <Card className="mb-6 bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                    <currentStep.icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge className="bg-blue-500 text-white text-xs">
                        Current Step
                      </Badge>
                    </div>
                    <h2 className="text-xl font-bold text-blue-800 dark:text-blue-200">
                      {currentStep.name}
                    </h2>
                    <p className="text-sm text-blue-600 dark:text-blue-300">
                      {currentStep.description}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Card className="shadow-sm">
            <CardContent className="p-8">
              {children}
            </CardContent>
          </Card>
        </div>
      </div>
    </OnboardingProvider>
  );
}
