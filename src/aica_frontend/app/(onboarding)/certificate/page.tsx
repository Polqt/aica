'use client';

import CertificateCard from '@/components/CertificateCard';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { FormProvider, useFieldArray, useForm } from 'react-hook-form';
import z from 'zod';
import { toast } from 'sonner';

const certificateItemSchema = z.object({
  name: z.string().optional(),
  issuing_organization: z.string().optional(),
  issue_date: z.string().optional(),
  credential_url: z
    .string()
    .optional()
    .refine(
      val => !val || val === '' || z.string().url().safeParse(val).success,
      {
        message: 'Invalid URL format',
      },
    ),
  credential_id: z.string().optional(),
});

const certificateFormSchema = z.object({
  certificates: z.array(certificateItemSchema),
});

export default function Certificate() {
  const router = useRouter();
  const { updateData, submitOnboardingData } = useOnboarding();
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
    setApiError(null);
    form.clearErrors();

    const validCertificates = values.certificates.filter(
      cert =>
        cert.name &&
        cert.name.trim() !== '' &&
        cert.issuing_organization &&
        cert.issuing_organization.trim() !== '',
    );

    updateData({ certificates: validCertificates });

    try {
      await submitOnboardingData();

      if (validCertificates.length > 0) {
        toast.success('Certificates Added!', {
          description: `Successfully added ${
            validCertificates.length
          } certificate${
            validCertificates.length > 1 ? 's' : ''
          } to your profile.`,
        });
      }

      setTimeout(() => {
        router.push('/dashboard');
      }, 500);
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : 'An unexpected error occurred. Please try again.';

      toast.error('Failed to Save Certificates', {
        description: errorMessage,
      });

      setApiError(errorMessage);
    }
  }

  return (
    <FormProvider {...form}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {fields.map((field, index) => (
            <CertificateCard
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
                name: '',
                issuing_organization: '',
                issue_date: '',
                credential_url: '',
                credential_id: '',
              })
            }
          >
            + Add Another Certificate
          </Button>

          {apiError && (
            <p className="text-sm font-medium text-destructive">{apiError}</p>
          )}

          <div className="flex flex-col gap-4">
            <div className="flex gap-4">
              <Button
                type="button"
                variant="outline"
                onClick={async () => {
                  updateData({ certificates: [] });
                  try {
                    await submitOnboardingData();
                    toast.success('Profile created successfully!', {
                      description:
                        'Welcome to AICA! You can add certificates later from your profile.',
                    });
                    router.push('/dashboard');
                  } catch (error) {
                    const errorMessage =
                      error instanceof Error
                        ? error.message
                        : 'An unexpected error occurred. Please try again.';
                    setApiError(errorMessage);
                    toast.error('Failed to complete profile', {
                      description: errorMessage,
                      action: {
                        label: 'Retry',
                        onClick: async () => {
                          try {
                            await submitOnboardingData();
                            router.push('/dashboard');
                          } catch {
                            // Silently handle retry errors
                          }
                        },
                      },
                    });
                  }
                }}
                disabled={form.formState.isSubmitting}
              >
                Skip Certificates
              </Button>

              <Button type="submit" disabled={form.formState.isSubmitting}>
                {form.formState.isSubmitting ? 'Saving...' : 'Submit'}
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Certificates are optional. You can skip this step and add them
              later.
            </p>
          </div>
        </form>
      </Form>
    </FormProvider>
  );
}
