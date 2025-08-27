
'use client';

import { motion } from 'framer-motion';
import { Navbar } from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Image from 'next/image';
import { FileText, Download, Calendar, Users } from 'lucide-react';
import React, { useState } from 'react';

export default function PaperPage() {
  const [showPDF, setShowPDF] = useState(false);
  
  const paperData = {
    title: "AICA: AI-Powered Career Assistant for Skills-Based Job Matching",
    authors: ["Gamboa, A.F.",  "Hidalgo, J.", "Mahandog, H.M.", "Santia, N.E."],
    abstract: "This paper presents AICA (AI Career Assistant), an innovative platform that leverages artificial intelligence to revolutionize job matching by focusing on skills compatibility rather than traditional keyword matching. The system employs advanced NLP techniques, including semantic analysis and skill extraction algorithms, to create comprehensive skill profiles from both job descriptions and candidate resumes. Our approach demonstrates significant improvements in matching accuracy, reducing time-to-hire by 40% and increasing candidate-job fit satisfaction scores by 65%. The platform addresses critical gaps in current recruitment systems by providing personalized career guidance, skill gap analysis, and targeted learning recommendations.",
    keywords: ["Artificial Intelligence", "Natural Language Processing", "Job Matching", "Skills Assessment", "Career Guidance"],
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
                width={100} 
                height={100}
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
              <div className="flex gap-3">
                <motion.button
                  onClick={() => setShowPDF(!showPDF)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium border border-blue-100 dark:border-blue-800/30 transition-all duration-200"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  {showPDF ? 'Hide PDF' : 'View PDF'}
                </motion.button>
                <motion.a
                  href="/aica-research-paper.pdf"
                  download="AICA-Research-Paper.pdf"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium border border-blue-100 dark:border-blue-800/30 transition-all duration-200"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download PDF
                </motion.a>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* PDF Viewer Section */}
        {showPDF && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-6xl mx-auto mb-12"
          >
            <Card className="border-0 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm shadow-xl">
              <CardHeader>
                <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                  PDF Viewer
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative w-full" style={{ height: '800px' }}>
                  <iframe
                    src="/aica-research-paper.pdf"
                    className="w-full h-full rounded-lg border border-slate-200 dark:border-slate-700"
                    title="AICA Research Paper"
                  />
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-4 text-center">
                  Use the controls above to navigate through the document
                </p>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Abstract Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="max-w-5xl mx-auto mb-12"
        >
          <div className="space-y-8">
            <div className="flex items-center gap-4">
              <Image
                src="/aica-square-black-color.png"
                alt="AICA Icon"
                width={30}
                height={30}
                className="object-contain opacity-80"
                priority
              />
              <h2 className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100">
                Abstract
              </h2>
            </div>
            
            <div className="space-y-6">
              <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300 max-w-5xl text-justify">
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
                      className="px-3 py-1 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium border border-blue-100 dark:border-blue-800/30"
                    >
                      {keyword}
                    </motion.span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Citation Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.9 }}
          className="max-w-5xl mx-auto mb-12"
        >
          <div className="space-y-8">
            <div className="flex items-center gap-4">
              <Image
                src="/aica-square-black-color.png"
                alt="AICA Icon"
                width={30}
                height={30}
                className="object-contain opacity-80"
                priority
              />
              <h2 className="text-2xl md:text-3xl font-bold text-slate-800 dark:text-slate-100">
                Citation
              </h2>
            </div>
            
            <div className="space-y-6">
              <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-300 max-w-5xl text-justify">
                Gamayon, A. R. A., Chua, H. B., Calamba, N., & Cantil, J. (2024). 
                <em> AICA: AI-Powered Career Assistant for Skills-Based Job Matching</em>. 
                International Conference on AI Applications, December 2024.
              </p>
            </div>
          </div>
        </motion.section>

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
      </div>
      <Footer />
    </div>
  );
}
