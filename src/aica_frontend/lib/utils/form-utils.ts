export function calculateFormCompletion(
  formData: Record<string, unknown>,
  optionalFields: string[] = [],
): { completedFields: number; totalFields: number; percentage: number } {
  const entries = Object.entries(formData);

  const completedFields = entries.filter(([key, value]) => {
    if (optionalFields.includes(key)) return true;

    return (
      value !== null &&
      value !== undefined &&
      value !== '' &&
      (typeof value === 'string' ? value.trim() !== '' : true)
    );
  }).length;

  const totalRequiredFields = entries.length - optionalFields.length;
  const percentage =
    totalRequiredFields > 0
      ? Math.round((completedFields / entries.length) * 100)
      : 100;

  return {
    completedFields,
    totalFields: entries.length,
    percentage,
  };
}

export function validateRequiredFields(
  formData: Record<string, unknown>,
  requiredFields: string[],
): { isValid: boolean; missingFields: string[] } {
  const missingFields = requiredFields.filter(field => {
    const value = formData[field];
    return (
      value === null ||
      value === undefined ||
      value === '' ||
      (typeof value === 'string' && value.trim() === '')
    );
  });

  return {
    isValid: missingFields.length === 0,
    missingFields,
  };
}

export function getFieldDisplayName(fieldName: string): string {
  return fieldName
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
