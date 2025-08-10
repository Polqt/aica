'use client';

import z from 'zod';
import React, { useState } from 'react';
import { useForm, FormProvider, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Form } from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import ExperienceCard from '@/components/ExperienceCard';
import {
  Plus,
  Briefcase,
  AlertCircle,
  ArrowRight,
  TrendingUp,
  CheckCircle2,
  Lightbulb,
} from 'lucide-react';

const experienceItemSchema = z.object({
  job_title: z
    .string()
    .min(2, 'Job title must be at least 2 characters')
    .max(100, 'Job title must be less than 100 characters'),
  company_name: z
    .string()
    .min(2, 'Company name must be at least 2 characters')
    .max(100, 'Company name must be less than 100 characters'),
  start_date: z.string().min(1, 'Start date is required'),
  end_date: z.string().optional(),
  description: z
    .array(z.string().min(1, 'Description cannot be empty'))
    .min(1, 'At least one accomplishment is required')
    .max(10, 'Maximum 10 accomplishments allowed'),
  is_current: z.boolean(),
});

const experienceFormSchema = z.object({
  experiences: z
    .array(experienceItemSchema)
    .max(10, 'Maximum 10 work experiences allowed'),
});

export default function Experience() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
  const { updateData } = useOnboarding();
  const [expandedIndexes, setExpandedIndexes] = useState<number[]>([0]);

  const form = useForm<z.infer<typeof experienceFormSchema>>({
    resolver: zodResolver(experienceFormSchema),
    defaultValues: {
      experiences: [],
    },
    mode: 'onBlur',
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'experiences',
  });

  const toggleExpand = (index: number) => {
    setExpandedIndexes(prev =>
      prev.includes(index) ? prev.filter(i => i !== index) : [...prev, index],
    );
  };

  const addExperience = () => {
    if (fields.length >= 10) {
      toast.error('Maximum limit reached', {
        description: 'You can add up to 10 work experiences only.',
      });
      return;
    }

    append({
      job_title: '',
      company_name: '',
      start_date: '',
      end_date: '',
      description: [''],
      is_current: false,
    });

    setExpandedIndexes(prev => [...prev, fields.length]);

    toast.success('New experience record added!', {
      description: 'Fill in the details for your new work experience.',
    });
  };

  async function onSubmit(values: z.infer<typeof experienceFormSchema>) {
    setApiError(null);
    form.clearErrors();

    try {
      updateData({ experiences: values.experiences });

      const hasExperience = values.experiences.length > 0;

      toast.success(
        hasExperience ? 'Work Experience Saved!' : 'Skipping Work Experience',
        {
          description: hasExperience
            ? `Successfully added ${
                values.experiences.length
              } experience record${
                values.experiences.length > 1 ? 's' : ''
              }. Let's add your skills next.`
            : "No problem! You can always add work experience later. Let's continue with your skills.",
          duration: 3000,
        },
      );

      setTimeout(() => {
        router.push('/skills');
      }, 1000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';

      setApiError(errorMessage);
      toast.error('Experience Update Failed', {
        description: errorMessage,
        duration: 5000,
      });
    }
  }

  const skipExperience = () => {
    updateData({ experiences: [] });

    toast.info('Skipping Work Experience', {
      description:
        'No worries! You can add work experience later from your profile.',
      duration: 3000,
    });

    setTimeout(() => {
      router.push('/skills');
    }, 1000);
  };

  const watchedExperiences = form.watch('experiences');
  const totalFields = watchedExperiences.reduce((acc, exp) => {
    return acc + 4 + exp.description.length;
  }, 0);

  const completedFields = watchedExperiences.reduce((acc, exp) => {
    let completed = 0;
    if (exp.job_title?.trim()) completed++;
    if (exp.company_name?.trim()) completed++;
    if (exp.start_date?.trim()) completed++;
    if (!exp.is_current && exp.end_date?.trim()) completed++;
    if (exp.is_current) completed++; 
    completed += exp.description.filter(desc => desc?.trim()).length;
    return acc + completed;
  }, 0);

  const completionPercentage =
    totalFields > 0 ? Math.round((completedFields / totalFields) * 100) : 0;

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-violet-600 rounded-2xl mx-auto mb-4">
          <Briefcase className="w-8 h-8 text-white" />
        </div>
        <div className="space-y-2">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
            Work Experience
          </h1>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Showcase your professional journey. Include internships, freelance
            work, and any relevant experience that demonstrates your skills.
          </p>
        </div>
      </div>

      {/* Progress Card */}
      <Card className="border-0 shadow-sm bg-gradient-to-r from-purple-50 to-violet-50 dark:from-purple-900/20 dark:to-violet-900/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              <span className="text-sm font-medium text-purple-700 dark:text-purple-300">
                Experience Completion
              </span>
            </div>
            <Badge
              variant="secondary"
              className="bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300"
            >
              {completionPercentage}%
            </Badge>
          </div>
          <div className="w-full bg-purple-100 dark:bg-purple-900/30 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-purple-500 to-violet-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
          {completionPercentage < 100 && (
            <p className="text-xs text-purple-600 dark:text-purple-400 mt-2">
              Complete all experience details to continue
            </p>
          )}
        </CardContent>
      </Card>

      {/* Tips Card */}
      <Card className="border-0 shadow-sm bg-gradient-to-r from-orange-50 to-amber-50 dark:from-orange-900/20 dark:to-amber-900/20">
        <CardContent className="p-6">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <Lightbulb className="w-4 h-4 text-orange-600 dark:text-orange-400" />
            </div>
            <div>
              <h3 className="font-semibold text-orange-900 dark:text-orange-100 mb-2">
                💼 Pro Tips for Experience Section
              </h3>
              <ul className="text-sm text-orange-700 dark:text-orange-300 space-y-1">
                <li>
                  • Use action verbs and quantify achievements where possible
                </li>
                <li>• Focus on accomplishments, not just job duties</li>
                <li>
                  • Include relevant internships, freelance, and volunteer work
                </li>
                <li>• List experience in reverse chronological order</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Form */}
      <FormProvider {...form}>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            {/* Experience Cards */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Work Experience ({fields.length})
                </h2>
                {fields.length > 1 && (
                  <Badge variant="outline" className="text-xs">
                    {fields.length}/10 records
                  </Badge>
                )}
              </div>

              {fields.map((field, index) => (
                <ExperienceCard
                  key={field.id}
                  index={index}
                  isExpanded={expandedIndexes.includes(index)}
                  toggleExpand={toggleExpand}
                  remove={remove}
                  canRemove={fields.length > 1}
                />
              ))}
            </div>

            {/* Add Another Experience Button */}
            <Card className="border-2 border-dashed border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-600 transition-colors">
              <CardContent className="p-6">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={addExperience}
                  disabled={fields.length >= 10}
                  className="w-full h-16 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 border-0 flex items-center gap-3"
                >
                  <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                    <Plus className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div className="text-left">
                    <p className="font-medium">Add Another Experience</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {fields.length >= 10
                        ? 'Maximum limit reached'
                        : 'Full-time, part-time, internships, freelance'}
                    </p>
                  </div>
                </Button>
              </CardContent>
            </Card>

            {/* Error Display */}
            {apiError && (
              <Card className="border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                    <p className="text-sm text-red-600 dark:text-red-400">
                      {apiError}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Submit Buttons */}
            <div className="pt-6 border-t border-gray-200 dark:border-gray-700 space-y-4">
              {fields.length > 0 && (
                <Button
                  type="submit"
                  disabled={
                    form.formState.isSubmitting || completionPercentage < 100
                  }
                  className="w-full h-12 text-base font-medium bg-gradient-to-r from-purple-600 to-violet-600 hover:from-purple-700 hover:to-violet-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
                >
                  {form.formState.isSubmitting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Saving Work Experience...
                    </>
                  ) : (
                    <>
                      Continue to Skills & Summary
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </Button>
              )}

              <Button
                type="button"
                onClick={skipExperience}
                disabled={form.formState.isSubmitting}
                variant="outline"
                className="w-full h-12 text-base font-medium border-2 border-gray-300 hover:border-gray-400 dark:border-gray-600 dark:hover:border-gray-500 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-200 flex items-center justify-center gap-2"
              >
                {fields.length === 0 ? (
                  <>
                    I&apos;m new to the workforce - Continue
                    <ArrowRight className="w-4 h-4" />
                  </>
                ) : (
                  <>
                    Skip for Now
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </Button>

              {fields.length > 0 && completionPercentage < 100 && (
                <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
                  Complete all experience details to save, or skip to continue
                </p>
              )}
            </div>
          </form>
        </Form>
      </FormProvider>
    </div>
  );
}
