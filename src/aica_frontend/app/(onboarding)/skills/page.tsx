'use client';

import SkillsCard from '@/components/SkillsCard';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { FormProvider, useFieldArray, useForm } from 'react-hook-form';
import { toast } from 'sonner';
import z from 'zod';

const skillFormSchema = z.object({
  skills: z.array(
    z.object({
      name: z.string().min(1, 'Skill is required'),
    }),
  ),
});
export default function Skills() {
  const router = useRouter();
  const { updateData } = useOnboarding();
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<z.infer<typeof skillFormSchema>>({
    resolver: zodResolver(skillFormSchema),
    defaultValues: {
      skills: [{ name: '' }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'skills',
  });

  async function onSubmit(values: z.infer<typeof skillFormSchema>) {
    setApiError(null);
    form.clearErrors();

    try {
      const skillNames = values.skills.map(skill => skill.name);

      updateData({ skills: skillNames });
      toast.success('Skills saved successfully!');
      router.push('/certificate');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Unknown error';
      setApiError(errorMessage);
      toast.error('Failed to save skills', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => form.handleSubmit(onSubmit)(),
        },
      });
    }
  }

  return (
    <FormProvider {...form}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {fields.map((field, index) => (
            <SkillsCard
              key={field.id}
              index={index}
              remove={remove}
              canRemove={fields.length > 1}
            />
          ))}

          <Button
            type="button"
            variant="outline"
            onClick={() => append({ name: '' })}
          >
            + Add Another Skill
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
