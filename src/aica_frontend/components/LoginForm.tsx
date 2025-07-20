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
} from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/context/AuthContext';
import { toast } from 'sonner';

const loginFormSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

export default function LoginForm() {
  const { login } = useAuth();
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
  const form = useForm<z.infer<typeof loginFormSchema>>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  async function loginOnSubmit(values: z.infer<typeof loginFormSchema>) {
    setApiError(null);

    try {
      await login(values.email, values.password);

      toast.success('Welcome back!', {
        description: `Successfully logged in as ${values.email}`,
      });

      setTimeout(() => {
        router.push('/dashboard');
      }, 500);
    } catch (error) {
      let errorMessage = 'Login failed. Please try again.';

      if (error instanceof Error) {
        const message = error.message.toLowerCase();
        if (
          message.includes('invalid credentials') ||
          message.includes('unauthorized')
        ) {
          errorMessage =
            'Invalid email or password. Please check your credentials and try again.';
        } else if (message.includes('network') || message.includes('fetch')) {
          errorMessage =
            'Network error. Please check your connection and try again.';
        } else if (message.includes('timeout')) {
          errorMessage = 'Request timed out. Please try again.';
        } else if (message.includes('email')) {
          errorMessage = 'Please enter a valid email address.';
        } else {
          errorMessage = error.message;
        }
      }

      // Show error toast with actionable message
      toast.error('Login Failed', {
        description: errorMessage,
        action: {
          label: 'Try Again',
          onClick: () => form.reset(),
        },
      });

      // Also set local error for persistent display
      setApiError(errorMessage);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(loginOnSubmit)} className="space-y-4">
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
                  placeholder="Enter your password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {apiError && (
          <p className="text-sm font-medium text-destructive">{apiError}</p>
        )}
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Logging in...' : 'Login'}
        </Button>
      </form>
    </Form>
  );
}
