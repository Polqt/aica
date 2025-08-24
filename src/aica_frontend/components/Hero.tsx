'use client';

import { motion } from 'motion/react';
import Image from 'next/image';
import { Navbar } from './Navbar';
import { useRouter } from 'next/navigation';

export function Hero() {
  const router = useRouter();

  const learnMoreButton = () => {
    router.push('/about');
  };

  const getStartedButton = () => {
    router.push('/sign-up');
  };

  const goToPaper = () => {
    router.push('/paper');
  };

  return (
    <div className="relative mx-auto my-10 flex w-full max-w-7xl flex-col items-start justify-start">
      <Navbar />
      <div className="px-4 py-10 md:py-20 w-full">
        <motion.div
          initial={{
            opacity: 0,
            y: -20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.3,
            delay: 0.2,
          }}
          className="text-left"
        >
          <div className="flex items-center mb-3">
            <Image
              src="/aica-square-black-color.png"
              alt="AICA Logo"
              width={40}
              height={40}
              className="mr-2"
            />
            <p className="text-xl font-bold text-purple-600 dark:text-purple-400">
              AI Career Assistant
            </p>
          </div>
          <h1 className="relative z-10 text-left text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tight text-slate-800 dark:text-slate-100 mb-6 leading-tight">
            <span className="text-slate-800 dark:text-slate-100">Find better jobs in</span>{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">minutes,</span>{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">not</span>{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">months</span>
          </h1>
        </motion.div>
        
        <div className="flex flex-col lg:flex-row items-start gap-8 mt-8">
          <div className="flex-1 lg:flex-[1.2]">
            <motion.p
              initial={{
                opacity: 0,
              }}
              animate={{
                opacity: 1,
              }}
              transition={{
                duration: 0.3,
                delay: 0.8,
              }}
              className="relative z-10 text-left text-lg font-normal text-neutral-600 dark:text-neutral-400 mb-6"
            >
              With AICA, you can connect your resume with <br />
              real job opportunities using AI — no gimmicks, <br />
              no guesswork. Just personalized, real-time <br />
              job matching for tech grads like you.
            </motion.p>
            
            <motion.div
              initial={{
                opacity: 0,
              }}
              animate={{
                opacity: 1,
              }}
              transition={{
                duration: 0.3,
                delay: 1,
              }}
              className="relative z-10 mt-8 flex flex-col items-start justify-start gap-4"
            >
              <div className="flex flex-wrap items-start justify-start gap-4">
                <button
                  onClick={getStartedButton}
                  className="relative px-4 py-2 text-neutral-600 dark:text-neutral-300 transition-all duration-200 rounded-full bg-purple-200/90 dark:bg-purple-800/50 border-2 border-purple-500 dark:border-purple-400 font-medium"
                >
                  Get Started
                </button>
                <button
                  onClick={learnMoreButton}
                  className="relative px-4 py-2 text-neutral-600 dark:text-neutral-300 transition-all duration-200 rounded-full bg-white/90 dark:bg-white/95 border border-black/30 dark:border-black/50 font-medium"
                >
                  Learn about AICA
                </button>
              </div>
              
              {/* Paper Preview Box - PDF Document Preview */}
              <motion.div
                initial={{
                  opacity: 0,
                  y: 20,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                transition={{
                  duration: 0.3,
                  delay: 1.2,
                }}
                onClick={goToPaper}
                className="mt-8 cursor-pointer group w-full max-w-md"
              >
                <div className="rounded-xl border border-neutral-200 bg-white dark:bg-neutral-900 dark:border-neutral-800 p-4 shadow-lg hover:shadow-xl transition-all duration-300 group-hover:scale-[1.02]">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-neutral-800 dark:text-neutral-200">AICA Research Paper</h3>
                      <p className="text-xs text-neutral-600 dark:text-neutral-400">
                        Click to view our AI research
                      </p>
                    </div>
                  </div>
                  <div className="relative w-full h-32 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 rounded-lg flex items-center justify-center border border-gray-200 dark:border-gray-700">
                    <div className="text-center">
                      <svg className="w-8 h-8 text-gray-400 dark:text-gray-500 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      <p className="text-xs text-gray-500 dark:text-gray-400">aica-research-paper.pdf</p>
                    </div>
                  </div>
                  <div className="mt-3 pt-3 border-t border-neutral-200 dark:border-neutral-700">
                    <p className="text-xs text-neutral-500 dark:text-neutral-400 italic">
                      "AI-Powered Career Matching: Revolutionizing Job Discovery"
                    </p>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>

          <motion.div
            initial={{
              opacity: 0,
              x: 20,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            transition={{
              duration: 0.5,
              delay: 0.5,
            }}
            className="w-full lg:w-auto lg:flex-[1.5]"
          >
            <div className="rounded-2xl border border-neutral-200 bg-white dark:bg-neutral-900 p-6 shadow-lg">
              <div className="relative w-full aspect-[16/9] overflow-hidden rounded-xl border border-gray-300 dark:border-gray-700">
                <Image
                  src="/students.jpg"
                  alt="Landing page preview"
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 60vw, 50vw"
                />
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
