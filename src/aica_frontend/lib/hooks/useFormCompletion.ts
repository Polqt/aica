import { useMemo } from 'react';

interface UseFormCompletionProps<T extends Record<string, unknown>> {
  data: T;
  requiredFields: (keyof T)[];
  optionalFields?: (keyof T)[];
}

interface FormCompletion {
  completionPercentage: number;
  completedCount: number;
  totalCount: number;
  isComplete: boolean;
  missingRequired: string[];
}

export function useFormCompletion<T extends Record<string, unknown>>({
  data,
  requiredFields,
  optionalFields = [],
}: UseFormCompletionProps<T>): FormCompletion {
  return useMemo(() => {
    const allFields = [...requiredFields, ...optionalFields];

    let completedCount = 0;
    const missingRequired: string[] = [];

    for (const field of allFields) {
      const value = data[field];
      const isCompleted = isFieldCompleted(value);

      if (isCompleted) {
        completedCount++;
      } else if (requiredFields.includes(field)) {
        missingRequired.push(String(field));
      }
    }

    const totalCount = allFields.length;
    const completionPercentage =
      totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
    const isComplete = missingRequired.length === 0;

    return {
      completionPercentage,
      completedCount,
      totalCount,
      isComplete,
      missingRequired,
    };
  }, [data, requiredFields, optionalFields]);
}

function isFieldCompleted(value: unknown): boolean {
  if (value === null || value === undefined) {
    return false;
  }

  if (typeof value === 'string') {
    return value.trim().length > 0;
  }

  if (Array.isArray(value)) {
    return value.length > 0;
  }

  if (typeof value === 'object') {
    return Object.keys(value).length > 0;
  }

  return Boolean(value);
}

interface UseArrayFormCompletionProps<T extends Record<string, unknown>> {
  items: T[];
  requiredFieldsPerItem: (keyof T)[];
}

export function useArrayFormCompletion<T extends Record<string, unknown>>({
  items,
  requiredFieldsPerItem,
}: UseArrayFormCompletionProps<T>): FormCompletion {
  return useMemo(() => {
    if (items.length === 0) {
      return {
        completionPercentage: 0,
        completedCount: 0,
        totalCount: 0,
        isComplete: false,
        missingRequired: [],
      };
    }

    let completedItems = 0;
    const missingRequired: string[] = [];

    items.forEach((item, index) => {
      let itemCompleted = true;
      const itemMissing: string[] = [];

      for (const field of requiredFieldsPerItem) {
        const value = (item as Record<string, unknown>)[field as string];
        if (!isFieldCompleted(value)) {
          itemCompleted = false;
          itemMissing.push(String(field));
        }
      }

      if (itemCompleted) {
        completedItems++;
      } else {
        missingRequired.push(`Item ${index + 1}: ${itemMissing.join(', ')}`);
      }
    });

    const completionPercentage = Math.round(
      (completedItems / items.length) * 100,
    );
    const isComplete = completedItems === items.length;

    return {
      completionPercentage,
      completedCount: completedItems,
      totalCount: items.length,
      isComplete,
      missingRequired,
    };
  }, [items, requiredFieldsPerItem]);
}
