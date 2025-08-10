'use client';

import React from 'react';
import { Progress } from './ui/progress';
import { Card, CardContent } from './ui/card';

interface ProgressIndicatorProps {
  completedFields: number;
  totalFields: number;
  label?: string;
}

export default function ProgressIndicator({
  completedFields,
  totalFields,
  label = 'Profile Completion',
}: ProgressIndicatorProps) {
  const percentage = Math.round((completedFields / totalFields) * 100);
  const isComplete = percentage >= 100;

  return (
    <Card className="mb-6 border-0 shadow-sm bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
      <CardContent className="pt-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {label}
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {percentage}%
          </span>
        </div>

        <Progress value={percentage} className="w-full h-2" />

        {!isComplete && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Complete all required fields to continue
          </p>
        )}

        {isComplete && (
          <p className="text-xs text-green-600 dark:text-green-400 mt-2">
            Profile is complete! You can now continue.
          </p>
        )}
      </CardContent>
    </Card>
  );
}
