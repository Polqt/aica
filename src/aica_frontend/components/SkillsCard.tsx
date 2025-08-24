'use client';

import React from 'react';
import { useFormContext } from 'react-hook-form';
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Trash2 } from 'lucide-react';

type skillCardProps = {
  index: number;
  remove: (index: number) => void;
  canRemove: boolean;
};

export default function SkillsCard({
  index,
  remove,
  canRemove,
}: skillCardProps) {
  const { control } = useFormContext();

  return (
    <div className="border border-slate-200 dark:border-slate-700 rounded-xl p-6 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 backdrop-blur-sm space-y-4 shadow-md hover:shadow-lg transition-all duration-300">
      <FormField
        control={control}
        name={`skills.${index}.name`}
        render={({ field }) => (
          <FormItem>
            <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
              <span className="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></span>
              Skill {index + 1}
            </FormLabel>
            <FormControl>
              <Input 
                {...field} 
                placeholder="e.g., React, Python, Project Management"
                className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white dark:bg-slate-700"
              />
            </FormControl>
            <FormMessage className="text-xs" />
          </FormItem>
        )}
      />

      {canRemove && (
        <Button 
          type="button" 
          variant={'outline'} 
          onClick={() => remove(index)}
          className="h-9 text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20 border-red-200 dark:border-red-800"
        >
          <Trash2 className="w-4 h-4 mr-2" />
          Remove
        </Button>
      )}
    </div>
  );
}
