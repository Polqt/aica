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
  const { control, watch, setValue, formState } = useFormContext();

  const institution = watch(`educations.${index}.institution_name`);
  const location = watch(`educations.${index}.address`);
  const degree = watch(`educations.${index}.degree`);
  const startDate = watch(`educations.${index}.start_date`);
  const endDate = watch(`educations.${index}.end_date`);
  // State for custom degree and custom field input
  const [showCustomDegree, setShowCustomDegree] = React.useState(degree && !DEGREE_SUGGESTIONS.includes(degree));
  const [showCustomField, setShowCustomField] = React.useState(false);

  // Watch field_of_study for custom handler
  const fieldOfStudy = watch(`educations.${index}.field_of_study`);
  React.useEffect(() => {
    setShowCustomDegree(degree === 'Others');
  }, [degree]);
  React.useEffect(() => {
    setShowCustomField(fieldOfStudy === 'Others');
  }, [fieldOfStudy]);

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
    Array.isArray(educationErrors) && index >= 0 && index < educationErrors.length
    ? (educationErrors[index] as Record<string, { message?: string }> | undefined)
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
        },
      },
    });
  };

  return (
    <Card
      className={cn(
        'group transition-all duration-300 hover:shadow-xl border border-gray-300 dark:border-gray-600 relative overflow-hidden',
        isExpanded
          ? 'shadow-lg ring-2 ring-blue-500/30 dark:ring-blue-400/30 bg-gradient-to-br from-white to-blue-50 dark:from-gray-900 dark:to-blue-900/20'
          : 'hover:border-blue-400 dark:hover:border-blue-500 bg-white dark:bg-gray-900',
        hasErrors &&
          'border-red-300 dark:border-red-600 bg-red-50/50 dark:bg-red-900/10',
      )}
    >
      {/* Subtle background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100/20 to-transparent dark:from-blue-900/10 dark:to-transparent opacity-50 pointer-events-none" />
      <CardHeader
        className="cursor-pointer relative z-10"
        onClick={() => toggleExpand(index)}
      >
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-3">
              <div
                className={cn(
                  'flex items-center justify-center w-12 h-12 rounded-full transition-all duration-300 shadow-md',
                  isComplete
                    ? 'bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/40 dark:to-blue-800/40 text-blue-600 dark:text-blue-300 shadow-blue-200/50 dark:shadow-blue-700/30'
                    : hasErrors
                    ? 'bg-gradient-to-br from-red-100 to-red-200 dark:from-red-900/40 dark:to-red-800/40 text-red-600 dark:text-red-300 shadow-red-200/50 dark:shadow-red-700/30'
                    : 'bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800/40 dark:to-gray-700/40 text-gray-500 dark:text-gray-400 shadow-gray-200/50 dark:shadow-gray-700/30',
                )}
              >
                {isComplete ? (
                  <CheckCircle2 className="w-6 h-6" />
                ) : hasErrors ? (
                  <AlertCircle className="w-6 h-6" />
                ) : (
                  <GraduationCap className="w-6 h-6" />
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
                      className="text-blue-600 dark:text-blue-400 border-blue-300 dark:border-blue-600"
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

                {/* Education Completion Progress - Matches Profile Page Style */}
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
                          Education Completion
                        </h4>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          {completedFields}/{requiredFields.length} fields completed
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
                      ✓ Education record complete
                    </p>
                  )}
                </div>
              </div>
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
            {/* Institution Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={control}
                name={`educations.${index}.institution_name`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <School className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      Institution Name *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., University of the Philippines"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
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
                      <MapPin className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      Location *
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g., Quezon City, Philippines"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      />
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />
            </div>

            {/* Degree Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Degree select with 'Others' option */}
              <FormField
                control={control}
                name={`educations.${index}.degree`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <GraduationCap className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      Degree *
                    </FormLabel>
                    <FormControl>
                      <div>
                        <select
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all w-full px-3 rounded block bg-white dark:bg-gray-900"
                          value={DEGREE_SUGGESTIONS.includes(field.value) ? field.value : (field.value ? 'Others' : '')}
                          onChange={e => {
                            if (e.target.value === 'Others') {
                              setShowCustomDegree(true);
                              field.onChange('Others');
                              setValue(`educations.${index}.degree`, 'Others');
                            } else {
                              setShowCustomDegree(false);
                              field.onChange(e.target.value);
                              setValue(`educations.${index}.degree`, e.target.value);
                            }
                          }}
                        >
                          <option value="" disabled>Select degree</option>
                          {DEGREE_SUGGESTIONS.map(option => (
                            <option key={option} value={option}>{option}</option>
                          ))}
                          <option value="Others">Others</option>
                        </select>
                        {showCustomDegree && (
                          <div className="pt-3">
                            <FormLabel className="text-sm text-gray-700 dark:text-gray-300 mb-1 block">Specify Degree</FormLabel>
                            <Input
                              className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all w-full"
                              placeholder="Enter your degree"
                              value={field.value && field.value !== 'Others' ? field.value : ''}
                              onChange={e => {
                                setValue(`educations.${index}.degree`, e.target.value);
                                field.onChange(e.target.value);
                              }}
                            />
                          </div>
                        )}
                      </div>
                    </FormControl>
                    <FormMessage className="text-xs" />
                  </FormItem>
                )}
              />

              {/* Field of Study select with 'Others' option */}
              <FormField
                control={control}
                name={`educations.${index}.field_of_study`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      Field of Study
                    </FormLabel>
                    <FormControl>
                      <div>
                        <select
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all w-full px-3 rounded block bg-white dark:bg-gray-900"
                          value={FIELD_SUGGESTIONS.includes(field.value) ? field.value : (field.value ? 'Others' : '')}
                          onChange={e => {
                            if (e.target.value === 'Others') {
                              setShowCustomField(true);
                              field.onChange('Others');
                              setValue(`educations.${index}.field_of_study`, 'Others');
                            } else {
                              setShowCustomField(false);
                              field.onChange(e.target.value);
                              setValue(`educations.${index}.field_of_study`, e.target.value);
                            }
                          }}
                        >
                          <option value="" disabled>Select field of study</option>
                          {FIELD_SUGGESTIONS.map(option => (
                            <option key={option} value={option}>{option}</option>
                          ))}
                          <option value="Others">Others</option>
                        </select>
                        {showCustomField && (
                          <div className="pt-3">
                            <FormLabel className="text-sm text-gray-700 dark:text-gray-300 mb-1 block">Specify Field of Study</FormLabel>
                            <Input
                              className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all w-full"
                              placeholder="Enter your field of study"
                              value={field.value && field.value !== 'Others' ? field.value : ''}
                              onChange={e => {
                                setValue(`educations.${index}.field_of_study`, e.target.value);
                                field.onChange(e.target.value);
                              }}
                            />
                          </div>
                        )}
                      </div>
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
                name={`educations.${index}.start_date`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      Start Date *
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
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
                      <Calendar className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      End Date *
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="month"
                        {...field}
                        className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
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
                      className="min-h-[100px] border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
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
