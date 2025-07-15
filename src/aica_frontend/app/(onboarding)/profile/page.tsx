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
import {
  Select,
  SelectContent,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { apiClient } from '@/lib/api';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';

const profileFormSchema = z.object({
  first_name: z.string().min(2, 'First name is required'),
  last_name: z.string().min(2, 'Last name is required'),
  professional_title: z.string().min(2, 'Professional title is required'),
  contact_number: z.string().optional(),
  location: z.string().optional(),
  linkedin_url: z.string().url('Enter a valid LinkedIn URL').optional(),
});

export default function Profle() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<z.infer<typeof profileFormSchema>>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      professional_title: '',
      contact_number: '',
      location: '',
      linkedin_url: '',
    },
  });

  async function onSubmit(values: z.infer<typeof profileFormSchema>) {
    setApiError(null);

    try {
      const result = await apiClient.updateCurrentUserProfile(values);

      if (result) {
        router.push('/education');
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
          name="first_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>First Name</FormLabel>
              <FormControl>
                <Input placeholder="Juan" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="last_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Last Name</FormLabel>
              <FormControl>
                <Input placeholder="Dela Cruz" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        {/* TODO: Change it to a with options that uses api for tech */}
        <FormField
          control={form.control}
          name="professional_title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Professional Title</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue  />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  
                </SelectContent>
              </Select>
            </FormItem>
          )}
        />

        {/* TODO: Change it to a api phone number for all country */}
        <FormField
          control={form.control}
          name="contact_number"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Contact Number</FormLabel>
              <FormControl>
                <Input placeholder="e.g. +1234567890" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="location"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Address</FormLabel>
              <FormControl>
                <Input placeholder="e.g. Manila, Philippines" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="linkedin_url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>LinkedIn URL</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
            </FormItem>
          )}
        />

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
