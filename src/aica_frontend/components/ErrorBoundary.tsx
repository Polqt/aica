'use client';

import React from 'react';
import { Button } from '@/components/ui/button';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  {
    children: React.ReactNode;
    fallback?: React.ComponentType<{ error: Error; reset: () => void }>;
  },
  ErrorBoundaryState
> {
  constructor(props: {
    children: React.ReactNode;
    fallback?: React.ComponentType<{ error: Error; reset: () => void }>;
  }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      const Fallback = this.props.fallback || DefaultErrorFallback;
      return (
        <Fallback
          error={this.state.error!}
          reset={() => this.setState({ hasError: false })}
        />
      );
    }

    return this.props.children;
  }
}

const DefaultErrorFallback = ({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) => (
  <div className="min-h-screen flex items-center justify-center bg-muted">
    <div className="text-center p-6 max-w-md">
      <h2 className="text-2xl font-bold text-destructive mb-4">
        Something went wrong
      </h2>
      <p className="text-muted-foreground mb-4">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  </div>
);
