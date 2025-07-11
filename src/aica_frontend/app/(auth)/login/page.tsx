import AuthWraper from '@/components/AuthWraper';
import LoginForm from '@/components/LoginForm';
import Link from 'next/link';
import React from 'react';

export default function LoginPage() {
  return (
    <AuthWraper title='Login to Aica'>
      <LoginForm />
      <hr />
      <p className="text-sm text-center mt-4">
        Don’t have an account?{" "}
        <Link href="/sign-up" className="text-primary underline hover:opacity-80">Sign up</Link>
      </p>
    </AuthWraper>
  );
}
