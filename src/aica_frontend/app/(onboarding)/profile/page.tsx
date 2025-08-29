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
} from 'lucide-react';
import { motion } from 'motion/react';
import AnimatedBackground from '@/components/AnimatedBackground';

const profileFormSchema = z.object({
  first_name: z
    .string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters')
    .regex(/^[A-Za-z\s]+$/, 'First name should only contain letters'),
  last_name: z
    .string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters')
    .regex(/^[A-Za-z\s]+$/, 'Last name should only contain letters'),
  professional_title: z.string().min(1, 'Professional title is required'),
  contact_number: z
    .string()
    .min(7, 'Invalid contact number')
    .max(20, 'Contact number is too long'),
  address: z
    .string()
    .min(5, 'Address must be at least 5 characters')
    .max(200, 'Address must be less than 200 characters'),
  linkedin_url: z
    .string()
    .optional()
    .refine(
      val => !val || val === '' || z.string().url().safeParse(val).success,
      {
        message: 'Enter a valid LinkedIn URL',
      },
    ),
  summary: z
    .string()
    .min(
      50,
      'Summary must be at least 50 characters to give us a good overview',
    )
    .max(500, 'Summary must be less than 500 characters'),
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
      last_name: '',
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
      if (key === 'linkedin_url' || key === 'profile_picture') return false;
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
      const cleanData = JSON.parse(JSON.stringify(values));
      updateData(cleanData);

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
    <div className="relative min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/40 to-purple-50/30 dark:from-slate-900 dark:via-blue-900/20 dark:to-purple-900/15 py-8 px-4 overflow-hidden">
      <AnimatedBackground />
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.8, type: 'spring', stiffness: 200 }}
            className="relative inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-6 shadow-xl"
          >
            <User className="w-12 h-12 text-white" />
            <div className="absolute -inset-2 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-2xl blur-lg animate-pulse"></div>
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 dark:from-white dark:to-slate-200 bg-clip-text text-transparent mb-4"
          >
            Complete Your{' '}
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 dark:from-blue-300 dark:via-purple-300 dark:to-indigo-300 bg-clip-text text-transparent">
              Profile
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg text-slate-600 dark:text-slate-300 max-w-md mx-auto leading-relaxed"
          >
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent font-semibold">
              Let&apos;s get to know you better
            </span>{' '}
            — this information helps us match you with perfect opportunities
          </motion.p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card className="mb-6 border-0 shadow-lg bg-gradient-to-r from-blue-50/40 via-purple-50/30 to-indigo-50/20 dark:from-blue-900/20 dark:via-purple-900/15 dark:to-indigo-900/10 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center shadow-md">
                    <span className="text-white font-semibold text-sm">
                      {completionPercentage}%
                    </span>
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-800 dark:text-white">
                      Profile Completion
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-300">
                      {completedFields}/{totalRequiredFields} fields completed
                    </p>
                  </div>
                </div>
                <Badge
                  variant="secondary"
                  className="bg-gradient-to-r from-blue-100 to-purple-100 text-blue-800 dark:from-blue-900/50 dark:to-purple-900/50 dark:text-blue-200 border-blue-200/60 dark:border-blue-700/30 px-3 py-1 text-xs font-semibold"
                >
                  Step 1 of 5
                </Badge>
              </div>

              <div className="w-full h-2 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden mb-2">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-700 ease-out"
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>

              {completionPercentage < 100 && (
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Complete all required fields to continue to the next step
                </p>
              )}
              {completionPercentage === 100 && (
                <p className="text-xs text-green-600 dark:text-green-400 font-medium">
                  ✓ All required fields completed! Ready to continue
                </p>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="border-0 shadow-xl bg-white dark:bg-slate-800 overflow-hidden">
            <CardContent className="p-8">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="space-y-8"
                >
                  {/* Profile Picture Section */}
                  <div className="flex flex-col items-center space-y-4 pb-8 border-b border-slate-200/60 dark:border-slate-700/50">
                    <div className="text-center mb-4">
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-2">
                        Profile Picture
                      </h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        Add a professional photo to personalize your profile
                      </p>
                    </div>
                    <FormField
                      control={form.control}
                      name="profile_picture"
                      render={({ field }) => (
                        <FormItem className="flex flex-col items-center">
                          <FormControl>
                            <div className="relative group">
                              <div className="w-28 h-28 rounded-full border-4 border-slate-200/80 dark:border-slate-600/60 overflow-hidden bg-gradient-to-br from-slate-100 to-slate-200 dark:from-slate-700 dark:to-slate-600 flex items-center justify-center transition-all duration-300 group-hover:scale-105 group-hover:shadow-lg">
                                {imagePreview || field.value ? (
                                  <Image
                                    src={imagePreview || field.value || ''}
                                    alt="Profile"
                                    width={112}
                                    height={112}
                                    className="w-full h-full object-cover"
                                  />
                                ) : (
                                  <Camera className="w-10 h-10 text-slate-400 dark:text-slate-500" />
                                )}
                              </div>
                              <label className="absolute -bottom-2 -right-2 w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 shadow-lg hover:shadow-xl">
                                <Upload className="w-5 h-5 text-white" />
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
                              <div className="absolute -inset-2 bg-gradient-to-r from-blue-400/10 to-purple-400/10 rounded-full blur-sm group-hover:blur-md transition-all duration-300"></div>
                            </div>
                          </FormControl>
                          {isUploading && (
                            <p className="text-xs text-blue-600 dark:text-blue-400 mt-2">
                              Uploading...
                            </p>
                          )}
                        </FormItem>
                      )}
                    />
                  </div>
                  
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-2">
                        Personal Information
                      </h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        Tell us about yourself
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <FormField
                        control={form.control}
                        name="first_name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                              <User className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                              First Name
                            </FormLabel>
                            <FormControl>
                              <Input
                                placeholder="Enter your first name"
                                {...field}
                                className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80"
                              />
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
                            <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                              <User className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                              Last Name
                            </FormLabel>
                            <FormControl>
                              <Input
                                placeholder="Enter your last name"
                                {...field}
                                className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80"
                              />
                            </FormControl>
                            <FormMessage className="text-xs" />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="professional_title"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                            <FileText className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                            Professional Title
                          </FormLabel>
                          <Select
                            onValueChange={field.onChange}
                            defaultValue={field.value}
                          >
                            <FormControl>
                              <SelectTrigger className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80">
                                <SelectValue placeholder="Select your professional title" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent className="max-h-60 bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700">
                              {PROFESSIONAL_TITLES.map(title => (
                                <SelectItem
                                  key={title}
                                  value={title}
                                  className="py-3 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
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
                  </div>

                  {/* Contact Information Section */}
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-2">
                        Contact Information
                      </h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        How can we reach you?
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <FormField
                        control={form.control}
                        name="contact_number"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                              <Phone className="w-4 h-4 text-green-600 dark:text-green-400" />
                              Contact Number
                            </FormLabel>
                            <FormControl>
                              <PhoneInput
                                country={'ph'}
                                value={field.value}
                                onChange={field.onChange}
                                containerClass="!w-full"
                                inputClass="!w-full !h-12 !bg-white/80 dark:!bg-slate-700/80 !text-foreground !border-slate-300 dark:!border-slate-600 !focus:ring-2 !focus:ring-blue-500 !focus:border-transparent !transition-all"
                                buttonClass="!border-slate-300 dark:!border-slate-600 !bg-white/80 dark:!bg-slate-700/80"
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
                            <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                              <MapPin className="w-4 h-4 text-orange-600 dark:text-orange-400" />
                              Address
                            </FormLabel>
                            <FormControl>
                              <Input
                                placeholder="e.g. Manila, Philippines"
                                {...field}
                                className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80"
                              />
                            </FormControl>
                            <FormMessage className="text-xs" />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="linkedin_url"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                            <Linkedin className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                            LinkedIn URL
                            <Badge
                              variant="secondary"
                              className="text-xs bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300"
                            >
                              Optional
                            </Badge>
                          </FormLabel>
                          <FormControl>
                            <Input
                              placeholder="https://linkedin.com/in/your-profile"
                              {...field}
                              className="h-12 border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white/80 dark:bg-slate-700/80"
                            />
                          </FormControl>
                          <FormMessage className="text-xs" />
                        </FormItem>
                      )}
                    />
                  </div>

                  {/* Professional Summary Section */}
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-2">
                        Professional Summary
                      </h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        Share your story and career aspirations
                      </p>
                    </div>

                    <FormField
                      control={form.control}
                      name="summary"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
                            <FileText className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                            Professional Summary
                          </FormLabel>
                          <FormControl>
                            <Textarea
                              placeholder="Tell us about your professional background, key skills, and career goals. This helps us understand what makes you unique..."
                              {...field}
                              className="min-h-[140px] border-slate-300 dark:border-slate-600 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none bg-white/80 dark:bg-slate-700/80"
                              maxLength={500}
                            />
                          </FormControl>
                          <div className="flex justify-between items-center">
                            <FormMessage className="text-xs" />
                            <span className="text-xs text-slate-500 dark:text-slate-400">
                              {field.value?.length || 0}/500
                            </span>
                          </div>
                        </FormItem>
                      )}
                    />
                  </div>

                  {apiError && (
                    <div className="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                      <p className="text-sm text-red-600 dark:text-red-400">
                        {apiError}
                      </p>
                    </div>
                  )}

                  <div className="pt-6 border-t border-slate-200/60 dark:border-slate-700/50">
                    <Button
                      type="submit"
                      disabled={
                        form.formState.isSubmitting ||
                        completionPercentage < 100
                      }
                      className="w-full h-14 text-base font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 dark:disabled:from-slate-600 dark:disabled:to-slate-700 transition-all duration-300 flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
                    >
                      {form.formState.isSubmitting ? (
                        <>
                          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          Saving Profile...
                        </>
                      ) : (
                        <>
                          Continue to Education
                          <ArrowRight className="w-5 h-5" />
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
