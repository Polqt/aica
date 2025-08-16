'use client';

import { motion } from 'motion/react';
import { Navbar } from '@/components/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Image from 'next/image';
import { Target, Eye, Sparkles, Rocket } from 'lucide-react';

export default function AboutPage() {
  const authors = [
    {
      name: 'April Faith J. Gamboa',
      role: 'Research/ Frontend Developer',
    },
    {
      name: 'Janpol S. Hidalgo',
      role: 'Full-Stack Developer/ Database Administrator',
    },
    {
      name: 'Heidine Marie J. Mahandog',
      role: 'Graphics/ Frontend Developer',
    },
    {
      name: 'Nathania Elouise A. Santia',
      role: 'Project Manager/Documentation',
    },  
  ];

  const specialThanks = [
    'Julian Diego Mapa - Our ever-supportive Thesis Adviser.',
    'Dr. Eddie de Paula - Our ever-supportive Thesis Co-Adviser.',
    'Dr. Eischeid Arcenal - for his expertise in Artificial Intelligence',
  ];

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Navbar />
      
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/4 top-1/4 h-64 w-64 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl"></div>
        <div className="absolute right-1/4 top-1/3 h-48 w-48 rounded-full bg-gradient-to-br from-pink-400/20 to-orange-400/20 blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/3 h-56 w-56 rounded-full bg-gradient-to-br from-green-400/20 to-cyan-400/20 blur-3xl"></div>
      </div>
      
      <div className="container mx-auto px-4 py-16 md:py-24">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-4xl text-center mb-16 md:mb-20"
        >
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-slate-800 dark:text-slate-100 mb-6"
          >
                   <div className="flex justify-center">
              <Image
                src="/aica-square-color.png"
                alt="AICA Logo"
                width={300} 
                height={300}
                className="object-contain"
                priority
              />
            </div>

            About{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Career Assistant
            </span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg md:text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto leading-relaxed"
          >
            Empowering tech graduates to find their perfect career match through intelligent AI-powered job matching
          </motion.p>
        </motion.div>
      

        {/* Hero Image Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="relative z-10 mb-16 md:mb-20"
        >
          <div className="max-w-5xl mx-auto">
            <div className="rounded-2xl border border-neutral-200 bg-white p-4 shadow-xl dark:border-neutral-800 dark:bg-neutral-900">
              <div className="w-full overflow-hidden rounded-xl">
                <Image
                  src="/team-photo.jpg"
                  alt="AICA Team"
                  className="h-auto w-full object-cover object-center"
                  height={600}
                  width={1200}
                  priority
                />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Main Content Grid */}
        <div className="max-w-6xl mx-auto space-y-16 md:space-y-20">
          
          {/* Mission & Vision Combined Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-transparent to-purple-50 dark:from-blue-900/10 dark:to-purple-900/10 rounded-3xl blur-3xl"></div>
            
            <div className="relative grid lg:grid-cols-2 gap-8 lg:gap-12">
              {/* Mission Card */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
                className="group"
              >
                <Card className="h-full border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-blue-600"></div>
                  
                  <CardHeader className="pb-4">
                    <div className="flex items-center space-x-4">
                      <div className="p-3 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/50 dark:to-blue-800/50">
                        <Target className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div>
                        <CardTitle className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100">
                          Our Mission
                        </CardTitle>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Purpose & Commitment</p>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    <div className="relative">
                      <div className="absolute -left-4 top-0 text-6xl text-blue-200 dark:text-blue-800/50 font-serif">"</div>
                      <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300 pl-6">
                        We are Nyx Arcana, a group of third-year Computer Science students from the University of St. La Salle – Bacolod. As part of our undergraduate thesis requirement, we present to you our successfully deployed project titled AICA (AI Career Assistant): A Job Matching Platform Using a Large Language Model with Retrieval-Augmented Generation.
                      </p>
                    </div>
                    
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-4">
                      <p className="text-slate-700 dark:text-slate-300 font-medium">
                        Our mission is to provide an innovative, intelligent, and user-friendly tool that guides students and graduates in building strong resumes, identifying their skills, and connecting them to relevant career opportunities.
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-2 text-sm text-slate-500 dark:text-slate-400">
                      <Sparkles className="w-4 h-4 text-blue-500" />
                      <span>Powered by cutting-edge AI technology</span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Vision Card */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.6 }}
                className="group"
              >
                <Card className="h-full border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300 overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 to-purple-600"></div>
                  
                  <CardHeader className="pb-4">
                    <div className="flex items-center space-x-4">
                      <div className="p-3 rounded-2xl bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/50 dark:to-purple-800/50">
                        <Eye className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                      </div>
                      <div>
                        <CardTitle className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100">
                          Our Vision
                        </CardTitle>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Future & Impact</p>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    <div className="relative">
                      <div className="absolute -left-4 top-0 text-6xl text-purple-200 dark:text-purple-800/50 font-serif">"</div>
                      <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300 pl-6">
                        To empower students and graduates with accessible, AI-driven career assistance by bridging the gap between academic learning and industry demands.
                      </p>
                    </div>
                    
                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl p-4">
                      <p className="text-slate-700 dark:text-slate-300 font-medium">
                        AICA envisions a future where every graduate seamlessly connects with opportunities that match their skills, potential, and aspirations—helping them thrive in a competitive job market.
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-2 text-sm text-slate-500 dark:text-slate-400">
                      <Rocket className="w-4 h-4 text-purple-500" />
                      <span>Shaping the future of career development</span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </motion.section>

     {/* Interactive Flip Card AICA Logo Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
            className="max-w-4xl mx-auto"
          >
            <div className="relative mx-auto w-80 h-80 cursor-pointer group" style={{ perspective: '1000px' }}>
              {/* Background glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-500" />
              
              {/* Flip Card Inner Container */}
              <div className="relative w-full h-full transition-transform duration-700 ease-in-out group-hover:rotate-y-180" style={{ transformStyle: 'preserve-3d' }}>
                
                {/* Front of card */}
                <div className="absolute inset-0 w-full h-full" style={{ backfaceVisibility: 'hidden' }}>
                  <div className="relative bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900 rounded-3xl p-8 shadow-2xl border border-slate-200/50 dark:border-slate-700/50 h-full flex flex-col items-center justify-center">
                    <Image
                      src="/aica-full-color.png"
                      alt="AICA Logo"
                      width={200}
                      height={200}
                      className="object-contain mb-4"
                      priority
                    />
                    <div className="text-center">
                      <p className="text-sm font-medium text-slate-600 dark:text-slate-300">Hover to flip</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Explore AICA features</p>
                    </div>
                  </div>
                </div>

                {/* Back of card */}
                <div className="absolute inset-0 w-full h-full rotate-y-180" style={{ backfaceVisibility: 'hidden' }}>
                  <div className="relative bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-slate-800 dark:to-slate-900 rounded-3xl p-6 shadow-2xl border border-slate-200/50 dark:border-slate-700/50 h-full flex flex-col">
                    <h3 className="text-lg font-bold text-center mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                      AICA Features
                    </h3>
                    <div className="space-y-2 flex-1">
                      {[
                        {
                          icon: "🤖",
                          title: "AI-Powered Matching",
                          description: "Advanced algorithms find your perfect career matches"
                        },
                        {
                          icon: "📄",
                          title: "Smart Resume Builder",
                          description: "Create professional resumes with AI guidance"
                        },
                        {
                          icon: "📊",
                          title: "Skill Analysis Engine",
                          description: "Get detailed insights about your technical skills"
                        }
                      ].map((feature, index) => (
                        <div key={index} className="bg-white/60 dark:bg-slate-700/60 p-2 rounded-lg backdrop-blur-sm">
                          <div className="flex items-start space-x-2">
                            <span className="text-lg mt-0.5">{feature.icon}</span>
                            <div className="flex-1">
                              <h4 className="font-semibold text-sm text-slate-800 dark:text-slate-100">{feature.title}</h4>
                              <p className="text-xs text-slate-600 dark:text-slate-300 leading-tight">{feature.description}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="text-center mt-2">
                      <p className="text-xs text-slate-500 dark:text-slate-400">Hover to flip back</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.section>
          {/* Purpose Section - No Box */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="max-w-4xl mx-auto"
          >
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                Project Purpose
              </h2>
              <p className="text-lg text-slate-600 dark:text-slate-300">
                Understanding the core objectives behind AICA's development
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-6 text-lg leading-relaxed text-slate-600 dark:text-slate-300"
            >
              <p>
                📝 The purpose of this study is to develop and evaluate the AI Career Assistant (AICA), a job matching platform that integrates Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) to bridge the gap between the skills of tech graduates and the demands of the modern job market.
              </p>
              
              <p>
                📝By guiding users through a structured resume-building process and making use of AI to match the declared skills with relevant job opportunities, this tool aims to empower graduating students and recent graduates to better articulate their competencies and improve their career alignment.
              </p>
              
              <p>
                📝This study seeks to address the limitations of traditional job portals by introducing an intelligent, user-centered tool that supports an efficient job matching in the tech industry.
              </p>
            </motion.div>
          </motion.section>

          {/* Team Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="text-center"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-12">
              Meet the Team
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-10 max-w-6xl mx-auto">
              {authors.map((author, index) => {
                const photoMap = {
                  'April Faith J. Gamboa': '/april.png',
                  'Janpol S. Hidalgo': '/jepoy.png',
                  'Heidine Marie J. Mahandog': '/heidine.png',
                  'Nathania Elouise A. Santia': '/nathania.png',
                };
                const photoSrc = photoMap[author.name as keyof typeof photoMap] || `/author-${index + 1}.jpg`;
                
                return (
                  <motion.div
                    key={author.name}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.7 + index * 0.1 }}
                    className="group"
                  >
                    <div className="relative mx-auto mb-4 h-48 w-48 rounded-full overflow-hidden bg-gradient-to-br from-blue-500 to-purple-500 shadow-lg group-hover:shadow-xl transition-shadow duration-300">
                      <Image
                        src={photoSrc}
                        alt={author.name}
                        fill
                        className="object-cover"
                        sizes="192px"
                      />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-800 dark:text-slate-100 mb-1">
                      {author.name}
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {author.role}
                    </p>
                  </motion.div>
                );
              })}
            </div>
          </motion.section>

          {/* Special Thanks Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.8 }}
            className="max-w-4xl mx-auto text-center"
          >
            <h3 className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100 mb-8">
              Special Thanks to
            </h3>
            <div className="space-y-4">
              {specialThanks.map((person, index) => (
                <motion.div
                  key={person}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.9 + index * 0.1 }}
                  className="flex items-center justify-center space-x-3 p-3"
                >
                  <span className="text-2xl">👨‍🏫</span>
                  <p className="text-lg text-slate-600 dark:text-slate-300">
                    {person}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.section>

          {/* Collaboration Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 1.0 }}
            className="max-w-2xl mx-auto"
          >
            <Card className="border-neutral-200 bg-gradient-to-br from-blue-50 to-purple-50 shadow-xl dark:border-neutral-700 dark:from-blue-900/20 dark:to-purple-900/20">
              <CardHeader>
                <CardTitle className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100 text-center">
                  Interested in Collaborating?
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-lg text-slate-600 dark:text-slate-300 mb-6">
                  Want to help us improve AICA and make this a job finding app? Contact us at:
                </p>
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 1.2 }}
                  className="inline-flex items-center space-x-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 px-6 py-3 text-white shadow-lg transition-transform duration-200 hover:scale-105"
                >
                  <span>📧</span>
                  <span className="font-medium">nyxarcanastudios123@gmail.com</span>
                </motion.div>
              </CardContent>
            </Card>
          </motion.section>

          {/* Footer Section */}
          <motion.footer
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 1.1 }}
            className="border-t border-neutral-200 dark:border-neutral-700 pt-12 text-center"
          >
            <div className="max-w-4xl mx-auto space-y-8">
              <div>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                  This is part of an undergraduate research paper by Gamboa, Hidalgo, Mahandog, Santia for University of Saint La Salle - College of Computing Studies.
                </p>
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  All Rights Reserved.
                </p>
              </div>
              
              <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 1.2 }}
                  className="flex flex-col items-center"
                >
                  <div className="relative h-24 w-24 md:h-32 md:w-32">
                    <Image
                      src="/usls.png"
                      alt="University of St. La Salle"
                      fill
                      className="object-contain"
                      sizes="128px"
                    />
                  </div>
                </motion.div>
                
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 1.3 }}
                  className="flex flex-col items-center"
                >
                  <div className="relative h-24 w-24 md:h-32 md:w-32">
                    <Image
                      src="/ccs.png"
                      alt="College of Computing Studies"
                      fill
                      className="object-contain"
                      sizes="128px"
                    />
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.footer>
        </div>
      </div>
    </div>
  );
}
