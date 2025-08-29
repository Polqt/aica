'use client';

import { motion } from 'motion/react';
import Link from 'next/link';
import React from 'react';
import RegisterForm from '@/components/RegisterForm';
import AuthLayout from '@/components/AuthLayout';

export default function SignupPage() {
  return (
    <AuthLayout
      title="Join AICA"
      subtitle="Create your account to get started"
      backgroundPattern="signup"
    >
      <RegisterForm />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-700"
      >
        <p className="text-sm text-center text-slate-600 dark:text-slate-300">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
            Log in here
          </Link>
        </p>
      </motion.div>
    </AuthLayout>
  );
}
