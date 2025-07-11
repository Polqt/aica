import AuthWraper from '@/components/AuthWraper';
import RegisterForm from '@/components/RegisterForm';
import Link from 'next/link';
import React from 'react';

export default function SignupPage() {
  return (
    <AuthWraper title="Login to Aica">
      <RegisterForm />
      <hr />
      <p className="text-sm text-center mt-4">
        Already have an account?{' '}
        <Link href="/login" className="text-primary underline hover:opacity-80">
          Log in
        </Link>
      </p>
    </AuthWraper>
  );
}
