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
    <div className="border rounded-md p-4 bg-muted space-y-3">
      <FormField
        control={control}
        name={`skills.${index}.name`}
        render={({ field }) => (
          <FormItem>
            <FormLabel>Skill</FormLabel>
            <FormControl>
              <Input {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      {canRemove && (
        <Button type="button" variant={'outline'} onClick={() => remove(index)}>
          Remove
        </Button>
      )}
    </div>
  );
}
