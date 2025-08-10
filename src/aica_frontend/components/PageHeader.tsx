'use client';

import React from 'react';

interface PageHeaderProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  className?: string;
}

export default function PageHeader({
  icon,
  title,
  description,
  className = '',
}: PageHeaderProps) {
  return (
    <div className={`text-center mb-8 ${className}`}>
      <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
        {icon}
      </div>

      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        {title}
      </h1>

      <p className="text-gray-600 dark:text-gray-300 max-w-md mx-auto">
        {description}
      </p>
    </div>
  );
}
