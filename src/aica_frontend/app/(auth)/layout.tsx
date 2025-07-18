import { AuthProvider } from '@/lib/context/AuthContext';
import { Toaster } from 'sonner';

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <AuthProvider>
      <Toaster />
      {children}
    </AuthProvider>
  );
}
