'use client';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { apiClient } from '@/lib/api';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';

const educationFormSchema = z.object({
  institution_name: z.string().min(2, 'Institution name is required'), // TODO: Add institution validation
  degree: z.string().min(2, 'Degree is required'), // TODO: Tech education only
  field_of_study: z.string().min(2, 'Field of study is required'),
  start_date: z.string(),
  end_date: z.string().optional(),
});

export default function Education() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<z.infer<typeof educationFormSchema>>({
    resolver: zodResolver(educationFormSchema),
    defaultValues: {
      institution_name: '',
      degree: '',
      field_of_study: '',
      start_date: '',
      end_date: '',
    },
  });

  async function onSubmit(values: z.infer<typeof educationFormSchema>) {
    setApiError(null);

    try {
      const result = await apiClient.updateCurrentUserProfile({
        educations: [values],
      });

      if (result) {
        router.push('/experience');
      }
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="institution_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Institution Name</FormLabel>
              <FormControl>
                <Input placeholder="USLS - Bacolod" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="degree"
          render={({ field }) => (
            <FormItem>
              <FormLabel></FormLabel>
              <FormControl>
                <Input placeholder="" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="field_of_study"
          render={({ field }) => (
            <FormItem>
              <FormLabel></FormLabel>
              <FormControl>
                <Input placeholder="" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        {/* TODO: Add the forms later */}

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
