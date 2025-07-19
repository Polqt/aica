'use client';

import React from 'react';
import { useFormContext } from 'react-hook-form';
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { Textarea } from './ui/textarea';

type ExperienceCardProps = {
  index: number;
  isExpanded: boolean;
  toggleExpand: (index: number) => void;
  remove: (index: number) => void;
  canRemove: boolean;
};

export default function ExperienceCard({
  index,
  isExpanded,
  toggleExpand,
  remove,
  canRemove,
}: ExperienceCardProps) {
  const { control, watch } = useFormContext();
  const jobTitle = watch(`experiences.${index}.job_title`);
  const companyName = watch(`experiences.${index}.company_name`);
  const start = watch(`experiences.${index}.start_date`);
  const end = watch(`experiences.${index}.end_date`);

  return (
    <div className="border rounded-md p-4 bg-muted space-y-3">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => toggleExpand(index)}
      >
        <div>
          <h3 className="font-semibold text-base">
            {jobTitle || 'Job Title'} - {companyName || 'Company Name'}
          </h3>
          <p className="text-sm text-muted-foreground">
            {start || 'Start'} - {end || 'End'}
          </p>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>

      {isExpanded && (
        <div className="pt-3 space-y-4">
          <FormField
            control={control}
            name={`experiences.${index}.job_title`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Job Title</FormLabel>
                <FormControl>
                  <Input placeholder="Software Engineer" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`experiences.${index}.company_name`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Company Name</FormLabel>
                <FormControl>
                  <Input placeholder="ABC Company" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`experiences.${index}.description`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Job Description</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="e.g. Developed APIs using FastAPI, Collaborated with UI/UX team"
                    value={
                      Array.isArray(field.value)
                        ? field.value.join('\n')
                        : field.value
                    }
                    onChange={e => {
                      const lines = e.target.value
                        .split('\n')
                        .filter(line => line.trim() !== '');
                      field.onChange(lines.length > 0 ? lines : ['']);
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`experiences.${index}.start_date`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Start Date</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`experiences.${index}.end_date`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>End Date</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          {canRemove && (
            <Button
              type="button"
              variant="outline"
              onClick={() => remove(index)}
            >
              Remove Experience
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
