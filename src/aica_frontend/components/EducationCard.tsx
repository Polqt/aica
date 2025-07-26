'use client';

import {
  ChevronDown,
  ChevronUp,
  School,
  MapPin,
  Calendar,
  BookOpen,
  Trash2,
  AlertCircle,
  CheckCircle2,
  GraduationCap,
} from 'lucide-react';
import React from 'react';
import { useFormContext } from 'react-hook-form';
import { toast } from 'sonner';
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader } from './ui/card';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
import { cn } from '@/lib/utils';

type EducationCardProps = {
  index: number;
  isExpanded: boolean;
  toggleExpand: (index: number) => void;
  remove: (index: number) => void;
  canRemove: boolean;
};

const DEGREE_SUGGESTIONS = [
  "Bachelor's Degree",
  "Master's Degree",
  'Associate Degree',
  'Doctorate/PhD',
  'High School Diploma',
  'Certificate Program',
  'Bootcamp Certificate',
  'Professional Certificate',
];

const FIELD_SUGGESTIONS = [
  'Computer Science',
  'Information Technology',
  'Software Engineering',
  'Data Science',
  'Computer Engineering',
  'Information Systems',
  'Cybersecurity',
  'Web Development',
  'Mobile Development',
  'DevOps',
];

export default function EducationCard({
  index,
  isExpanded,
  toggleExpand,
  remove,
  canRemove,
}: EducationCardProps) {
  const { control, watch, formState } = useFormContext();

  // Watch field values for dynamic display
  const institution = watch(`educations.${index}.institution_name`);
  const location = watch(`educations.${index}.address`);
  const degree = watch(`educations.${index}.degree`);
  const startDate = watch(`educations.${index}.start_date`);
  const endDate = watch(`educations.${index}.end_date`);

  const requiredFields = [institution, location, degree, startDate, endDate];
  const completedFields = requiredFields.filter(
    field => field && field.trim() !== '',
  ).length;
  const isComplete = completedFields === requiredFields.length;
  const completionPercentage = Math.round(
    (completedFields / requiredFields.length) * 100,
  );

  const educationErrors = formState.errors?.educations;
  const hasErrors =
    educationErrors && Array.isArray(educationErrors)
      ? (educationErrors[index] as
          | Record<string, { message?: string }>
          | undefined)
      : undefined;

  const handleRemove = () => {
    toast('Remove Education Record?', {
      description:
        'This action cannot be undone. The education record will be permanently deleted.',
      action: {
        label: 'Remove',
        onClick: () => {
          remove(index);
          toast.success('Education record removed successfully');
        },
      },
      cancel: {
        label: 'Cancel',
        onClick: () => {
          // No action needed, toast will close
        },
      },
    });
  };

  return (
    <Card
      className={cn(
        'group transition-all duration-300 hover:shadow-lg border border-gray-200 dark:border-gray-700',
        isExpanded
          ? 'shadow-lg ring-2 ring-emerald-500/20 dark:ring-emerald-400/20'
          : 'hover:border-emerald-300 dark:hover:border-emerald-600',
        hasErrors &&
          'border-red-300 dark:border-red-600 bg-red-50/50 dark:bg-red-900/10',
      )}
    >
      <CardHeader
        className="cursor-pointer"
        onClick={() => toggleExpand(index)}
      >
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3">
              <div
                className={cn(
                  'flex items-center justify-center w-10 h-10 rounded-full transition-colors duration-200',
                  isComplete
                    ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'
                    : hasErrors
                    ? 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400',
                )}
              >
                {isComplete ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : hasErrors ? (
                  <AlertCircle className="w-5 h-5" />
                ) : (
                  <GraduationCap className="w-5 h-5" />
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">
                    {institution || `Education ${index + 1}`}
                  </h3>
                  {isComplete && (
                    <Badge
                      variant="outline"
                      className="text-emerald-600 dark:text-emerald-400 border-emerald-300 dark:border-emerald-600"
                    >
                      Complete
                    </Badge>
                  )}
                  {hasErrors && (
                    <Badge variant="destructive" className="text-xs">
                      {Object.keys(hasErrors).length} Error
                      {Object.keys(hasErrors).length > 1 ? 's' : ''}
                    </Badge>
                  )}
                </div>

                {(degree || location) && (
                  <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                    {degree && (
                      <div className="flex items-center gap-1">
                        <BookOpen className="w-4 h-4" />
                        <span className="truncate">{degree}</span>
                      </div>
                    )}
                    {location && (
                      <div className="flex items-center gap-1">
                        <MapPin className="w-4 h-4" />
                        <span className="truncate">{location}</span>
                      </div>
                    )}
                  </div>
                )}

                {(startDate || endDate) && (
                  <div className="flex items-center gap-1 mt-1 text-sm text-gray-500 dark:text-gray-400">
                    <Calendar className="w-4 h-4" />
                    <span>
                      {startDate
                        ? new Date(startDate).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                          })
                        : 'Start Date'}{' '}
                      -{' '}
                      {endDate
                        ? new Date(endDate).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                          })
                        : 'End Date'}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {!isComplete && (
              <div className="mt-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    Completion: {completionPercentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                  <div
                    className="bg-gradient-to-r from-emerald-500 to-teal-600 h-1 rounded-full transition-all duration-300"
                    style={{ width: `${completionPercentage}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center gap-2">
            {canRemove && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={e => {
                  e.stopPropagation();
                  handleRemove();
                }}
                className="text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 p-2"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            )}
            <Button type="button" variant="ghost" size="sm" className="p-2">
              {isExpanded ? (
                <ChevronUp className="w-4 h-4" />
              ) : (
                <ChevronDown className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="pt-0">
          <div className="space-y-6">
            {/* Institution Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`educations.${index}.institution_name`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <School className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      Institution Name *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., University of the Philippines"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name={`educations.${index}.address`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      Location *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Quezon City, Philippines"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Degree Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`educations.${index}.degree`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <GraduationCap className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      Degree *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Bachelor of Science"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                        list={`degree-suggestions-${index}`}
                      />
                    </FormControl>
                    <datalist id={`degree-suggestions-${index}`}>
                      {DEGREE_SUGGESTIONS.map(suggestion => (
                        <option key={suggestion} value={suggestion} />
                      ))}
                    </datalist>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name={`educations.${index}.field_of_study`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      Field of Study
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Computer Science"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                        list={`field-suggestions-${index}`}
                      />
                    </FormControl>
                    <datalist id={`field-suggestions-${index}`}>
                      {FIELD_SUGGESTIONS.map(suggestion => (
                        <option key={suggestion} value={suggestion} />
                      ))}
                    </datalist>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`educations.${index}.start_date`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      Start Date *
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name={`educations.${index}.end_date`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      End Date *
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Description */}
            <FormField
              control={control}
              name={`educations.${index}.description`}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description (Optional)</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Describe relevant coursework, projects, achievements, GPA, honors, etc..."
                      {...field}
                      className="min-h-[100px] border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all resize-none"
                      maxLength={500}
                    />
                  </FormControl>
                  <div className="flex justify-between items-center">
                    <FormMessage className="text-xs" />
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {field.value?.length || 0}/500
                    </span>
                  </div>
                </FormItem>
              )}
            />
          </div>
        </CardContent>
      )}
    </Card>
  );
}
