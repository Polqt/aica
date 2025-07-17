'use client';

import z from 'zod';
import React, { useState } from 'react';
import { useForm, FormProvider, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';

import { Form } from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import ExperienceCard from '@/components/ExperienceCard';

const experienceItemSchema = z.object({
  job_title: z.string(),
  company_name: z.string().min(2, 'Company name is required'),
  start_date: z.string().min(1, 'Start date is required'),
  end_date: z.string(),
  description: z
    .array(z.string())
    .min(1, 'At least one description is required'),
  is_current: z.boolean(),
});

const experienceFormSchema = z.object({
  experiences: z.array(experienceItemSchema),
});

export default function Experience() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
  const { updateData } = useOnboarding();
  const [expandedIndexes, setExpandedIndexes] = useState<number[]>([0]);

  const form = useForm<z.infer<typeof experienceFormSchema>>({
    resolver: zodResolver(experienceFormSchema),
    defaultValues: {
      experiences: [
        {
          job_title: '',
          company_name: '',
          start_date: '',
          end_date: '',
          description: [''],
          is_current: false,
        },
      ],
    },
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

  async function onSubmit(values: z.infer<typeof experienceFormSchema>) {
    try {
      await updateData({ experiences: values.experiences });
      router.push('/skills');
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  return (
    <FormProvider {...form}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
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

          <Button
            type="button"
            variant="outline"
            onClick={() =>
              append({
                job_title: '',
                company_name: '',
                start_date: '',
                end_date: '',
                description: [''],
                is_current: false,
              })
            }
          >
            + Add Another Experience
          </Button>

          {apiError && (
            <p className="text-sm font-medium text-destructive">{apiError}</p>
          )}

          <Button type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? 'Saving...' : 'Continue'}
          </Button>
        </form>
      </Form>
    </FormProvider>
  );
}
