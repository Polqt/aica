'use client';

import z from 'zod';
import React, { useState } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
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
} from 'lucide-react';
import { motion } from 'motion/react';
import AnimatedBackground from '@/components/AnimatedBackground';
import {
  computePercentage,
  showToastError,
  showToastInfo,
  showToastSuccess,
} from '@/lib/utils';

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
  const { updateData, submitOnboardingData } = useOnboarding();
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
      const cleanExperiences = JSON.parse(JSON.stringify(values.experiences));
      updateData({ experiences: cleanExperiences });

      const hasExperience = values.experiences.length > 0;

      showToastSuccess(
        hasExperience ? 'Work Experience Saved!' : 'Skipping Work Experience',
        hasExperience
          ? `Successfully added ${values.experiences.length} experience record${
              values.experiences.length > 1 ? 's' : ''
            }. Let's add your skills next.`
          : "No problem! You can always add work experience later. Let's continue with your skills.",
      );

      setTimeout(() => {
        router.push('/skills');
      }, 1000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';

      setApiError(errorMessage);
      showToastError('Experience Update Failed', errorMessage);
    }
  }

  const skipExperience = async () => {
    setApiError(null);
    try {
      updateData({ experiences: [] });
      await submitOnboardingData();
      showToastInfo(
        'Skipping Work Experience',
        'You can add experience later from your profile.',
      );
      router.push('/skills');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';
      setApiError(errorMessage);
    }
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
    totalFields > 0 ? computePercentage(completedFields, totalFields) : 100;

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/40 to-purple-50/30 dark:from-slate-900 dark:via-blue-900/20 dark:to-purple-900/15 py-8 px-4 overflow-hidden">
      <AnimatedBackground />
      <div className="max-w-4xl mx-auto">
        {/* Enhanced Header Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.8, type: 'spring', stiffness: 200 }}
            className="relative inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-6 shadow-xl"
          >
            <Briefcase className="w-12 h-12 text-white" />
            <div className="absolute -inset-2 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-2xl blur-lg animate-pulse"></div>
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 dark:from-white dark:to-slate-200 bg-clip-text text-transparent mb-4"
          >
            Work{' '}
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 dark:from-blue-300 dark:via-purple-300 dark:to-indigo-300 bg-clip-text text-transparent">
              Experience
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg text-slate-600 dark:text-slate-300 max-w-md mx-auto leading-relaxed"
          >
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent font-semibold">
              Showcase your professional journey
            </span>{' '}
            — this information helps us match you with perfect opportunities
          </motion.p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="border-0 shadow-xl bg-white dark:bg-slate-800 overflow-hidden">
            <CardContent className="p-8">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="space-y-8"
                >
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
                    <div className="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                      <p className="text-sm text-red-600 dark:text-red-400">
                        {apiError}
                      </p>
                    </div>
                  )}

                  <div className="pt-6 border-t border-slate-200/60 dark:border-slate-700/50 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={skipExperience}
                      disabled={form.formState.isSubmitting}
                    >
                      Skip Experience
                    </Button>
                    <Button
                      type="submit"
                      disabled={
                        form.formState.isSubmitting ||
                        fields.length === 0 ||
                        completionPercentage < 100
                      }
                      className="w-full h-14 text-base font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 dark:disabled:from-slate-600 dark:disabled:to-slate-700 transition-all duration-300 flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
                    >
                      {form.formState.isSubmitting ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      ) : (
                        <>
                          Continue to Skills & Summary
                          <ArrowRight className="w-5 h-5" />
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
