import React from 'react';
import { Card, CardContent, CardHeader } from './ui/card';

export default function AuthWraper({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted">
      <Card className="w-full max-w-md shadow-md">
        <CardHeader>
          <h1 className="text-2xl font-semibold text-center">{title}</h1>
        </CardHeader>
        <CardContent>{children}</CardContent>
      </Card>
    </div>
  );
}
