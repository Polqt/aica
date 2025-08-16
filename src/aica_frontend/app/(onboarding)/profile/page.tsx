'use client';

import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';
import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/style.css';
import Image from 'next/image';
import { toast } from 'sonner';
import {
  User,
  MapPin,
  Phone,
  Linkedin,
  Camera,
  FileText,
  AlertCircle,
  ArrowRight,
  Upload,
  Mail,
  Calendar,
  Globe,
} from 'lucide-react';

const profileFormSchema = z.object({
  first_name: z.string().min(2, 'First name must be at least 2 characters').max(50, 'First name must be less than 50 characters').regex(/^[A-Za-z\s]+$/, 'First name should only contain letters'),
  middle_name: z.string().optional(),
  last_name: z.string().min(2, 'Last name must be at least 2 characters').max(50, 'Last name must be less than 50 characters').regex(/^[A-Za-z\s]+$/, 'Last name should only contain letters'),
  email: z.string().email('Invalid email address'),
  gender: z.string().optional(),
  date_of_birth: z.string().optional(),
  place_of_birth: z.string().optional(),
  nationality: z.string().optional(),
  marital_status: z.string().optional(),
  religion: z.string().optional(),
  professional_title: z.string().min(1, 'Professional title is required'),
  contact_number: z.string().min(7, 'Invalid contact number').max(20, 'Contact number is too long'),
  address: z.string().min(5, 'Address must be at least 5 characters').max(200, 'Address must be less than 200 characters'),
  linkedin_url: z
    .string()
    .optional()
    .refine(
      val => !val || val === '' || z.string().url().safeParse(val).success,
      {
        message: 'Enter a valid LinkedIn URL',
      },
    ),
  summary: z.string().min(50, 'Summary must be at least 50 characters to give us a good overview').max(500, 'Summary must be less than 500 characters'),
  profile_picture: z.string().optional(),
});

const PROFESSIONAL_TITLES = [
  'Software Engineer',
  'Senior Software Engineer',
  'Lead Software Engineer',
  'Frontend Developer',
  'Senior Frontend Developer',
  'Backend Developer',
  'Senior Backend Developer',
  'Full Stack Developer',
  'Senior Full Stack Developer',
  'UI/UX Designer',
  'Senior UI/UX Designer',
  'Product Designer',
  'Data Scientist',
  'Senior Data Scientist',
  'Data Analyst',
  'DevOps Engineer',
  'Senior DevOps Engineer',
  'Cloud Engineer',
  'Mobile Developer',
  'iOS Developer',
  'Android Developer',
  'QA Engineer',
  'Test Automation Engineer',
  'Product Manager',
  'Technical Lead',
  'Engineering Manager',
  'CTO',
  'Architect',
  'Solutions Architect',
  'Security Engineer',
  'Machine Learning Engineer',
  'AI Engineer',
  'Blockchain Developer',
  'Game Developer',
  'Other',
] as const;

