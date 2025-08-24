'use client';

import React, { useEffect } from 'react';
import { useFormContext, useFieldArray } from 'react-hook-form';
import { toast } from 'sonner';
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Textarea } from './ui/textarea';
import { Checkbox } from './ui/checkbox';
import {
  ChevronDown,
  ChevronUp,
  Briefcase,
  Building,
  Calendar,
  Plus,
  Trash2,
  AlertCircle,
  CheckCircle2,
  Target,
  Award,
  ListChecks,
} from 'lucide-react';
import { cn } from '@/lib/utils';

type ExperienceCardProps = {
  index: number;
  isExpanded: boolean;
  toggleExpand: (index: number) => void;
  remove: (index: number) => void;
  canRemove: boolean;
};

const JOB_TITLE_SUGGESTIONS = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Senior Software Engineer',
  'Lead Developer',
  'DevOps Engineer',
  'Data Scientist',
  'Product Manager',
  'UI/UX Designer',
  'Mobile Developer',
  'QA Engineer',
];

export default function ExperienceCard({
  index,
  isExpanded,
  toggleExpand,
  remove,
  canRemove,
}: ExperienceCardProps) {
  const { control, watch, formState } = useFormContext();

  // Watch field values for dynamic display
  const jobTitle = watch(`experiences.${index}.job_title`);
  const companyName = watch(`experiences.${index}.company_name`);
  const startDate = watch(`experiences.${index}.start_date`);
  const endDate = watch(`experiences.${index}.end_date`);
  const isCurrent = watch(`experiences.${index}.is_current`);
  const descriptions = watch(`experiences.${index}.description`);

  // Calculate completion status
  const requiredFields = [jobTitle, companyName, startDate];
  if (!isCurrent) requiredFields.push(endDate);
  const completedRequiredFields = requiredFields.filter(
    field => field && field.trim() !== '',
  ).length;
  const hasDescriptions =
    descriptions &&
    descriptions.some((desc: string) => desc && desc.trim() !== '');
  const isComplete =
    completedRequiredFields === requiredFields.length && hasDescriptions;

  const totalRequiredFields = requiredFields.length + 1; // +1 for description
  const completedFields = completedRequiredFields + (hasDescriptions ? 1 : 0);
  const completionPercentage = Math.round(
    (completedFields / totalRequiredFields) * 100,
  );

  // Check for errors in this experience record
  const experienceErrors = formState.errors?.experiences;
  const hasErrors =
    experienceErrors && Array.isArray(experienceErrors)
      ? (experienceErrors[index] as
          | Record<string, { message?: string }>
          | undefined)
      : undefined;

  // Monitor for validation errors and show toast notifications
  useEffect(() => {
    if (hasErrors && formState.isSubmitted) {
      const errorCount = Object.keys(hasErrors).length;
      toast.error('Please fix validation errors', {
        description: `${errorCount} field${errorCount > 1 ? 's' : ''} need${
          errorCount === 1 ? 's' : ''
        } attention in Work Experience ${index + 1}`,
        action: {
          label: 'Fix Issues',
          onClick: () => {
            if (!isExpanded) {
              toggleExpand(index);
            }
          },
        },
      });
    }
  }, [hasErrors, formState.isSubmitted, isExpanded, toggleExpand, index]);

  const {
    fields: descriptionFields,
    append: appendDescription,
    remove: removeDescription,
  } = useFieldArray({
    control,
    name: `experiences.${index}.description`,
  });

  const handleRemove = () => {
    toast('Remove Work Experience?', {
      description:
        'This action cannot be undone. The work experience record will be permanently deleted.',
      action: {
        label: 'Remove',
        onClick: () => {
          remove(index);
          toast.success('Work experience record removed successfully');
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

  const addDescription = () => {
    if (descriptionFields.length >= 10) {
      toast.error('Maximum limit reached', {
        description: 'You can add up to 10 accomplishments only.',
      });
      return;
    }
    appendDescription('');
    toast.success('New accomplishment added', {
      description:
        'Describe your key achievement or responsibility in this role.',
    });
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
    });
  };

  return (
    <Card
      className={cn(
        'transition-all duration-300 hover:shadow-md',
        isExpanded && 'ring-2 ring-purple-200 dark:ring-purple-800',
        hasErrors && 'ring-2 ring-red-200 dark:ring-red-800',
        isComplete && 'border-purple-200 dark:border-purple-800',
      )}
    >
      <CardHeader className="pb-3">
        <div
          className="flex justify-between items-start cursor-pointer group"
          onClick={() => toggleExpand(index)}
        >
          <div className="flex-1 min-w-0 pr-4">
            <div className="flex items-center gap-2 mb-2">
              <div
                className={cn(
                  'w-8 h-8 rounded-lg flex items-center justify-center transition-colors',
                  isComplete
                    ? 'bg-purple-100 dark:bg-purple-900/30'
                    : 'bg-gray-100 dark:bg-gray-800',
                )}
              >
                <Briefcase
                  className={cn(
                    'w-4 h-4',
                    isComplete
                      ? 'text-purple-600 dark:text-purple-400'
                      : 'text-gray-500 dark:text-gray-400',
                  )}
                />
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="secondary" className="text-xs">
                  Experience {index + 1}
                </Badge>
                {isCurrent && (
                  <Badge
                    variant="secondary"
                    className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs"
                  >
                    Current
                  </Badge>
                )}
                {isComplete && (
                  <Badge
                    variant="secondary"
                    className="bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs"
                  >
                    <CheckCircle2 className="w-3 h-3 mr-1" />
                    Complete
                  </Badge>
                )}
                {hasErrors && (
                  <Badge variant="destructive" className="text-xs">
                    <AlertCircle className="w-3 h-3 mr-1" />
                    Errors
                  </Badge>
                )}
              </div>
            </div>

            <h3 className="font-semibold text-base text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
              {jobTitle || 'Job Title'}
              {companyName && ` at ${companyName}`}
            </h3>

            <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 mt-1">
              {companyName && (
                <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-300">
                  <Building className="w-3 h-3" />
                  {companyName}
                </div>
              )}
              {(startDate || endDate) && (
                <div className="flex items-center gap-1 text-sm text-gray-600 dark:text-gray-300">
                  <Calendar className="w-3 h-3" />
                  {formatDate(startDate) || 'Start'} -{' '}
                  {isCurrent ? 'Present' : formatDate(endDate) || 'End'}
                </div>
              )}
            </div>

            {/* Experience Completion Progress - Matches Education Card Style */}
            <div className="mt-3 p-3 bg-gradient-to-r from-blue-50/40 via-purple-50/30 to-indigo-50/20 dark:from-blue-900/20 dark:via-purple-900/15 dark:to-indigo-900/10 rounded-lg border border-blue-100/50 dark:border-blue-800/30">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center shadow-md">
                    <span className="text-white font-semibold text-xs">
                      {completionPercentage}%
                    </span>
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-gray-800 dark:text-gray-200">
                      Experience Completion
                    </h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {completedFields}/{totalRequiredFields} fields completed
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>
              
              {completionPercentage < 100 && (
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Complete all required fields
                </p>
              )}
              {completionPercentage === 100 && (
                <p className="text-xs text-green-600 dark:text-green-400 font-medium mt-1">
                  ✓ Experience record complete
                </p>
              )}
            </div>
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
            {/* Job Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`experiences.${index}.job_title`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Briefcase className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      Job Title *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Software Engineer"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                        list={`job-title-suggestions-${index}`}
                      />
                    </FormControl>
                    <datalist id={`job-title-suggestions-${index}`}>
                      {JOB_TITLE_SUGGESTIONS.map(suggestion => (
                        <option key={suggestion} value={suggestion} />
                      ))}
                    </datalist>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name={`experiences.${index}.company_name`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Building className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      Company Name *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Google, Microsoft, Startup Inc."
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`experiences.${index}.start_date`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      Start Date *
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name={`experiences.${index}.end_date`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                      End Date {!isCurrent && '*'}
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        disabled={isCurrent}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all disabled:opacity-50"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Current Job Checkbox */}
            <FormField
              control={control}
              name={`experiences.${index}.is_current`}
              render={({ field }) => (
                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                  <FormControl>
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={checked => {
                        field.onChange(checked);
                        if (checked) {
                          // Clear end date when current job is checked
                          control._formValues.experiences[index].end_date = '';
                        }
                      }}
                    />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel className="text-sm font-medium">
                      I currently work here
                    </FormLabel>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Check this if this is your current position
                    </p>
                  </div>
                </FormItem>
              )}
            />

            {/* Job Descriptions/Accomplishments */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <FormLabel className="flex items-center gap-2 text-sm font-medium">
                  <Target className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                  Key Accomplishments & Responsibilities *
                </FormLabel>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={addDescription}
                  disabled={descriptionFields.length >= 10}
                  className="text-xs h-8"
                >
                  <Plus className="w-3 h-3 mr-1" />
                  Add Point
                </Button>
              </div>

              <div className="space-y-3">
                {descriptionFields.map((field, descIndex) => (
                  <div key={field.id} className="flex gap-2">
                    <FormField
                      control={control}
                      name={`experiences.${index}.description.${descIndex}`}
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormControl>
                            <Textarea
                              placeholder={`${
                                descIndex === 0
                                  ? 'e.g., Developed and maintained RESTful APIs using FastAPI and PostgreSQL'
                                  : 'Add another key accomplishment or responsibility...'
                              }`}
                              {...field}
                              className="min-h-[80px] border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                              maxLength={200}
                            />
                          </FormControl>
                          <div className="flex justify-between items-center">
                            <FormMessage className="text-xs" />
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {field.value?.length || 0}/200
                            </span>
                          </div>
                        </FormItem>
                      )}
                    />
                    {descriptionFields.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeDescription(descIndex)}
                        className="text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 p-2 mt-2"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>

              <p className="text-xs text-gray-500 dark:text-gray-400">
                💡 Tip: Use action verbs and quantify your achievements where
                possible (e.g., &quot;Increased performance by 30%&quot;)
              </p>
            </div>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
