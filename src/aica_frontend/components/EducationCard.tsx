'use client';

import { ChevronDown, ChevronUp } from 'lucide-react';
import React from 'react';
import { useFormContext } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel } from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';

type EducationCardProps = {
  index: number;
  isExpanded: boolean;
  toggleExpand: (index: number) => void;
  remove: (index: number) => void;
  canRemove: boolean;
};

export default function EducationCard({
  index,
  isExpanded,
  toggleExpand,
  remove,
  canRemove,
}: EducationCardProps) {
  const { control, watch } = useFormContext();
  const institution = watch(`educations.${index}.institution_name`);
  const location = watch(`educations.${index}.address`);
  const start = watch(`educations.${index}.start_date`);
  const end = watch(`educations.${index}.end_date`);

  return (
    <div className="border rounded-md p-4 bg-muted space-y-3">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => toggleExpand(index)}
      >
        <div>
          <h3 className="font-semibold text-base">
            {institution || 'School Name'} - {location || 'Location'}
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
            name={`educations.${index}.institution_name`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Institution Name</FormLabel>
                <FormControl>
                  <Input placeholder="USLS - Bacolod" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.address`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>School Address</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.degree`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Degree</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.field_of_study`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Field of Study</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.start_date`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Start Year</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.end_date`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>End Year</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`educations.${index}.description`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Description</FormLabel>
                <FormControl>
                  <Input placeholder="" {...field} />
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
              Remove Education
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
