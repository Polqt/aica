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
} from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { useFormSubmission } from '@/lib/hooks/useFormWithValidation';
import { loginSchema, LoginFormData } from '@/lib/schemas/validation';
import { useAuth } from '@/lib/context/AuthContext';

export default function LoginForm() {
  const { login } = useAuth();
  const router = useRouter();

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
    mode: 'onChange',
  });

  const { handleSubmit, isSubmitting, apiError, clearApiError } =
    useFormSubmission<LoginFormData>({
      onSubmit: async data => {
        clearApiError();
        await login(data.email, data.password);
        // Dev fallback: persist access token from cookie to localStorage
        try {
          const cookie = document.cookie
            .split('; ')
            .find(r => r.startsWith('access_token='))
            ?.split('=')[1];
          if (cookie) {
            const token = cookie.startsWith('Bearer ')
              ? cookie.substring(7)
              : cookie;
            localStorage.setItem('access_token', token);
          }
        } catch {}
        router.push('/dashboard');
      },
      successMessage: 'Welcome back! Successfully logged in.',
      errorMessage: 'Login failed. Please check your credentials.',
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
          {isSubmitting ? 'Signing In...' : 'Sign In'}
        </Button>
      </form>
    </Form>
  );
}
