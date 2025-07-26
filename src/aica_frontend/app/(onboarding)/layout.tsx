'use client';

import { OnboardingProvider } from '@/lib/context/OnboardingContext';
import { usePathname } from 'next/navigation';
import React from 'react';
import {
  CheckCircle,
  User,
  GraduationCap,
  Briefcase,
  Star,
  Award,
  ChevronRight,
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';

const steps = [
  {
    path: '/profile',
    name: 'Personal Info',
    step: 1,
    description: 'Tell us about yourself',
    icon: User,
    color: 'from-blue-500 to-indigo-600',
  },
  {
    path: '/education',
    name: 'Education',
    step: 2,
    description: 'Share your academic background',
    icon: GraduationCap,
    color: 'from-emerald-500 to-teal-600',
  },
  {
    path: '/experience',
    name: 'Work Experience',
    step: 3,
    description: 'Highlight your professional journey',
    icon: Briefcase,
    color: 'from-purple-500 to-violet-600',
  },
  {
    path: '/skills',
    name: 'Skills & Summary',
    step: 4,
    description: 'Showcase your technical abilities',
    icon: Star,
    color: 'from-orange-500 to-red-600',
  },
  {
    path: '/certificate',
    name: 'Certificates',
    step: 5,
    description: 'Add your certifications',
    icon: Award,
    color: 'from-pink-500 to-rose-600',
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
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-700">
        <div className="container mx-auto max-w-6xl py-6 px-4">
          {/* Header Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-4">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" />
              <span className="text-sm font-medium text-blue-700 dark:text-blue-300">
                Profile Setup
              </span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-3">
              Complete Your Professional Profile
            </h1>
            <p className="text-gray-600 dark:text-gray-300 text-lg max-w-2xl mx-auto">
              Help us understand your background to find the perfect job matches
              tailored for you
            </p>
          </div>

          {/* Progress Overview Card */}
          <Card className="mb-8 border-0 shadow-lg bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">
                      {currentStepIndex + 1}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      Step {currentStepIndex + 1} of {totalSteps}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {Math.round(progressPercentage)}% Complete
                    </p>
                  </div>
                </div>
                <Badge
                  variant="secondary"
                  className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800"
                >
                  {totalSteps - currentStepIndex - 1} steps remaining
                </Badge>
              </div>
              <Progress
                value={progressPercentage}
                className="w-full h-3 mb-4 bg-gray-100 dark:bg-gray-700"
              />

              {/* Visual Step Indicator */}
              <div className="flex items-center justify-between">
                {steps.map((step, index) => {
                  const StepIcon = step.icon;
                  const isCompleted = index < currentStepIndex;
                  const isCurrent = index === currentStepIndex;
                  const isUpcoming = index > currentStepIndex;

                  return (
                    <React.Fragment key={step.path}>
                      <div className="flex flex-col items-center group">
                        <div
                          className={cn(
                            'relative w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300 transform group-hover:scale-105',
                            isCompleted &&
                              'bg-gradient-to-r from-green-500 to-emerald-600 shadow-lg shadow-green-500/25',
                            isCurrent &&
                              `bg-gradient-to-r ${step.color} shadow-lg shadow-blue-500/25`,
                            isUpcoming &&
                              'bg-gray-100 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600',
                          )}
                        >
                          {isCompleted ? (
                            <CheckCircle className="w-6 h-6 text-white" />
                          ) : (
                            <StepIcon
                              className={cn(
                                'w-6 h-6',
                                isCurrent && 'text-white',
                                isUpcoming &&
                                  'text-gray-400 dark:text-gray-500',
                              )}
                            />
                          )}
                          {isCurrent && (
                            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl blur opacity-30 animate-pulse" />
                          )}
                        </div>
                        <div className="mt-2 text-center hidden sm:block">
                          <p
                            className={cn(
                              'text-xs font-medium transition-colors',
                              isCurrent && 'text-blue-600 dark:text-blue-400',
                              isCompleted &&
                                'text-green-600 dark:text-green-400',
                              isUpcoming && 'text-gray-400 dark:text-gray-500',
                            )}
                          >
                            {step.name}
                          </p>
                        </div>
                      </div>
                      {index < steps.length - 1 && (
                        <div className="flex-1 flex items-center justify-center px-2">
                          <div
                            className={cn(
                              'h-0.5 w-full transition-all duration-500',
                              index < currentStepIndex &&
                                'bg-gradient-to-r from-green-500 to-emerald-600',
                              index === currentStepIndex &&
                                'bg-gradient-to-r from-blue-500 to-indigo-600',
                              index > currentStepIndex &&
                                'bg-gray-200 dark:bg-gray-600',
                            )}
                          />
                          <ChevronRight
                            className={cn(
                              'w-4 h-4 mx-1 transition-colors',
                              index < currentStepIndex && 'text-green-500',
                              index === currentStepIndex && 'text-blue-500',
                              index > currentStepIndex && 'text-gray-400',
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

          {/* Current Step Information */}
          {currentStep && (
            <Card className="mb-8 border-0 shadow-sm bg-gradient-to-r from-white to-gray-50 dark:from-gray-800 dark:to-gray-700">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div
                    className={cn(
                      'w-16 h-16 rounded-2xl flex items-center justify-center bg-gradient-to-r shadow-lg',
                      currentStep.color,
                    )}
                  >
                    <currentStep.icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="outline" className="text-xs">
                        Current Step
                      </Badge>
                    </div>
                    <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-1">
                      {currentStep.name}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 text-base">
                      {currentStep.description}
                    </p>
                  </div>
                  <div className="hidden md:flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                    <span>Step</span>
                    <Badge variant="secondary" className="font-mono">
                      {currentStep.step}/{totalSteps}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Card className="border-0 shadow-xl bg-white dark:bg-gray-800 overflow-hidden">
            <CardContent className="p-0">
              <div className="p-8 md:p-12">{children}</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </OnboardingProvider>
  );
}
