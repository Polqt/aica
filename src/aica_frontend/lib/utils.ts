import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { toast } from 'sonner';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function computePercentage(completed: number, total: number): number {
  if (total <= 0) return 0;
  const percentage = Math.round((completed / total) * 100);
  return Math.max(0, Math.min(100, percentage));
}

export function showToastSuccess(
  title: string,
  description?: string,
  duration = 3000,
) {
  toast.success(title, { description, duration });
}

export function showToastError(
  title: string,
  description?: string,
  duration = 5000,
) {
  toast.error(title, { description, duration });
}

export function showToastInfo(
  title: string,
  description?: string,
  duration = 3000,
) {
  toast.info(title, { description, duration });
}
