'use client';

import { Form } from '@/components/ui/form';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { FormProvider, useFieldArray, useForm } from 'react-hook-form';
import z from 'zod';

const certificateItemSchema = z.object({
  name: z.string().min(1, 'Certificate name is required'),
  issuing_organization: z.string().min(1, 'Issuing organization is required'),
  issue_date: z.string().optional(),
  credential_url: z.string().url('Invalid URL format').optional(),
  credential_id: z.string().min(1, 'Credential ID is required'),
});

const certificateFormSchema = z.object({
  certificates: z.array(certificateItemSchema),
});

export default function Certificate() {
  const router = useRouter();
  const { updateData } = useOnboarding();
  const [apiError, setApiError] = useState<string | null>(null);
  const [expandedIndexes, setExpandedIndexes] = useState<number[]>([0]);

  const form = useForm<z.infer<typeof certificateFormSchema>>({
    resolver: zodResolver(certificateFormSchema),
    defaultValues: {
      certificates: [
        {
          name: '',
          issuing_organization: '',
          issue_date: '',
          credential_url: '',
          credential_id: '',
        },
      ],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'certificates',
  });

  const toggleExpand = (index: number) => {
    setExpandedIndexes(prev =>
      prev.includes(index) ? prev.filter(i => i !== index) : [...prev, index],
    );
  };

  async function onSubmit(values: z.infer<typeof certificateFormSchema>) {
    try {
      updateData({ certificates: values.certificates });
      router.push('/dashboard');
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }
  return (
    <FormProvider {...form}>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-6"
        >
            
        </form>
      </Form>
    </FormProvider>
  );
}
