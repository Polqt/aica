'use client';

import React, { useCallback, useState } from 'react';
import Image from 'next/image';
import { toast } from 'sonner';
import { Camera, Upload } from 'lucide-react';
import { FormControl, FormItem, FormLabel } from './ui/form';


interface ProfilePictureUploadProps {
  value?: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export default function ProfilePictureUpload({
  value,
  onChange,
  disabled = false,
}: ProfilePictureUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(value || null);

  const validateFile = (file: File): boolean => {
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File too large', {
        description: 'Please select an image smaller than 5MB',
      });
      return false;
    }
    
    if (!file.type.startsWith('image/')) {
      toast.error('Invalid file type', {
        description: 'Please select a valid image file',
      });
      return false;
    }

    return true;
  };

  const handleImageUpload = useCallback(
    async (file: File) => {
      if (!validateFile(file)) return;

      setIsUploading(true);

      try {
        const reader = new FileReader();

        reader.onloadend = () => {
          const base64String = reader.result as string;
          setPreview(base64String);
          onChange(base64String);
          toast.success('Image uploaded successfully!');
        };

        reader.onerror = () => {
          throw new Error('Failed to read file');
        };

        reader.readAsDataURL(file);
      } catch {
        toast.error('Upload failed', {
          description: 'Failed to upload image. Please try again.',
        });
      } finally {
        setIsUploading(false);
      }
    },
    [onChange],
  );

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleImageUpload(file);
    }
  };

  return (
    <FormItem className="flex flex-col items-center">
      <FormLabel className="text-sm font-medium text-gray-700 dark:text-gray-300">
        Profile Picture (Optional)
      </FormLabel>
      <FormControl>
        <div className="relative">
          <div className="w-24 h-24 rounded-full border-4 border-gray-200 dark:border-gray-600 overflow-hidden bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
            {preview ? (
              <Image
                src={preview}
                alt="Profile"
                width={96}
                height={96}
                className="w-full h-full object-cover"
              />
            ) : (
              <Camera className="w-8 h-8 text-gray-400" />
            )}
          </div>

          <label className="absolute -bottom-2 -right-2 w-8 h-8 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center cursor-pointer transition-colors shadow-lg">
            <Upload className="w-4 h-4 text-white" />
            <input
              type="file"
              accept="image/*"
              className="hidden"
              disabled={disabled || isUploading}
              onChange={handleFileChange}
            />
          </label>

          {isUploading && (
            <div className="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            </div>
          )}
        </div>
      </FormControl>
    </FormItem>
  );
}
