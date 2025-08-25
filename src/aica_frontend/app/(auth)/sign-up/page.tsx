'use client';

import { motion } from 'motion/react';
import Link from 'next/link';
import Image from 'next/image';
import React from 'react';
import RegisterForm from '@/components/RegisterForm';

export default function SignupPage() {
  return (
    <div className="relative min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      {/* Enhanced gradient background matching login page */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        {/* Sophisticated gradient layers */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/20 dark:from-slate-900 dark:via-blue-950/20 dark:to-purple-950/10"></div>
        
        {/* Animated gradient orbs with enhanced colors */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-blue-400/20 via-purple-400/15 to-pink-400/10 rounded-full blur-3xl opacity-60 animate-pulse"></div>
        <div className="absolute top-1/3 left-0 w-80 h-80 bg-gradient-to-br from-cyan-400/15 via-teal-400/10 to-emerald-400/5 rounded-full blur-3xl opacity-50 animate-pulse" style={{animationDelay: '1.5s'}}></div>
        <div className="absolute bottom-0 right-1/4 w-72 h-72 bg-gradient-to-tl from-violet-400/15 via-purple-400/10 to-fuchsia-400/5 rounded-full blur-3xl opacity-50 animate-pulse" style={{animationDelay: '2.5s'}}></div>
        
        {/* Subtle animated mesh gradient */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100/10 via-transparent to-purple-100/10 dark:from-blue-900/10 dark:via-transparent dark:to-purple-900/10"></div>
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-pink-100/10 via-transparent to-orange-100/10 dark:from-pink-900/10 dark:via-transparent dark:to-orange-900/10"></div>
        
        {/* Enhanced subtle pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#8882_1px,transparent_1px),linear-gradient(to_bottom,#8882_1px,transparent_1px)] bg-[size:20px_30px] opacity-10"></div>
      </div>
      
      <div className="flex-1 container mx-auto px-4 py-16 md:py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-md mx-auto"
        >
          <div className="text-center mb-8">
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-6"
            >
              <Image
                src="/aica-square-black-color.png"
                alt="AICA Logo"
                width={80}
                height={80}
                className="mx-auto mb-4"
                priority
              />
            </motion.div>
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-800 dark:text-slate-100 mb-2">
              Join <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">AICA</span>
            </h1>
            <p className="text-lg text-slate-600 dark:text-slate-300">
              Create your account to get started
            </p>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8 backdrop-blur-sm"
          >
            <RegisterForm />
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-700"
            >
              <p className="text-sm text-center text-slate-600 dark:text-slate-300">
                Already have an account?{" "}
                <Link href="/login" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
                  Log in here
                </Link>
              </p>
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
