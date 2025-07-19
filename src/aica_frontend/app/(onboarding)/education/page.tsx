'use client';

import EducationCard from '@/components/EducationCard';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import z from 'zod';

const educationItemSchema = z.object({
  institution_name: z.string().min(2, 'Institution name is required'), // TODO: Add institution validation
  address: z.string().min(2, 'Location is required'),
  degree: z.string().min(2, 'Degree is required'),
  field_of_study: z.string().optional(), // TODO: Tech education only
  start_date: z.string(),
  end_date: z.string(),
  description: z.string().optional(),
});

const educationFormSchema = z.object({
  educations: z
    .array(educationItemSchema)
    .min(1, 'At least one education is required'),
});

export default function Education() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
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

  async function onSubmit(values: z.infer<typeof educationFormSchema>) {
    setApiError(null);
    form.clearErrors();

    try {
      updateData({ educations: values.educations });
      router.push('/experience');
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
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

        <Button
          type="button"
          variant={'outline'}
          onClick={() =>
            append({
              institution_name: '',
              address: '',
              degree: '',
              field_of_study: '',
              start_date: '',
              end_date: '',
              description: '',
            })
          }
        >
          + Add Another Education
        </Button>

        {apiError && (
          <p className="text-sm font-medium text-destructive">{apiError}</p>
        )}

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Saving...' : 'Continue'}
        </Button>
      </form>
    </Form>
  );
}
