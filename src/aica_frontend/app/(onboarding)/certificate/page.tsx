'use client';

import CertificateCard from '@/components/CertificateCard';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import { FormProvider, useFieldArray, useForm } from 'react-hook-form';
import z from 'zod';
import { toast } from 'sonner';
import {
  Plus,
  Award,
  ArrowRight,
  FileText,
  Lightbulb,
  AlertCircle,
} from 'lucide-react';
import { motion } from 'motion/react';

const certificateItemSchema = z.object({
  name: z.string().optional(),
  issuing_organization: z.string().optional(),
  issue_date: z.string().optional(),
  credential_url: z
    .string()
    .optional()
    .refine(
      val => !val || val === '' || z.string().url().safeParse(val).success,
      {
        message: 'Invalid URL format',
      },
    ),
  credential_id: z.string().optional(),
});

const certificateFormSchema = z.object({
  certificates: z.array(certificateItemSchema),
});

export default function Certificate() {
  const router = useRouter();
  const { updateData, submitOnboardingData } = useOnboarding();
  const [apiError, setApiError] = useState<string | null>(null);
  const [expandedIndexes, setExpandedIndexes] = useState<number[]>([0]);

  const form = useForm<z.infer<typeof certificateFormSchema>>({
    resolver: zodResolver(certificateFormSchema),
    defaultValues: {
      certificates: [
        {
          name: '',
          issuing_organization: '',
          issue_date: '',
          credential_url: '',
          credential_id: '',
        },
      ],
    },
    mode: 'onBlur',
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'certificates',
  });

  const toggleExpand = (index: number) => {
    setExpandedIndexes(prev =>
      prev.includes(index) ? prev.filter(i => i !== index) : [...prev, index],
    );
  };

  const addCertificate = () => {
    if (fields.length >= 10) {
      toast.error('Maximum limit reached', {
        description: 'You can add up to 10 certificates only.',
      });
      return;
    }

    append({
      name: '',
      issuing_organization: '',
      issue_date: '',
      credential_url: '',
      credential_id: '',
    });

    setExpandedIndexes(prev => [...prev, fields.length]);

    toast.success('New certificate record added!', {
      description: 'Fill in the details for your new certificate.',
    });
  };

  async function onSubmit(values: z.infer<typeof certificateFormSchema>) {
    setApiError(null);
    form.clearErrors();

    const validCertificates = values.certificates.filter(
      cert =>
        cert.name &&
        cert.name.trim() !== '' &&
        cert.issuing_organization &&
        cert.issuing_organization.trim() !== '',
    );

    const cleanCertificates = JSON.parse(JSON.stringify(validCertificates));
    updateData({ certificates: cleanCertificates });

    try {
      await submitOnboardingData();

      if (validCertificates.length > 0) {
        toast.success('Certificates Saved!', {
          description: `Successfully added ${
            validCertificates.length
          } certificate${
            validCertificates.length > 1 ? 's' : ''
          }. Your profile is now complete!`,
          duration: 3000,
        });
      } else {
        toast.success('Profile Completed!', {
          description: 'Your profile has been created successfully!',
          duration: 3000,
        });
      }

      setTimeout(() => {
        router.push('/dashboard');
      }, 1000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';

      setApiError(errorMessage);
      toast.error('Certificate Update Failed', {
        description: errorMessage,
        duration: 5000,
      });
    }
  }

  const skipCertificates = () => {
    updateData({ certificates: [] });

    toast.info('Skipping Certificates', {
      description:
        'No worries! You can add certificates later from your profile.',
      duration: 3000,
    });

    setTimeout(() => {
      router.push('/dashboard');
    }, 1000);
  };

  const watchedCertificates = form.watch('certificates');
  const totalFields = watchedCertificates.length * 5; // 5 fields per certificate
  const completedFields = watchedCertificates.reduce((acc, cert) => {
    let completed = 0;
    if (cert.name?.trim()) completed++;
    if (cert.issuing_organization?.trim()) completed++;
    if (cert.issue_date?.trim()) completed++;
    if (cert.credential_id?.trim()) completed++;
    if (cert.credential_url?.trim()) completed++;
    return acc + completed;
  }, 0);
  const completionPercentage =
    totalFields > 0 ? Math.round((completedFields / totalFields) * 100) : 0;

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/40 to-purple-50/30 dark:from-slate-900 dark:via-blue-900/20 dark:to-purple-900/15 py-8 px-4 overflow-hidden">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50/20 via-indigo-50/15 to-purple-50/25 dark:from-blue-900/10 dark:via-indigo-900/8 dark:to-purple-900/12"></div>

        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 2, ease: 'easeOut' }}
          className="absolute left-[15%] top-[20%] h-96 w-96 rounded-full bg-gradient-to-br from-blue-300/25 to-purple-300/20 dark:from-blue-700/15 dark:to-purple-700/12 blur-3xl animate-float-slow"
        />
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 2, delay: 0.3, ease: 'easeOut' }}
          className="absolute right-[20%] top-[30%] h-80 w-80 rounded-full bg-gradient-to-br from-pink-300/20 to-orange-300/15 dark:from-pink-700/12 dark:to-orange-700/10 blur-3xl animate-float-medium"
        />
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 2, delay: 0.6, ease: 'easeOut' }}
          className="absolute bottom-[25%] left-[25%] h-88 w-88 rounded-full bg-gradient-to-br from-green-300/30 to-cyan-300/20 dark:from-green-700/18 dark:to-cyan-700/15 blur-3xl animate-float-fast"
        />

        <div className="absolute inset-0 opacity-15 dark:opacity-10">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        </div>

        <div className="absolute top-0 left-0 w-48 h-48 bg-gradient-to-br from-blue-400/10 to-transparent rounded-full blur-xl"></div>
        <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-purple-400/10 to-transparent rounded-full blur-xl"></div>
        <div className="absolute bottom-0 left-0 w-36 h-36 bg-gradient-to-tr from-indigo-400/10 to-transparent rounded-full blur-xl"></div>
        <div className="absolute bottom-0 right-0 w-44 h-44 bg-gradient-to-tl from-pink-400/10 to-transparent rounded-full blur-xl"></div>

        <div className="absolute inset-0">
          {[
            { left: 10, top: 20, duration: 4, delay: 0.5 },
            { left: 80, top: 30, duration: 5, delay: 1.0 },
            { left: 25, top: 70, duration: 6, delay: 1.5 },
            { left: 70, top: 15, duration: 3, delay: 0.2 },
            { left: 40, top: 50, duration: 5, delay: 0.8 },
            { left: 90, top: 60, duration: 4, delay: 1.2 },
            { left: 15, top: 40, duration: 7, delay: 1.8 },
            { left: 60, top: 80, duration: 4, delay: 0.3 },
          ].map((particle, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-gradient-to-r from-blue-400/40 to-purple-400/30 rounded-full"
              initial={{
                opacity: 0,
                x: particle.left - 50,
                y: particle.top - 50,
              }}
              animate={{
                opacity: [0, 0.6, 0],
                x: [particle.left - 50, particle.left - 30, particle.left - 70],
                y: [particle.top - 50, particle.top - 30, particle.top - 70],
              }}
              transition={{
                duration: particle.duration,
                repeat: Infinity,
                delay: particle.delay,
                ease: 'easeInOut',
              }}
              style={{
                left: `${particle.left}%`,
                top: `${particle.top}%`,
              }}
            />
          ))}
        </div>
      </div>

      <div className="max-w-4xl mx-auto">
        {/* Enhanced Header Section */}
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
            <Award className="w-12 h-12 text-white" />
            <div className="absolute -inset-2 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-2xl blur-lg animate-pulse"></div>
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 dark:from-white dark:to-slate-200 bg-clip-text text-transparent mb-4"
          >
            Certifications &{' '}
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 dark:from-blue-300 dark:via-purple-300 dark:to-indigo-300 bg-clip-text text-transparent">
              Achievements
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg text-slate-600 dark:text-slate-300 max-w-md mx-auto leading-relaxed"
          >
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent font-semibold">
              Showcase your professional credentials
            </span>{' '}
            — add certifications that validate your expertise
          </motion.p>
        </motion.div>

        {/* Tips Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Card className="border-0 shadow-lg bg-gradient-to-r from-blue-50/40 via-purple-50/30 to-indigo-50/20 dark:from-blue-900/20 dark:via-purple-900/15 dark:to-indigo-900/10 backdrop-blur-sm mb-6">
            <CardContent className="p-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center shadow-md flex-shrink-0">
                  <Lightbulb className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-800 dark:text-white mb-2">
                    💡 Pro Tips for Certificates
                  </h3>
                  <ul className="text-sm text-slate-600 dark:text-slate-300 space-y-1">
                    <li>• Include industry-recognized certifications</li>
                    <li>• Add online course certificates and badges</li>
                    <li>• Include professional development courses</li>
                    <li>• Add credential URLs for verification</li>
                  </ul>
                </div>
              </div>
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
              <FormProvider {...form}>
                <Form {...form}>
                  <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-8"
                  >
                    {/* Certificate Cards */}
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                          <FileText className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                          Certificates ({fields.length})
                        </h2>
                        {fields.length > 1 && (
                          <Badge variant="outline" className="text-xs">
                            {fields.length}/10 certificates
                          </Badge>
                        )}
                      </div>

                      {fields.map((field, index) => (
                        <CertificateCard
                          key={field.id}
                          index={index}
                          isExpanded={expandedIndexes.includes(index)}
                          toggleExpand={toggleExpand}
                          remove={remove}
                          canRemove={fields.length > 1}
                        />
                      ))}
                    </div>

                    <Card className="border-2 border-dashed border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-600 transition-colors">
                      <CardContent className="p-6">
                        <Button
                          type="button"
                          variant="ghost"
                          onClick={addCertificate}
                          disabled={fields.length >= 10}
                          className="w-full h-16 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 border-0 flex items-center gap-3"
                        >
                          <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                            <Plus className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                          </div>
                          <div className="text-left">
                            <p className="font-medium">
                              Add Another Certificate
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {fields.length >= 10
                                ? 'Maximum limit reached'
                                : 'Professional certifications, online courses, etc.'}
                            </p>
                          </div>
                        </Button>
                      </CardContent>
                    </Card>

                    {apiError && (
                      <div className="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                        <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                        <p className="text-sm text-red-600 dark:text-red-400">
                          {apiError}
                        </p>
                      </div>
                    )}

                    <div className="pt-6 border-t border-slate-200/60 dark:border-slate-700/50">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Button
                          type="button"
                          variant="outline"
                          onClick={skipCertificates}
                          disabled={form.formState.isSubmitting}
                          className="h-14 text-base font-medium border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-all duration-300"
                        >
                          Skip Certificates
                        </Button>
                        <Button
                          type="submit"
                          disabled={form.formState.isSubmitting}
                          className="h-14 text-base font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 dark:disabled:from-slate-600 dark:disabled:to-slate-700 transition-all duration-300 flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
                        >
                          {form.formState.isSubmitting ? (
                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          ) : (
                            <>
                              Complete Profile
                              <ArrowRight className="w-5 h-5" />
                            </>
                          )}
                        </Button>
                      </div>
                      <div className="mt-4">
                        <p className="text-xs text-slate-500 dark:text-slate-400 text-center mb-2">
                          Completion: {completionPercentage}%
                        </p>
                        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${completionPercentage}%` }}
                          />
                        </div>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400 text-center mt-3">
                        Certificates are optional. You can skip this step and
                        add them later.
                      </p>
                    </div>
                  </form>
                </Form>
              </FormProvider>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
