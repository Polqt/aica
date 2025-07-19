'use client';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';
import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/style.css';
import Image from 'next/image';

const profileFormSchema = z.object({
  first_name: z.string().min(2, 'First name is required'),
  last_name: z.string().min(2, 'Last name is required'),
  professional_title: z.string().min(2, 'Professional title is required'),
  contact_number: z.string().min(7, 'Invalid contact number'),
  address: z.string().min(3, 'Address is required'),
  linkedin_url: z.string().url('Enter a valid LinkedIn URL').optional(),
  summary: z.string().min(20, 'Tell us a little more about you'),
  profile_picture: z.string().optional(),
});

const PROFESSIONAL_TITLES = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'UI/UX Designer',
  'Data Scientist',
  'DevOps Engineer',
];

export default function Profile() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
  const { updateData } = useOnboarding();

  const form = useForm<z.infer<typeof profileFormSchema>>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      professional_title: '',
      contact_number: '',
      address: '',
      linkedin_url: '',
      summary: '',
      profile_picture: '',
    },
  });

  async function onSubmit(values: z.infer<typeof profileFormSchema>) {
    setApiError(null);
    try {
      updateData(values);
      router.push('/education');
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unknown error');
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* First Name */}
        <FormField
          control={form.control}
          name="first_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>First Name</FormLabel>
              <FormControl>
                <Input placeholder="Juan" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Last Name */}
        <FormField
          control={form.control}
          name="last_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Last Name</FormLabel>
              <FormControl>
                <Input placeholder="Dela Cruz" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Professional Title */}
        <FormField
          control={form.control}
          name="professional_title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Professional Title</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your title" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {PROFESSIONAL_TITLES.map(title => (
                    <SelectItem key={title} value={title}>
                      {title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FormItem>
          )}
        />

        {/* Contact Number */}
        <FormField
          control={form.control}
          name="contact_number"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Contact Number</FormLabel>
              <FormControl>
                <PhoneInput
                  country={'ph'}
                  value={field.value}
                  onChange={field.onChange}
                  containerClass="!w-full"
                  inputClass="!w-full !bg-background !text-foreground !border-border"
                />
              </FormControl>
            </FormItem>
          )}
        />

        {/* Address */}
        <FormField
          control={form.control}
          name="address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Address</FormLabel>
              <FormControl>
                <Input placeholder="e.g. Manila, Philippines" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        {/* LinkedIn URL */}
        <FormField
          control={form.control}
          name="linkedin_url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>LinkedIn URL</FormLabel>
              <FormControl>
                <Input
                  placeholder="https://linkedin.com/in/your-profile"
                  {...field}
                />
              </FormControl>
            </FormItem>
          )}
        />

        {/* Summary */}
        <FormField
          control={form.control}
          name="summary"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Summary</FormLabel>
              <FormControl>
                <Textarea placeholder="Tell us about yourself..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        {/* Profile Picture */}
        <FormField
          control={form.control}
          name="profile_picture"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Profile Picture</FormLabel>
              <FormControl>
                <div className="space-y-2">
                  <Input
                    type="file"
                    accept="image/*"
                    onChange={async e => {
                      const file = e.target.files?.[0];
                      if (file) {
                        const reader = new FileReader();
                        reader.onloadend = () => {
                          const base64String = reader.result as string;
                          field.onChange(base64String);
                        };
                        reader.readAsDataURL(file);
                      }
                    }}
                  />
                  {field.value && (
                    <Image
                      src={field.value}
                      alt="Profile Picture"
                      width={100}
                      height={100}
                      className="rounded-full object-cover"
                    />
                  )}
                </div>
              </FormControl>
            </FormItem>
          )}
        />

        {/* Error Message */}
        {apiError && (
          <p className="text-sm font-medium text-destructive">{apiError}</p>
        )}

        {/* Submit Button */}
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Saving...' : 'Continue'}
        </Button>
      </form>
    </Form>
  );
}
