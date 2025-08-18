'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { MinusCircle } from 'lucide-react';
import { useFormContext } from 'react-hook-form';
import { cn } from '@/lib/utils';

type CertificateCardProps = {
  index: number;
  isExpanded: boolean;
  toggleExpand: (index: number) => void;
  remove: (index: number) => void;
  canRemove: boolean;
};

export default function CertificateCard({
  index,
  isExpanded,
  toggleExpand,
  remove,
  canRemove,
}: CertificateCardProps) {
  const { control } = useFormContext();

  return (
    <div
      className={cn(
        'rounded-xl border p-4 space-y-4',
        isExpanded && 'bg-muted',
      )}
    >
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-base">Certificate {index + 1}</h3>
        <div className="flex items-center gap-2">
          {canRemove && (
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => remove(index)}
              className="text-destructive"
            >
              <MinusCircle className="h-5 w-5" />
            </Button>
          )}
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => {
              toggleExpand(index);
            }}
          >
            {isExpanded ? 'Collapse' : 'Expand'}
          </Button>
        </div>
      </div>

      {isExpanded && (
        <div className="grid gap-4 sm:grid-cols-2">
          <FormField
            control={control}
            name={`certificates.${index}.name`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Certificate Name</FormLabel>
                <FormControl>
                  <Input
                    placeholder="e.g. AWS Certified Developer"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`certificates.${index}.issuing_organization`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Issuing Organization</FormLabel>
                <FormControl>
                  <Input placeholder="e.g. Amazon Web Services" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`certificates.${index}.issue_date`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Issue Date</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`certificates.${index}.credential_id`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Credential ID</FormLabel>
                <FormControl>
                  <Input placeholder="e.g. ABCD-1234" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name={`certificates.${index}.credential_url`}
            render={({ field }) => (
              <FormItem className="col-span-2">
                <FormLabel>Credential URL</FormLabel>
                <FormControl>
                  <Input
                    placeholder="https://www.your-cert-link.com"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
      )}
    </div>
  );
}
