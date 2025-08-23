'use client';

import EducationCard from '@/components/EducationCard';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import z from 'zod';
import { toast } from 'sonner';
import {
  Plus,
  GraduationCap,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Lightbulb,
} from 'lucide-react';

const educationItemSchema = z.object({
  institution_name: z
    .string()
    .min(2, 'Institution name must be at least 2 characters')
    .max(100, 'Institution name must be less than 100 characters'),
  address: z
    .string()
    .min(2, 'Location must be at least 2 characters')
    .max(100, 'Location must be less than 100 characters'),
  degree: z
    .string()
    .min(2, 'Degree must be at least 2 characters')
    .max(100, 'Degree must be less than 100 characters'),
  field_of_study: z
    .string()
    .max(100, 'Field of study must be less than 100 characters')
    .optional(),
  start_date: z.string().min(1, 'Start date is required'),
  end_date: z.string().min(1, 'End date is required'),
  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
});

const educationFormSchema = z.object({
  educations: z
    .array(educationItemSchema)
    .min(1, 'At least one education record is required')
    .max(5, 'Maximum 5 education records allowed'),
});

export default function Education() {
  const router = useRouter();
  const { updateData } = useOnboarding();
  const [expandedIndexes, setExpandedIndexes] = useState<number[]>([0]);

  const form = useForm<z.infer<typeof educationFormSchema>>({
    resolver: zodResolver(educationFormSchema),
    defaultValues: {
      educations: [
        {
          institution_name: '',
          address: '',
          degree: '',
          field_of_study: '',
          start_date: '',
          end_date: '',
          description: '',
        },
      ],
    },
    mode: 'onBlur',
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'educations',
  });

  const toggleExpand = (index: number) => {
    setExpandedIndexes(prev =>
      prev.includes(index) ? prev.filter(i => i !== index) : [...prev, index],
    );
  };

  const addEducation = () => {
    if (fields.length >= 5) {
      toast.error('Maximum limit reached', {
        description: 'You can add up to 5 education records only.',
      });
      return;
    }

    append({
      institution_name: '',
      address: '',
      degree: '',
      field_of_study: '',
      start_date: '',
      end_date: '',
      description: '',
    });

    // Expand the newly added education card
    setExpandedIndexes(prev => [...prev, fields.length]);

    toast.success('New education record added!', {
      description: 'Fill in the details for your new education record.',
    });
  };

  async function onSubmit(values: z.infer<typeof educationFormSchema>) {
    try {
      updateData({ educations: values.educations });

      toast.success('Education Records Saved!', {
        description: `Successfully added ${
          values.educations.length
        } education record${
          values.educations.length > 1 ? 's' : ''
        }. Let's add your work experience next.`,
        duration: 3000,
      });

      setTimeout(() => {
        router.push('/experience');
      }, 1000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';

      toast.error('Education Update Failed', {
        description: errorMessage,
        duration: 5000,
      });
    }
  }

  const watchedEducations = form.watch('educations');
  const totalFields = watchedEducations.length * 6; 
  const completedFields = watchedEducations.reduce((acc, edu) => {
    let completed = 0;
    if (edu.institution_name?.trim()) completed++;
    if (edu.address?.trim()) completed++;
    if (edu.degree?.trim()) completed++;
    if (edu.start_date?.trim()) completed++;
    if (edu.end_date?.trim()) completed++;
    if (edu.field_of_study?.trim()) completed++;
    return acc + completed;
  }, 0);
  const completionPercentage =
    totalFields > 0 ? Math.round((completedFields / totalFields) * 100) : 0;

  return (
<div className="space-y-8 bg-gradient-to-br from-slate-50 via-blue-50/40 to-purple-50/30 dark:from-slate-900 dark:via-blue-900/20 dark:to-purple-900/15">
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mx-auto mb-4">
          <GraduationCap className="w-8 h-8 text-white" />
        </div>
        <div className="space-y-2">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
            Educational Background
          </h1>
          <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Share your educational journey. Include universities, colleges,
            bootcamps, or any formal learning that shaped your career.
          </p>
        </div>
      </div>

      {/* Tips Card */}
      <Card className="border-0 shadow-sm bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
        <CardContent className="p-6">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <Lightbulb className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">
                💡 Pro Tips for Education Section
              </h3>
              <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
                <li>
                  • Include relevant coursework, projects, or thesis topics
                </li>
                <li>• Add online courses, bootcamps, and certifications</li>
                <li>
                  • Mention academic achievements, honors, or GPA if impressive
                </li>
                <li>
                  • List education in reverse chronological order (most recent
                  first)
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Form */}
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {/* Education Cards */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                Education Records ({fields.length})
              </h2>
              {fields.length > 1 && (
                <Badge variant="outline" className="text-xs">
                  {fields.length}/5 records
                </Badge>
              )}
            </div>

            {fields.map((field, index) => (
              <EducationCard
                key={field.id}
                index={index}
                isExpanded={expandedIndexes.includes(index)}
                toggleExpand={toggleExpand}
                remove={remove}
                canRemove={fields.length > 1}
              />
            ))}
          </div>

          {/* Add Another Education Button */}
          <Card className="border-2 border-dashed border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
            <CardContent className="p-6">
<Button
                type="button"
                variant="ghost"
                onClick={addEducation}
                disabled={fields.length >= 5}
                className="w-full h-16 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 border-0 flex items-center gap-3"
              >
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  <Plus className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="text-left">
                  <p className="font-medium">Add Another Education</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {fields.length >= 5
                      ? 'Maximum limit reached'
                      : 'Universities, colleges, bootcamps, etc.'}
                  </p>
                </div>
              </Button>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
            <Button
              type="submit"
              disabled={
                form.formState.isSubmitting || completionPercentage < 100
              }
              className="w-full h-12 text-base font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            >
              {form.formState.isSubmitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Saving Education Records...
                </>
              ) : (
                <>
                  Continue to Work Experience
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </Button>
            {completionPercentage < 100 && (
              <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
                Please complete all education details to continue
              </p>
            )}
          </div>
        </form>
      </Form>
    </div>
  );
}
