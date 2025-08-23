import { Navbar } from '@/components/Navbar';
import Image from 'next/image';
import React from 'react';

export default function AboutPage() {
  const authors = [
    {
      name: 'April Faith J. Gamboa',
      role: 'Researcher',
    },
    {
      name: 'Janpol S. Hidalgo',
      role: 'Full-Stack Developer/ Database Administrator',
    },
    {
      name: 'Heidine Marie J. Mahandog',
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
    <div className="relative min极-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      <Navbar />
      
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-1/4 top-极/4 h-64 w-64 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl"></div>
        <div className="absolute right-1/4 top-1/3 h-48 w-48 rounded-full bg-gradient-to极r from-pink-400/20 to-orange-400/20 blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/3 h-56 w-56 rounded-full bg-gradient-to-br from-green-400/20 to-cyan-400/20 blur-3xl"></div>
      </div>
      
      <div className="flex-1 container mx-auto px-4 py-16 md:py-24">
        {/* Hero Section */}
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
              />
            </div>

            About{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Career Assistant
            </span>
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