export default function Profile() {
  const router = useRouter();
  const [apiError, setApiError] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const { updateData } = useOnboarding();

  const form = useForm<z.infer<typeof profileFormSchema>>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      first_name: '',
      middle_name: '',
      last_name: '',
      email: '',
      gender: '',
      date_of_birth: '',
      place_of_birth: '',
      nationality: '',
      marital_status: '',
      religion: '',
      professional_title: '',
      contact_number: '',
      address: '',
      linkedin_url: '',
      summary: '',
      profile_picture: '',
    },
    mode: 'onBlur',
  });

  const watchedFields = form.watch();
  const completedFields = Object.entries(watchedFields).filter(
    ([key, value]) => {
      if (key === 'linkedin_url' || key === 'profile_picture') return true;
      return value && value.toString().trim() !== '';
    },
  ).length;
  const totalRequiredFields = 6;
  const completionPercentage = Math.round(
    (completedFields / totalRequiredFields) * 100,
  );

  const handleImageUpload = useCallback(
    async (file: File) => {
      setIsUploading(true);
      try {
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
          toast.error('File too large', {
            description: 'Please select an image smaller than 5MB',
          });
          return;
        }

        // Validate file type
        if (!file.type.startsWith('image/')) {
          toast.error('Invalid file type', {
            description: 'Please select a valid image file',
          });
          return;
        }

        const reader = new FileReader();
        reader.onloadend = () => {
          const base64String = reader.result as string;
          form.setValue('profile_picture', base64String);
          setImagePreview(base64String);
          toast.success('Image uploaded successfully!');
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
    [form],
  );

  async function onSubmit(values: z.infer<typeof profileFormSchema>) {
    setApiError(null);
    try {
      updateData(values);

      toast.success('Profile Completed!', {
        description:
          "Great! Your profile looks amazing. Let's add your education next.",
        duration: 3000,
      });

      setTimeout(() => {
        router.push('/education');
      }, 1000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';

      toast.error('Profile Update Failed', {
        description: errorMessage,
        duration: 5000,
      });

      setApiError(errorMessage);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
            <User className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Complete Your Profile
          </h1>
          <p className="text-gray-600 dark:text-gray-300 max-w-md mx-auto">
            Let&apos;s get to know you better. This information will help us
            match you with the perfect opportunities.
          </p>
        </div>

        <Card className="mb-6 border-0 shadow-sm bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Profile Completion
              </span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {completionPercentage}%
              </span>
            </div>
            <Progress value={completionPercentage} className="w-full h-2" />
            {completionPercentage < 100 && (
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                Complete all required fields to continue
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="border-0 shadow-lg bg-white dark:bg-gray-800">
          <CardContent className="p-8">
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-6"
              >
                <div className="flex flex-col items-center space-y-4 pb-6 border-b border-gray-200 dark:border-gray-700">
                  <FormField
                    control={form.control}
                    name="profile_picture"
                    render={({ field }) => (
                      <FormItem className="flex flex-col items-center">
                        <FormLabel className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          Profile Picture (Optional)
                        </FormLabel>
                        <FormControl>
                          <div className="relative">
                            <div className="w-24 h-24 rounded-full border-4 border-gray-200 dark:border-gray-600 overflow-hidden bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                              {imagePreview || field.value ? (
                                <Image
                                  src={imagePreview || field.value || ''}
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
                                disabled={isUploading}
                                onChange={e => {
                                  const file = e.target.files?.[0];
                                  if (file) handleImageUpload(file);
                                }}
                              />
                            </label>
                          </div>
                        </FormControl>
                        {isUploading && (
                          <p className="text-xs text-blue-600 dark:text-blue-400">
                            Uploading...
                          </p>
                        )}
                      </FormItem>
                    )}
                  />
                </div>

                {/* Personal Information */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 mb-2">
                    <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    <span className="font-bold text-base text-gray-900 dark:text-white">Personal Information</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <FormField
                      control={form.control}
                      name="first_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            First Name
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="Enter your first name" {...field} className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="middle_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            Middle Name / Initial
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="Enter middle name / initial" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="last_name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            Last Name
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="Enter your last name" {...field} className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="email"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <Mail className="w-4 h-4" />
                            Email Address
                          </FormLabel>
                          <FormControl>
                            <Input type="email" placeholder="Enter email address" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="gender"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            Gender
                          </FormLabel>
                          <Select onValueChange={field.onChange} value={field.value || ''}>
                            <FormControl>
                              <SelectTrigger className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                                <SelectValue placeholder="Select gender..." />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem value="Male">Male</SelectItem>
                              <SelectItem value="Female">Female</SelectItem>
                              <SelectItem value="Other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="marital_status"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            Marital Status
                          </FormLabel>
                          <Select onValueChange={field.onChange} value={field.value || ''}>
                            <FormControl>
                              <SelectTrigger className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                                <SelectValue placeholder="Select status..." />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem value="Single">Single</SelectItem>
                              <SelectItem value="Married">Married</SelectItem>
                              <SelectItem value="Divorced">Divorced</SelectItem>
                              <SelectItem value="Widowed">Widowed</SelectItem>
                              <SelectItem value="Other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="date_of_birth"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <Calendar className="w-4 h-4" />
                            Date of Birth
                          </FormLabel>
                          <FormControl>
                            <Input type="date" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="place_of_birth"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <MapPin className="w-4 h-4" />
                            Place of Birth
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. Manila, Philippines" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="nationality"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <Globe className="w-4 h-4" />
                            Nationality / Citizenship
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. Filipino" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="religion"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                            <User className="w-4 h-4" />
                            Religion
                          </FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. Catholic" {...field} className="h-11 border-gray-300 dark:border-gray-600" />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                  </div>
                </div>

                {/* Professional Title */}
                <FormField
                  control={form.control}
                  name="professional_title"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        <FileText className="w-4 h-4" />
                        Professional Title
                      </FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                            <SelectValue placeholder="Select your professional title" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="max-h-60">
                          {PROFESSIONAL_TITLES.map(title => (
                            <SelectItem
                              key={title}
                              value={title}
                              className="py-2"
                            >
                              {title}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />

                {/* Contact Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField
                    control={form.control}
                    name="contact_number"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                          <Phone className="w-4 h-4" />
                          Contact Number
                        </FormLabel>
                        <FormControl>
                          <PhoneInput
                            country={'ph'}
                            value={field.value}
                            onChange={field.onChange}
                            containerClass="!w-full"
                            inputClass="!w-full !h-11 !bg-background !text-foreground !border-gray-300 dark:!border-gray-600 !focus:ring-2 !focus:ring-blue-500 !focus:border-transparent !transition-all"
                            buttonClass="!border-gray-300 dark:!border-gray-600 !bg-background"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="address"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                          <MapPin className="w-4 h-4" />
                          Address
                        </FormLabel>
                        <FormControl>
                          <Input
                            placeholder="e.g. Manila, Philippines"
                            {...field}
                            className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                          />
                        </FormControl>
                        <FormMessage className="text-xs" />
                      </FormItem>
                    )}
                  />
                </div>

                {/* LinkedIn URL */}
                <FormField
                  control={form.control}
                  name="linkedin_url"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        <Linkedin className="w-4 h-4" />
                        LinkedIn URL
                        <Badge variant="secondary" className="text-xs">
                          Optional
                        </Badge>
                      </FormLabel>
                      <FormControl>
                        <Input
                          placeholder="https://linkedin.com/in/your-profile"
                          {...field}
                          className="h-11 border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />

                {/* Summary */}
                <FormField
                  control={form.control}
                  name="summary"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                        <FileText className="w-4 h-4" />
                        Professional Summary
                      </FormLabel>
                      <FormControl>
                        <Textarea
                          placeholder="Tell us about your professional background, key skills, and career goals. This helps us understand what makes you unique..."
                          {...field}
                          className="min-h-[120px] border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
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

                {apiError && (
                  <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                    <p className="text-sm text-red-600 dark:text-red-400">
                      {apiError}
                    </p>
                  </div>
                )}

                <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
                  <Button
                    type="submit"
                    disabled={
                      form.formState.isSubmitting || completionPercentage < 100
                    }
                    className="w-full h-12 text-base font-medium bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 transition-all duration-200 flex items-center justify-center gap-2"
                  >
                    {form.formState.isSubmitting ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Saving Profile...
                      </>
                    ) : (
                      <>
                        Continue to Education
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
