'use client';

import z from 'zod';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
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
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/lib/context/AuthContext';
import { toast } from 'sonner';

const registerFormSchema = z
  .object({
    email: z.string().email('Please enter a valid email address'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters long')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number')
      .regex(
        /[!@#$%^&*(),.?":{}|<>]/,
        'Password must contain at least one special character',
      ),
    confirmPassword: z.string().min(1, 'Please confirm your password'),
  })
  .refine(data => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'],
  });

export default function RegisterForm() {
  const router = useRouter();
  const { setAuthToken } = useAuth();
  const [apiError, setApiError] = useState<string | null>(null);

  const form = useForm<z.infer<typeof registerFormSchema>>({
    resolver: zodResolver(registerFormSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  async function registerOnSubmit(values: z.infer<typeof registerFormSchema>) {
    setApiError(null);
    try {
      const tokenData = await apiClient.register({
        email: values.email,
        password: values.password,
      });

      if (tokenData.access_token) {
        setAuthToken(tokenData.access_token);

        toast.success('Welcome to AICA!', {
          description: `Account created for ${values.email}. Let's complete your profile to get started.`,
        });

        setTimeout(() => {
          router.push('/profile');
        }, 500);
      } else {
        throw new Error('Registration failed. Please try again.');
      }
    } catch (error) {
      let errorMessage = 'Registration failed. Please try again.';

      if (error instanceof Error) {
        const message = error.message.toLowerCase();
        if (
          message.includes('already exists') ||
          message.includes('duplicate')
        ) {
          errorMessage =
            'An account with this email already exists. Please try logging in instead.';
        } else if (message.includes('network') || message.includes('fetch')) {
          errorMessage =
            'Network error. Please check your connection and try again.';
        } else if (message.includes('timeout')) {
          errorMessage = 'Request timed out. Please try again.';
        } else if (message.includes('email')) {
          errorMessage = 'Please enter a valid email address.';
        } else if (message.includes('password')) {
          errorMessage =
            'Password requirements not met. Please check the requirements above.';
        } else {
          errorMessage = error.message;
        }
      }

      toast.error('Registration Failed', {
        description: errorMessage,
        action: errorMessage.includes('already exists')
          ? {
              label: 'Go to Login',
              onClick: () => router.push('/login'),
            }
          : {
              label: 'Try Again',
              onClick: () => form.reset(),
            },
      });
      setApiError(errorMessage);
    }
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(registerOnSubmit)}
        className="space-y-4"
      >
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
                  placeholder="Enter a strong password"
                  {...field}
                />
              </FormControl>
              <FormDescription className="text-xs">
                Password must contain at least 8 characters with uppercase,
                lowercase, and number
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
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {apiError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
            <p className="text-sm font-medium">{apiError}</p>
          </div>
        )}
        <Button
          type="submit"
          disabled={form.formState.isSubmitting}
          className="w-full"
        >
          {form.formState.isSubmitting
            ? 'Creating Account...'
            : 'Create Account'}
        </Button>
      </form>
    </Form>
  );
}
