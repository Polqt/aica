'use client';

import { motion } from 'motion/react';
import { Navbar } from '@/components/Navbar';
import Image from 'next/image';
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Image from 'next/image';
import { Target, Eye, Sparkles, Rocket } from 'lucide-react';
import Footer from '@/components/Footer';


export default function AboutPage() {
  const authors = [
    {
      name: 'April Faith J. Gamboa',
      role: 'Research/ Frontend Developer',
      role: 'Researcher',
    },
    {
      name: 'Janpol S. Hidalgo',
      role: 'Full-Stack Developer/ Database Administrator',
    },
    {
      name: 'Heidine Marie J. Mahandog',
      role: 'Graphics/ Frontend Developer',
      role: 'Graphics',
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
    <div className="relative min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
    <div className="relative min极-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      <Navbar />
      
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/4 top-1/4 h-64 w-64 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl"></div>
        <div className="absolute right-1/4 top-1/3 h-48 w-48 rounded-full bg-gradient-to-br from-pink-400/20 to-orange-400/20 blur-3xl"></div>
        <div className="absolute left-1/4 top-极/4 h-64 w-64 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl"></div>
        <div className="absolute right-1/4 top-1/3 h-48 w-48 rounded-full bg-gradient-to极r from-pink-400/20 to-orange-400/20 blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/3 h-56 w-56 rounded-full bg-gradient-to-br from-green-400/20 to-cyan-400/20 blur-3xl"></div>
      </div>
      
      <div className="flex-1 container mx-auto px-4 py-16 md:py-24">
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
        <div
          className="mx-auto max-w-4xl text-center mb-16 md:mb-20"
        >
          <h1 
            className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-slate-800 dark:text-slate-100 mb-6"
          >
            <div className="flex justify-center">
              <Image
                src="/aica-square-color.png"
                alt="AICA Logo"
                width={100} 
                height={100}
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
      

        {/* Main Content Grid */}
        <div className="max-w-6xl mx-auto space-y-16 md:space-y-20">
          
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
              <div className="relative w-full h-full transition-transform duration-700 ease-in-out group-hover:[transform:rotateY(180deg)]" style={{ transformStyle: 'preserve-3d' }}>
                
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
                <div className="absolute inset-0 w-full h-full [transform:rotateY(180deg)]" style={{ backfaceVisibility: 'hidden' }}>
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

          {/* Purpose Section - Enhanced with Subtle Background Design */}
          <motion.section
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
            className="relative max-w-4xl mx-auto px-6 py-20"
          >
            {/* Subtle background design elements */}
            <div className="absolute inset-0 -z-10 overflow-hidden">
              {/* Soft gradient base */}
              <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-950 dark:to-slate-900 opacity-60" />
              
              {/* Floating geometric shapes - subtle */}
              <div className="absolute top-1/4 left-1/4 h-32 w-32 rounded-full bg-gradient-to-br from-blue-400/5 to-purple-400/5 blur-2xl animate-pulse" />
              <div 
                className="absolute bottom-1/3 right-1/4 h-24 w-24 rounded-lg bg-gradient-to-tr from-pink-400/5 to-orange-400/5 blur-2xl animate-pulse"
                style={{ animationDelay: '1s' }} 
              />
              <div 
                className="absolute top-2/3 left-1/3 h-20 w-20 rounded-full bg-gradient-to-bl from-green-400/5 to-cyan-400/5 blur-2xl animate-pulse"
                style={{ animationDelay: '2s' }} 
              />
              
              {/* Subtle grid pattern */}
              <div className="absolute inset-0 opacity-[0.015] dark:opacity-[0.03]">
                <div 
                  className="h-full w-full"
                  style={{
                    backgroundImage: `radial-gradient(circle at 1px 1px, rgb(148 163 184) 1px, transparent 1px)`,
                    backgroundSize: '20px 20px'
                  }} 
                />
              </div>
            </div>

            <div className="space-y-8 text-lg leading-relaxed text-slate-700 dark:text-slate-200">
              {[
                "The primary goal of this study is to design and evaluate the AI Career Assistant (AICA), a job-matching platform that combines Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG). It seeks to close the gap between the skills of technology graduates and the requirements of today's job market.Through a structured resume-building process and AI-driven job matching, AICA helps graduating students and recent graduates present their skills more effectively and discover opportunities that match their strengths and aspirations.",
                "This research also addresses the shortcomings of conventional job portals by offering an intelligent, user-centered system that promotes more accurate and efficient job matching in the technology sector."
              ].map((text, index) => (
                <motion.p
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.25 }}
                >
                  {text}
                </motion.p>
              ))}
            </div>
          </motion.section>

          {/* Team Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="text-center"
          >
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                Meet the Team
              </h2>
              {/* Gradient accent line */}
              <div className="h-1 w-20 mx-auto rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
            </motion.div>

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
                    <div className="relative mx-auto mb-4 h-48 w-48 rounded-full overflow-hidden bg-gradient-to-br from-blue-500 to-purple-500 shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:scale-105">
                      <Image
                        src={photoSrc}
                        alt={author.name}
                        fill
                        className="object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
                        sizes="192px"
                      />
                    </div>
                    <h3 className="text-xl font-semibold text-slate-800 dark:text-slate-100 mb-1 transition-colors duration-300 group-hover:text-blue-600 dark:group-hover:text-blue-400">
                      {author.name}
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 transition-colors duration-300 group-hover:text-slate-700 dark:group-hover:text-slate-300">
                      {author.role}
                    </p>
                  </motion.div>
                );
              })}
            </div>
          </motion.section>

          {/* Mission & Vision Combined Section */}
          <motion.section
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="relative"
          >
            <div className="relative grid lg:grid-cols-2 gap-8 lg:gap-12">
              {/* Mission Card */}
              <motion.div
                initial={{ opacity: 0, x: -100, scale: 0.8 }}
                whileInView={{ opacity: 1, x: 0, scale: 1 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ 
                  duration: 0.8, 
                  delay: 0.2,
                  ease: "easeOut",
                  type: "spring",
                  stiffness: 100
                }}
                className="group"
              >
                <Card className="h-full border border-blue-200 dark:border-blue-800 bg-white dark:bg-gray-900 shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden rounded-2xl">
                  
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.5 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                  >
                    <CardHeader className="pb-4">
                      <div className="flex items-center space-x-4">
                        <motion.div 
                          initial={{ scale: 0, rotate: -180 }}
                          whileInView={{ scale: 1, rotate: 0 }}
                          viewport={{ once: true, amount: 0.5 }}
                          transition={{ duration: 0.6, delay: 0.6, type: "spring", stiffness: 200 }}
                          className="p-3 rounded-xl bg-blue-100 dark:bg-blue-900 overflow-hidden"
                        >
                          <img 
                            src="aica-square-black-color.png" 
                            alt="Mission Icon" 
                            className="w-8 h-8 object-cover"
                          />
                        </motion.div>
                        <div>
                          <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, amount: 0.5 }}
                            transition={{ duration: 0.6, delay: 0.7 }}
                          >
                            <CardTitle className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                              Our Mission
                            </CardTitle>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Purpose & Commitment</p>
                          </motion.div>
                        </div>
                      </div>
                    </CardHeader>
                  </motion.div>
                  
                  <CardContent className="space-y-4">
                    <motion.div 
                      initial={{ opacity: 0, y: 30 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 0.8 }}
                      className="relative"
                    >
                      <div className="absolute -left-4 top-0 text-6xl text-blue-200 dark:text-blue-800 font-serif">"</div>
                      <p className="text-lg leading-relaxed text-gray-700 dark:text-gray-300 pl-6">
                        We are Nyx Arcana, a group of third-year Computer Science students from the University of St. La Salle – Bacolod. As part of our undergraduate thesis requirement, we present to you our successfully deployed project titled AICA (AI Career Assistant): A Job Matching Platform Using a Large Language Model with Retrieval-Augmented Generation.
                      </p>
                    </motion.div>
                    
                    <motion.div 
                      initial={{ opacity: 0, scale: 0.9 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 1.0 }}
                      className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950 dark:to-purple-950 rounded-xl p-4 border border-blue-200 dark:border-blue-800"
                    >
                      <p className="text-gray-800 dark:text-gray-200 font-medium">
                        Our mission is to provide an innovative, intelligent, and user-friendly tool that guides students and graduates in building strong resumes, identifying their skills, and connecting them to relevant career opportunities.
                      </p>
                    </motion.div>
                    
                    <motion.div 
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 1.2 }}
                      className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400"
                    >
                      <Sparkles className="w-4 h-4 text-blue-500" />
                      <span>Powered by cutting-edge AI technology</span>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Vision Card */}
              <motion.div
                initial={{ opacity: 0, x: 100, scale: 0.8 }}
                whileInView={{ opacity: 1, x: 0, scale: 1 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ 
                  duration: 0.8, 
                  delay: 0.4,
                  ease: "easeOut",
                  type: "spring",
                  stiffness: 100
                }}
                className="group"
              >
                <Card className="h-full border border-blue-200 dark:border-blue-800 bg-white dark:bg-gray-900 shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden rounded-2xl">
                  
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.5 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                  >
                    <CardHeader className="pb-4">
                      <div className="flex items-center space-x-4">
                        <motion.div 
                          initial={{ scale: 0, rotate: 180 }}
                          whileInView={{ scale: 1, rotate: 0 }}
                          viewport={{ once: true, amount: 0.5 }}
                          transition={{ duration: 0.6, delay: 0.8, type: "spring", stiffness: 200 }}
                          className="p-3 rounded-xl bg-purple-100 dark:bg-purple-900 overflow-hidden"
                        >
                          <img 
                            src="aica-square-black-color.png" 
                            alt="Vision Icon" 
                            className="w-8 h-8 object-cover"
                          />
                        </motion.div>
                        <div>
                          <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, amount: 0.5 }}
                            transition={{ duration: 0.6, delay: 0.9 }}
                          >
                            <CardTitle className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                              Our Vision
                            </CardTitle>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Future & Impact</p>
                          </motion.div>
                        </div>
                      </div>
                    </CardHeader>
                  </motion.div>
                  
                  <CardContent className="space-y-4">
                    <motion.div 
                      initial={{ opacity: 0, y: 30 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 1.0 }}
                      className="relative"
                    >
                      <div className="absolute -left-4 top-0 text-6xl text-purple-200 dark:text-purple-800 font-serif">"</div>
                      <p className="text-lg leading-relaxed text-gray-700 dark:text-gray-300 pl-6">
                        To empower students and graduates with accessible, AI-driven career assistance by bridging the gap between academic learning and industry demands.
                      </p>
                    </motion.div>
                    
                    <motion.div 
                      initial={{ opacity: 0, scale: 0.9 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 1.2 }}
                      className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-950 dark:to-blue-950 rounded-xl p-4 border border-purple-200 dark:border-purple-800"
                    >
                      <p className="text-gray-800 dark:text-gray-200 font-medium">
                        AICA envisions a future where every graduate seamlessly connects with opportunities that match their skills, potential, and aspirations—helping them thrive in a competitive job market.
                      </p>
                    </motion.div>
                    
                    <motion.div 
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true, amount: 0.5 }}
                      transition={{ duration: 0.6, delay: 1.4 }}
                      className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400"
                    >
                      <Rocket className="w-4 h-4 text-purple-500" />
                      <span>Shaping the future of career development</span>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </motion.section>

          {/* Hero Image Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="relative z-10 mb-16 md:mb-20"
          >
            <div className="max-w-5xl mx-auto">
              <motion.div 
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className="rounded-2xl border border-neutral-200 bg-white p-4 shadow-xl dark:border-neutral-800 dark:bg-neutral-900 cursor-pointer"
              >
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
              </motion.div>
            </div>
          </motion.div>

          {/* Special Thanks Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.8 }}
            className="max-w-4xl mx-auto text-center py-16"
          >
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7 }}
              className="mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                Special Thanks to
              </h2>
              {/* Gradient accent line */}
              <div className="h-1 w-20 mx-auto rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
            </motion.div>

            {/* People list */}
            <div className="space-y-4">
              {specialThanks.map((person, index) => (
                <motion.div
                  key={person}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.3, delay: 0.9 + index * 0.1 }}
                  className="flex items-center justify-center space-x-3"
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
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="max-w-3xl mx-auto text-center py-20"
          >
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mb-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                Interested in Collaborating?
              </h2>
              <div className="h-1 w-20 mx-auto rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
            </motion.div>

            {/* Text */}
            <p className="text-lg text-slate-600 dark:text-slate-300 mb-8 max-w-2xl mx-auto">
              Want to help us improve <span className="font-semibold text-slate-800 dark:text-slate-100">AICA</span> and turn it into a full job-finding app?  
              Get in touch with us at:
            </p>

            {/* Contact Email Button */}
            <motion.a
              href="mailto:nyxarcanastudios123@gmail.com"
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="inline-flex items-center space-x-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 px-6 py-3 text-white font-medium shadow-lg transition-transform duration-200 hover:scale-105"
            >
              <span>📧</span>
              <span>nyxarcanastudios123@gmail.com</span>
            </motion.a>
          </motion.section>


        </div>
      </div>
      
      {/* Footer Section */}
      <motion.footer
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.0 }}
        className="border-t border-slate-200 dark:border-slate-700 pt-12 text-center"
      >
        <div className="max-w-4xl mx-auto space-y-8">
          <div>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
              This research paper is part of an undergraduate research paper by Gamboa, Hidalgo, Mahandog, Santia for University of Saint La Salle - College of Computing Studies.
            </p>
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
              All Rights Reserved.
            </p>
          </div>
          
          <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 1.1 }}
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
              transition={{ duration: 0.5, delay: 1.2 }}
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
      <div className="pb-16">
        <Footer />
      </div>
          </h1>
          
          <p
            className="text-lg md:text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto leading-relaxed"
          >
            Empowering tech graduates to find their perfect career match through intelligent AI-powered job matching
          </p>
        </div>

        {/* Authors Section */}
        <div className="max-w-6xl mx-auto space-y-16 md:space-y-20">
          <h2 className="text-2xl font-bold text-center">Meet the Authors</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {authors.map((author) => (
              <div key={author.name} className="text-center">
                <h3 className="font-semibold">{author.name}</h3>
                <p>{author.role}</p>
              </div>
            ))}
          </div>

          {/* Special Thanks Section */}
          <h2 className="text-2xl font-bold text-center">Special Thanks</h2>
          <ul className="list-disc list-inside">
            {specialThanks.map((thanks, index) => (
              <li key={index}>{thanks}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
