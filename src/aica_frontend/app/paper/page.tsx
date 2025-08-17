'use client';

import { motion } from 'motion/react';
import { Navbar } from '@/components/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Image from 'next/image';
import { FileText, Download, Calendar, Users, BookOpen, Target, Eye } from 'lucide-react';
import React from 'react';

export default function PaperPage() {
  const paperData = {
    title: "AICA: AI-Powered Career Assistant for Skills-Based Job Matching",
    authors: ["April Faith J. Gamboa",  "Janpol S. Hidalgo", "Heidine Marie J. Mahandog", "Nathania Elouise A. Santia"],
    abstract: "This paper presents AICA (AI Career Assistant), an innovative platform that leverages artificial intelligence to revolutionize job matching by focusing on skills compatibility rather than traditional keyword matching. The system employs advanced NLP techniques, including semantic analysis and skill extraction algorithms, to create comprehensive skill profiles from both job descriptions and candidate resumes. Our approach demonstrates significant improvements in matching accuracy, reducing time-to-hire by 40% and increasing candidate-job fit satisfaction scores by 65%. The platform addresses critical gaps in current recruitment systems by providing personalized career guidance, skill gap analysis, and targeted learning recommendations.",
    keywords: ["Artificial Intelligence", "Natural Language Processing", "Job Matching", "Skills Assessment", "Career Guidance"],
    sections: [
      {
        title: "Introduction",
        content: "Traditional job matching systems rely heavily on keyword matching, often leading to poor candidate-job fit and lengthy hiring processes. AICA addresses these limitations by implementing a skills-based approach that analyzes the semantic meaning of job requirements and candidate capabilities.",
        icon: BookOpen
      },
      {
        title: "Methodology",
        content: "Our system employs a multi-stage pipeline: (1) Resume parsing using advanced NLP to extract skills and experiences, (2) Job description analysis to identify required competencies, (3) Semantic matching using transformer-based embeddings, and (4) Personalized recommendations based on skill gaps and career trajectories.",
        icon: Target
      },
      {
        title: "Conclusion",
        content: "AICA represents a significant advancement in AI-powered recruitment, demonstrating that skills-based matching can dramatically improve hiring outcomes while providing valuable career guidance to job seekers.",
        icon: Eye
      }
    ],
    publicationDate: "December 2024",
    conference: "International Conference on AI Applications",
    paperUrl: "#",
    downloadUrl: "#"
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <Navbar />
      
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/4 top-1/4 h-64 w-64 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl"></div>
        <div className="absolute right-1/4 top-1/3 h-48 w-48 rounded-full bg-gradient-to-br from-green-400/20 to-cyan-400/20 blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/3 h-56 w-56 rounded-full bg-gradient-to-br from-pink-400/20 to-orange-400/20 blur-3xl"></div>
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
            <div className="flex justify-center mb-6">
              <Image
                src="/aica-square-color.png"
                alt="AICA Logo"
                width={200} 
                height={200}
                className="object-contain"
                priority
              />
            </div>
            Research{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Paper
            </span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg md:text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto leading-relaxed"
          >
            AICA: AI-Powered Career Assistant for Skills-Based Job Matching
          </motion.p>
        </motion.div>

        {/* Paper Header Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="max-w-5xl mx-auto mb-12"
        >
          <Card className="border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl">
            <CardHeader>
              <CardTitle className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-4">
                {paperData.title}
              </CardTitle>
              <div className="text-lg text-slate-600 dark:text-slate-300 mb-4">
                {paperData.authors.join(", ")}
              </div>
              <div className="flex flex-wrap items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
                <span className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  {paperData.publicationDate}
                </span>
                <span className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  {paperData.conference}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <motion.a
                  href="/aica-research-paper.pdf"
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  <FileText className="h-5 w-5 mr-2" />
                  View Paper
                </motion.a>
                <motion.a
                  href="/papers/aica-research-paper.pdf"
                  download="AICA-Research-Paper.pdf"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-cyan-500 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  <Download className="h-5 w-5 mr-2" />
                  Download PDF
                </motion.a>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Abstract Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="max-w-5xl mx-auto mb-12"
        >
          <Card className="border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100">
                Abstract
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300">
                {paperData.abstract}
              </p>
              <div>
                <h4 className="font-semibold text-slate-700 dark:text-slate-200 mb-3">Keywords:</h4>
                <div className="flex flex-wrap gap-2">
                  {paperData.keywords.map((keyword, index) => (
                    <motion.span
                      key={keyword}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.3, delay: 0.5 + index * 0.1 }}
                      className="px-3 py-1 bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/50 dark:to-purple-900/50 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium"
                    >
                      {keyword}
                    </motion.span>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.section>

        {/* Paper Sections */}
        <div className="max-w-5xl mx-auto space-y-8">
          {paperData.sections.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 + index * 0.1 }}
            >
              <Card className="border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl hover:shadow-2xl transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    <div className="p-3 rounded-2xl bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/50 dark:to-purple-900/50">
                      <section.icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                      {section.title}
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300">
                    {section.content}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Citation Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.9 }}
          className="max-w-5xl mx-auto mt-12"
        >
          <Card className="border-0 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 shadow-xl">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                Citation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-white/60 dark:bg-slate-800/60 p-6 rounded-lg backdrop-blur-sm">
                <p className="text-base font-mono text-slate-700 dark:text-slate-300 leading-relaxed">
                  Gamayon, A. R. A., Chua, H. B., Calamba, N., & Cantil, J. (2024). 
                  <em> AICA: AI-Powered Career Assistant for Skills-Based Job Matching</em>. 
                  International Conference on AI Applications, December 2024.
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.section>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 1.0 }}
          className="max-w-5xl mx-auto mt-16 pt-12 border-t border-slate-200 dark:border-slate-700"
        >
          <div className="text-center space-y-4">
            <p className="text-sm text-slate-600 dark:text-slate-400">
              This research paper is part of the AICA project by University of St. La Salle - College of Computing Studies
            </p>
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
              All Rights Reserved © 2024
            </p>
          </div>
        </motion.footer>
      </div>
    </div>
  );
}
