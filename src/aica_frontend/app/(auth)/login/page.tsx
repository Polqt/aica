'use client';

import { motion } from 'motion/react';
import Link from 'next/link';
import React from 'react';
import LoginForm from '@/components/LoginForm';
import AuthLayout from '@/components/AuthLayout';

export default function LoginPage() {
  return (
    <AuthLayout
      title="Welcome to AICA"
      subtitle="AI Career Assistant - Your Path to Success"
      backgroundPattern="login"
    >
      <LoginForm />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mt-6 pt-6 border-t border-slate-200/50 dark:border-slate-700/50"
      >
        <p className="text-sm text-center text-slate-600 dark:text-slate-300">
          Don&apos;t have an account?{" "}
          <Link href="/sign-up" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
            Sign up here
          </Link>
        </p>
      </motion.div>
    </AuthLayout>
  );
}
