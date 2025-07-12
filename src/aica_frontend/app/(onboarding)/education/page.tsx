'use client';

import apiClient from '@/lib/api';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';

const educationFormSchema = z.object({
  institution_name: z.string().min(2, 'Institution name is required'), // TODO: Add institution validation
  degree: z.string().min(2, 'Degree is required'), // TODO: Tech education only
  field_of_study: z.string().min(2, 'Field of study is required'),
  start_date: z.string().optional(), // TODO: Add date validation
  end_date: z.string().optional(), // TODO: Add date validation
})

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
    }
  })

  async function onSubmit(values: z.infer<typeof educationFormSchema>) {
    setApiError(null);

    try {
      const result = await apiClient.updateCurrentUserProfile(values);

      
      
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  return <div>Education</div>;
}
