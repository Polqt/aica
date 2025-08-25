'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { apiClient } from '@/lib/services/api-client';
import { useFormSubmission } from '@/lib/hooks/useFormWithValidation';
import { registerSchema, RegisterFormData } from '@/lib/schemas/validation';
import { useAuth } from '@/lib/context/AuthContext';

export default function RegisterForm() {
  const router = useRouter();
  const { setUser } = useAuth();

  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
    mode: 'onChange',
  });

  const { handleSubmit, isSubmitting, apiError, clearApiError } =
    useFormSubmission<RegisterFormData>({
      onSubmit: async data => {
        clearApiError();

        try {
          const authResponse = await apiClient.auth.register({
            email: data.email,
            password: data.password,
          });

          console.log('Registration successful:', authResponse);

          await setUser(authResponse);
          router.push('/profile');
        } catch (error) {
          console.error('Registration error: ', error)
          throw error;
        }
      },
      successMessage: 'Account created successfully! Welcome to AICA.',
      errorMessage: 'Failed to create account. Please try again.',
    });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  id="email"
                  type="email"
                  placeholder="aica@example.com"
                  {...field}
                  disabled={isSubmitting}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  {...field}
                  disabled={isSubmitting}
                />
              </FormControl>
              <FormDescription className="text-xs">
                Password must contain at least 8 characters with uppercase,
                lowercase, number, and special character
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="confirmPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Confirm Password</FormLabel>
              <FormControl>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm your password"
                  {...field}
                  disabled={isSubmitting}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {apiError && (
          <div className="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
            <div className="text-sm text-red-700 dark:text-red-300">
              {apiError}
            </div>
          </div>
        )}

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Creating Account...' : 'Create Account'}
        </Button>
      </form>
    </Form>
  );
}
