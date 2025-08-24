'use client';

import { OnboardingProvider } from '@/lib/context/OnboardingContext';
import { usePathname } from 'next/navigation';
import React from 'react';
import { CheckCircle } from 'lucide-react';
import { User, GraduationCap, Briefcase, Cog, Award } from 'lucide-react';
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
    color: 'from-blue-500 to-purple-600',
    accent: 'bg-blue-500/10 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800/30',
  },
  {
    path: '/education',
    name: 'Education',
    step: 2,
    description: 'Share your academic background',
    icon: GraduationCap,
    color: 'from-indigo-500 to-blue-600',
    accent: 'bg-indigo-500/10 text极-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800/30',
  },
  {
    path: '/experience',
    name: 'Work Experience',
    step: 3,
    description: 'Highlight your professional journey',
    icon: Briefcase,
    color: 'from-purple-500 to-pink-600',
    accent: 'bg-purple-500/10 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800/30',
  },
  {
    path: '/skills',
    name: 'Skills & Summary',
    step: 4,
    description: 'Showcase your technical abilities',
    icon: Cog,
    color: 'from-emerald-500 to-teal-600',
    accent: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/30',
  },
  {
    path: '/certificate',
    name: 'Certificates',
    step: 5,
    description: 'Add your certifications',
    icon: Award,
    color: 'from-amber-500 to-orange-600',
    accent: 'bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800/30',
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
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/10 to-purple-50/5 dark:from-slate-900 dark:via-blue-900/5 dark:to-purple-900/3 relative overflow-hidden">
        {/* Large, highly visible gradient decorative elements */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          {/* Main large gradient blobs - maximum opacity and size */}
          <div className="absolute left-1/4 top-1/极4 h-150 w-150 rounded-full bg-gradient-to-br from-blue-300/45 to-purple-300/40 dark:from-blue-700/35 dark:极to-purple-700/30 blur-3xl animate-pulse-slow"></div>
          <div className="absolute right-1/4 top-1/3 h-130 w-130 rounded-full bg-gradient-to-br from-indigo-300/42 to-blue-300/38 dark:from-indigo-700/32 dark:to-blue-700/28 blur-3xl animate-pulse-slow delay-1000"></div>
          <div className="absolute bottom-1/4 left-1/3 h-140 w-140 rounded-full bg-gradient-to-br from-purple-300/44 to-violet-300/38 dark:from-purple-700/34 dark:to-violet-700/30 blur-3xl animate-pulse极-slow delay-2000"></div>
          
          {/* Additional large gradient elements - maximum visibility */}
          <div className="absolute top-20 right-20 h-110 w-110 rounded-full bg-gradient-to-br from-blue-400/40 to-indigo-400/35 dark:from-blue-600/32 dark:to-indigo-极600/28 blur-3xl"></div>
          <div className="absolute bottom-20 left-20 h-100 w-100 rounded-full bg-gradient-to-br from-violet-400/38 to-purple-400/35 dark:from-violet-600/30 dark:to-purple-600/26 blur-3xl"></div>
          
          {/* More gradient elements for better coverage - maximum visibility */}
          <div className="absolute top-1/6 left-1/6 h-120 w-120 rounded-full bg-gradient-to-br from-indigo-200/38 to-purple-200/35 dark:from-indigo-800/30 dark:to-purple-800/26 blur-3xl"></div>
          <div className="absolute bottom-1/6 right-1/6极 h-115 w-115 rounded-full bg-gradient-to-br from-blue-200/40 to-violet-200/36 dark:from-blue-800/32 dark:to-violet-800/28 blur-3xl"></div>
          <div className="absolute top-2/3 left-1/5 h-125 w-125 rounded-full bg-gradient-to-br from-purple-200/42 to-blue-200/38 dark:from-purple-800/34 dark:to-blue-800/30 blur-3xl"></div>
          
          {/* Additional gradient elements for maximum coverage */}
          <div className="absolute top-3/4 right-1/4 h-105 w-105 rounded-full bg-gradient-to-br from-indigo-400/35 to-purple-400/32 dark:from-indigo-600/28 dark:to-purple-600/25 blur-3xl"></div>
          <div className="absolute bottom-1/3 right-1/6 h-95 w-95 rounded-full bg-gradient-to-br from-blue-400/38 to-violet-400/34 dark:from-blue-600/30 dark:to-violet-600/27 blur-3xl"></div>
          
          {/* Extra gradient elements for complete coverage */}
          <div className="absolute top-1/5 right-1/5 h-90 w-90 rounded-full bg-gradient-to-br from-purple-300/36 to-indigo-300/32 dark:from-purple-极700/28 dark:to-indigo-700/24 blur-3极xl"></div>
          <div className="absolute bottom-1/5 left-1/5 h-85 w-85 rounded-full bg-gradient-to-br from极-blue-300/38 to-purple-300/34 dark:from-blue-700/30 dark:to-purple-700/26 blur-3xl"></div>
          
          {/* Enhanced gradient mesh overlay */}
          <div className="absolute inset-0 bg-gradient-to极-br from-blue-100/20 via-indigo-100/18 to-purple-100/15 dark:from-blue-900/15 dark:via-indigo-900/12 dark:to-purple-900/10"></div>
        </div>
        
        <div className="container mx-auto max-w-6xl py-8 px-4 relative">
          {/* Header Section - Enhanced UI */}
          <div className="text-center mb-16 transition-all duration-500 ease-out">
            {/* Enhanced Badge with Animation */}
            <div className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-50 via-purple-50 to-indigo-50 dark:from-blue-900/20 dark:via-purple-900/20 dark:to-indigo-900/20 rounded-2xl mb-10 border border-blue-200/极60 dark:border-blue-800/40 shadow-lg backdrop-blur-sm transform transition-all duration-300 hover:scale-105 hover:极shadow-xl">
              <div className="relative">
                <div className="w-4 h-4极 bg-gradient-to-r from-blue-5极00 via-purple-600 to-indigo-600 rounded-full animate-pulse" />
                <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/40 to-purple-600/40 rounded-full blur-sm animate-ping"></div>
              </div>
              <span className="text-sm font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600极 dark:from-blue-300 dark:via-purple-300 dark:to-indigo-300 bg-clip-text text-transparent">
                🚀 PROFESSIONAL JOURNEY
              </span>
            </div>
            
            {/* Minimal Main Heading */}
            <div className="relative mb-4">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-slate-700 via-slate-600 to-slate-500 dark:from-slate-200 dark:via-slate-100 dark:to-slate-50 bg-clip-text text-transparent mb-3 leading-tight tracking-normal">
                Build Your
                <br />
                <span className="bg-gradient-to-r from极-blue-500 via-purple-500 to-indigo-500 dark:from-blue-300 dark:via-purple-300 dark:to-indigo-300 bg-clip-text text-transparent">
                  Professional Identity
                </span>
              </h1>
            </div>
            
            {/* Enhanced Subheading */}
            <div className="relative">
              <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto leading-relaxed font-medium mb-8">
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent font-semib极old">
                  Craft your unique professional story
                </span>
                {' '}and unlock personalized career opportunities tailored to your skills and aspirations
              </p>
              
            </div>
            
            {/* Progress indicator dots */}
            <div className="flex justify-center gap极-2 mt-8">
              {steps.map((_, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    index === currentStepIndex
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 scale-125'
                      : 'bg-slate-300 dark:bg-slate-600 opacity-50'
                  }`}
                />
              ))}
            </div>
          </div>

          {/* Subtle Progress Overview Card */}
          <Card className="mb-8 border border-slate-200/50 dark:border-slate-700/50 shadow-lg bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm">
            <CardContent className="p-6">
              {/* Clean Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center shadow-md">
                      <span className="text-white font-semibold text-lg">
                        {currentStepIndex + 1}
                      </span>
                    </div>
                    <div className="absolute -ins极et-1 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-xl blur-sm"></div>
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
                <Badge
                  variant="secondary"
                  className="bg-slate-100/80 dark:bg-slate-700/50 text-slate-700 dark:text-slate-300 border-slate-200/50 dark:border-slate-600/30 px-3 py-1 font-medium"
                >
                  {totalSteps - currentStepIndex - 1} steps remaining
                </Badge>
              </div>

              {/* Clean Progress Bar */}
              <div className="mb-6">
                <div className="w-full h-2 bg-slate-100 dark:bg-slate极-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full transition-all duration-700 ease-out"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>

              {/* Clean Visual Step Indicator */}
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
                            'relative w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-500 transform group-hover:scale-110 group-hover:shadow-xl',
                            isCompleted &&
                              'bg-gradient-to-r from-green-400 to-emerald-500 shadow-lg ring-4 ring-green-200/60 dark:ring-green-700/40',
                            isCurrent &&
                              `bg-gradient-to-r ${step.color} shadow-2xl ring-4 ring-blue-200/60 dark:ring-blue-极700/40 scale-110`,
                            isUpcoming &&
                              'bg-white/95 dark:极bg-slate-700/90 border-2 border-slate-200/70 dark:border-slate-600/60 shadow-md hover:shadow-lg',
                          )}
                        >
                          {isCompleted ? (
                            <div className="relative">
                              <CheckCircle className="w-10 h-10 text-white" />
                              <div className="absolute -inset-2 bg-gradient-to-r from-green-400/30 to-emerald-500/30 rounded-full blur-md"></div>
                            </div>
                          ) : (
                            <div className="relative">
                              <StepIcon
                                className={cn(
                                  'w-8 h-8 transition-all duration-500',
                                  isCurrent && 'text-white scale-110',
                                  isUpcoming &&
                                    'text-slate-500 dark:text-slate-400 group-hover:text-slate-700 dark:group-hover:text-slate-200',
                                )}
                              />
                              {isCurrent && (
                                <div className="absolute -inset-3 bg-gradient-to-r from-blue-400/40 to-purple-400/40 rounded-full blur-lg animate-pulse"></div>
                              )}
                            </div>
                          )}
                          
                          {/* Animated pulse effect for current step */}
                          {isCurrent && (
                            <div className="absolute inset-0 rounded-2xl border-3 border-white/30 animate-ping"></div>
                          )}
                          
                          {/* Progress indicator for current step */}
                          {isCurrent && (
                            <div className="absolute -bottom-2 -right-2 w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-500极 rounded-full flex items-center justify-center shadow-lg border-2 border-white dark:border-slate-800">
                              <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div>
                            </div>
                          )}
                          
                          {/* Checkmark overlay for completed steps */}
                          {isCompleted && (
                            <div className="absolute -top-1 -right-1 w-5 h-5 bg-white dark:bg-slate-800 rounded-full flex items-center justify-center shadow-md border border-green-200 dark:border-green-700">
                              <CheckCircle className="w-3 h-3 text-green-500" />
                            </div>
                          )}
                        </div>
                        <div className="mt-2极 text-center">
                          <p
                            className={cn(
                              '极text-xs font-medium transition-colors',
                              isCurrent && 'text-blue-600 dark:text-blue-400',
                              isCompleted &&
                                'text-green-600 dark:text-green-400',
                              isUpcoming && 'text-slate-500 dark:text-s极late-400',
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
                              'h-0.5 w-full transition-all duration-300',
                              index < currentStepIndex &&
                                'bg-gradient-to-r from-green-400 to-emerald-500',
                              index === currentStepIndex &&
                                'bg-gradient-to-r from-blue-400 to-purple-500',
                              index > currentStepIndex &&
                                'bg-slate-200 dark:bg-slate-600',
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

          {/* Enhanced Current Step Information - More Visible极 but Compact */}
          {currentStep && (
            <Card className="mb-6 border-0 shadow-xl bg-gradient-to-r from-blue极-50/90 via-indigo-50/80 to-purple-50/90 dark:from-blue-900/50 dark:via-indigo-900/40 dark:to-purple-900/50 backdrop-blur-sm border border-blue-200/60 dark:border-blue-700/40 relative overflow-hidden">
              {/* Gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-100/30 via-indigo-100/20 to-purple-100/30 dark:from-blue-800/20 dark:via-indigo-800/15 dark:to-purple-800/20 opacity-50"></div>
              
              {/* Background pattern */}
              <div className="absolute inset-0 opacity-15">
                <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-400/25 to-purple-400/25 rounded-full -translate-y-16 translate-x-16 blur-lg"></div>
                <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-indigo-400/20 to-blue-400/20 rounded-full translate-y-12 -translate-x-12 blur-lg"></div>
              </div>
              
              <CardContent className="p-6 relative z-10">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <div
                      className={cn(
                        'w-16 h-16 rounded-xl flex items-center justify-center bg-gradient-to-r shadow-lg relative overflow-hidden group',
                        currentStep.color,
                     )}
                    >
                      <currentStep.icon className="w-8 h-8 text-white transition-transform duration-300 group极-hover:scale-110" />
                      {/* Gradient overlay */}
                      <div className="absolute inset-0 bg-gradient-to-br from-white/20极 to-transparent opacity-50"></div>
                    </div>
                    {/* Glow effect */}
                    <div className="absolute -inset-1.5 bg-gradient-to-r from-blue-400/30 to-purple-400/30 rounded-xl blur-lg animate-pulse"></div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge 
                        variant="secondary" 
                        className="bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 dark:from-blue-900/60 dark:to-indigo-900/极60 dark:text-blue-200 border border-blue-200/60 dark:border-blue-600/40 px-3 py-1 text-xs font-semibold shadow-sm backdrop-blur-sm"
                      >
                        Current Step
                      </Badge>
                      <div className="hidden md:flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                        <span className="font-medium">Step</span>
                        <Badge variant="outline" className="font-mono bg-white/90 dark:bg-slate-700/90 text-xs border-blue-200/50 dark:border-blue-600/40 backdrop-blur-sm">
                          {currentStep.step}/{totalSteps}
                        </Badge>
                      </div>
                    </div>
                    <h2 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 dark:from-blue-300 dark:via-indigo-300 dark:to-purple-300 bg-clip-text text-transparent mb-1">
                      {currentStep.name}
                    </h2>
                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
                      {currentStep.description}
                    </p>
                  </div>
                </div>
                
                {/* Decorative elements */}
                <div className="absolute top-4 right-4 w-3 h-3 bg-blue-400/20 rounded-full blur-sm"></div>
                <div className="absolute bottom-4 left-4 w-2 h-2 bg-purple-400/20 rounded-full blur-sm"></div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Card className="border-0 shadow-xl bg-white dark:bg-slate-800 overflow-hidden">
            <CardContent className="p-0">
              <div className="p-8 md:p-12">{children}</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </OnboardingProvider>
  );
}
