'use client';

import { ChevronDown, ChevronUp } from 'lucide-react';
import React from 'react';
import { useFormContext } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel } from './ui/form';
import { Input } from './ui/input';
import { Button } from './ui/button';

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
  const { control, watch } = useFormContext();
  const name = watch(`certificates.${index}.name`);
  const issuingOrganization = watch(
    `certificates.${index}.issuing_organization`,
  );
  const issueDate = watch(`certificates.${index}.issue_date`);
  const credentialUrl = watch(`certificates.${index}.credential_url`);
  const credentialId = watch(`certificates.${index}.credential_id`);

  return (
    <div className="border rounded-md p-4 bg-muted space-y-3">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => toggleExpand(index)}
      >
        <div>
          <h3 className="font-semibold text-base">
            {name || 'Certificate Name'} -{' '}
            {issuingOrganization || 'Organization'}
          </h3>
          <p className="text-sm text-muted-foreground">
            {issueDate || 'Issue Date'} - {credentialId || 'Credential ID'}
          </p>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>

      {isExpanded && (
        <div className="pt-3 space-y-4">
          <FormField
            control={control}
            name={`certificates.${index}.name`}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Certificate Name</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
              </FormItem>
            )}
          />

          {canRemove && (
            <Button
              type="button"
              variant={'outline'}
              onClick={() => remove(index)}
            >
              Remove Certificate
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
