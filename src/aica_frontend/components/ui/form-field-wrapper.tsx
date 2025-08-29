'use client';

import React from 'react';
import { FieldError } from 'react-hook-form';
import { FormItem, FormLabel, FormControl, FormMessage } from './form';
import { Input } from './input';
import { Textarea } from './textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './select';
import { Checkbox } from './checkbox';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface BaseFormFieldProps {
  label: string;
  error?: FieldError;
  required?: boolean;
  icon?: LucideIcon;
  className?: string;
}

interface InputFieldProps extends BaseFormFieldProps {
  type: 'input';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  maxLength?: number;
}

interface TextareaFieldProps extends BaseFormFieldProps {
  type: 'textarea';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  maxLength?: number;
  rows?: number;
}

interface SelectFieldProps extends BaseFormFieldProps {
  type: 'select';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  options: Array<{ value: string; label: string }>;
  disabled?: boolean;
}

interface CheckboxFieldProps extends BaseFormFieldProps {
  type: 'checkbox';
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  description?: string;
}

type FormFieldWrapperProps = InputFieldProps | TextareaFieldProps | SelectFieldProps | CheckboxFieldProps;

export function FormFieldWrapper(props: FormFieldWrapperProps) {
  const { label, error, required, icon: Icon, className } = props;

  const renderField = () => {
    switch (props.type) {
      case 'input':
        return (
          <Input
            placeholder={props.placeholder}
            value={props.value}
            onChange={(e) => props.onChange?.(e.target.value)}
            disabled={props.disabled}
            maxLength={props.maxLength}
            className={cn(
              "h-11 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80",
              className
            )}
          />
        );

      case 'textarea':
        return (
          <Textarea
            placeholder={props.placeholder}
            value={props.value}
            onChange={(e) => props.onChange?.(e.target.value)}
            disabled={props.disabled}
            maxLength={props.maxLength}
            rows={props.rows || 4}
            className={cn(
              "border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none bg-white/80 dark:bg-slate-700/80",
              className
            )}
          />
        );

      case 'select':
        return (
          <Select value={props.value} onValueChange={props.onChange} disabled={props.disabled}>
            <SelectTrigger className={cn(
              "h-11 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80",
              className
            )}>
              <SelectValue placeholder={props.placeholder} />
            </SelectTrigger>
            <SelectContent className="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700">
              {props.options.map(option => (
                <SelectItem
                  key={option.value}
                  value={option.value}
                  className="py-3 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                >
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );

      case 'checkbox':
        return (
          <div className="flex flex-row items-start space-x-3 space-y-0">
            <FormControl>
              <Checkbox
                checked={props.checked}
                onCheckedChange={props.onChange}
              />
            </FormControl>
            <div className="space-y-1 leading-none">
              <FormLabel className="text-sm font-medium">
                {label}
              </FormLabel>
              {props.description && (
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {props.description}
                </p>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <FormItem className={className}>
      {props.type !== 'checkbox' && (
        <FormLabel className={cn(
          "flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300",
          required && "after:content-['*'] after:text-red-500 after:ml-1"
        )}>
          {Icon && <Icon className="w-4 h-4 text-blue-600 dark:text-blue-400" />}
          {label}
        </FormLabel>
      )}
      <FormControl>
        {renderField()}
      </FormControl>
      {error && <FormMessage className="text-xs" />}
    </FormItem>
  );
}