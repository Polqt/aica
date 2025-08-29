'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle,
  Home,
  User,
  GraduationCap,
  Briefcase,
  Award,
} from 'lucide-react';
import AnimatedBackground from './AnimatedBackground';

interface OnboardingLayoutProps {
  children: React.ReactNode;
  currentStep: string;
  title: string;
  description: string;
  stepNumber: number;
  totalSteps: number;
}

const stepConfig = {
  profile: { icon: User, label: 'Profile', path: '/profile' },
  education: { icon: GraduationCap, label: 'Education', path: '/education' },
  skills: { icon: Briefcase, label: 'Skills', path: '/skills' },
  experience: { icon: Briefcase, label: 'Experience', path: '/experience' },
  certificates: { icon: Award, label: 'Certificates', path: '/certificates' },
};

export default function OnboardingLayout({
  children,
  currentStep,
  title,
  description,
  stepNumber,
  totalSteps,
}: OnboardingLayoutProps) {
  const router = useRouter();
  const { completionStatus } = useOnboarding();

  const steps = ['profile', 'education', 'skills', 'experience', 'certificates'];
  const currentIndex = steps.indexOf(currentStep);

  const handleStepClick = (step: string) => {
    if (completionStatus?.completed_steps.includes(step) || step === currentStep) {
      router.push(stepConfig[step as keyof typeof stepConfig].path);
    }
  };

  const handleNext = () => {
    if (currentIndex < steps.length - 1) {
      const nextStep = steps[currentIndex + 1];
      router.push(stepConfig[nextStep as keyof typeof stepConfig].path);
    } else {
      router.push('/dashboard');
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      const prevStep = steps[currentIndex - 1];
      router.push(stepConfig[prevStep as keyof typeof stepConfig].path);
    }
  };

  const handleSkip = () => {
    router.push('/dashboard');
  };

  const overallProgress = completionStatus?.overall_completion_percentage ?? 0;

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/40 to-purple-50/30 dark:from-slate-900 dark:via-blue-900/20 dark:to-purple-900/15 py-8 px-4 overflow-hidden">
      <AnimatedBackground />

      {/* Header */}
      <div className="max-w-4xl mx-auto mb-8">
        <div className="flex items-center justify-between mb-6">
          <Button
            variant="ghost"
            onClick={() => router.push('/dashboard')}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200"
          >
            <Home className="w-4 h-4" />
            Dashboard
          </Button>

          <Badge
            variant="secondary"
            className="bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 dark:from-blue-900/50 dark:to-purple-900/50 dark:text-blue-200 border-blue-200/60 dark:border-blue-700/30 px-3 py-1 text-xs font-semibold"
          >
            Step {stepNumber} of {totalSteps}
          </Badge>
        </div>

        {/* Overall Progress */}
        <Card className="mb-6 border-0 shadow-lg bg-gradient-to-r from-blue-50/40 via-purple-50/30 to-indigo-50/20 dark:from-blue-900/20 dark:via-purple-900/15 dark:to-indigo-900/10 backdrop-blur-sm">
          <div className="p-6">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h2 className="text-lg font-semibold text-slate-800 dark:text-white">
                  Overall Progress
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  {overallProgress}% Complete
                </p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {overallProgress}%
                </p>
              </div>
            </div>
            <Progress value={overallProgress} className="h-3" />
          </div>
        </Card>

        {/* Step Navigation */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            {steps.map((step, index) => {
              const StepIcon = stepConfig[step as keyof typeof stepConfig].icon;
              const isCompleted = completionStatus?.completed_steps.includes(step);
              const isCurrent = step === currentStep;
              const isAccessible = isCompleted || step === currentStep;

              return (
                <React.Fragment key={step}>
                  <button
                    onClick={() => handleStepClick(step)}
                    disabled={!isAccessible}
                    className={`flex flex-col items-center p-3 rounded-xl transition-all duration-300 ${
                      isCurrent
                        ? 'bg-blue-500 text-white shadow-lg scale-105'
                        : isCompleted
                        ? 'bg-green-500 text-white hover:bg-green-600 shadow-md'
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-400 dark:text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle className="w-6 h-6 mb-1" />
                    ) : (
                      <StepIcon className="w-6 h-6 mb-1" />
                    )}
                    <span className="text-xs font-medium">
                      {stepConfig[step as keyof typeof stepConfig].label}
                    </span>
                  </button>
                  {index < steps.length - 1 && (
                    <div className={`w-8 h-0.5 ${
                      completionStatus?.completed_steps.includes(step)
                        ? 'bg-green-500'
                        : 'bg-slate-200 dark:bg-slate-600'
                    }`} />
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Step Content Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 dark:from-white dark:to-slate-200 bg-clip-text text-transparent mb-4">
            {title}
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
            {description}
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto">
        {children}
      </div>

      {/* Navigation Footer */}
      <div className="max-w-4xl mx-auto mt-8">
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Previous
          </Button>

          <div className="flex items-center gap-3">
            {currentStep !== 'profile' && (
              <Button
                variant="ghost"
                onClick={handleSkip}
                className="text-slate-600 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200"
              >
                Skip for now
              </Button>
            )}

            <Button
              onClick={handleNext}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              {currentIndex === steps.length - 1 ? 'Complete Setup' : 'Next'}
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}