'use client';

import { motion } from 'motion/react';
import React from 'react';

const AnimatedBackground = () => {
  const particles = [
    { left: 10, top: 20, duration: 4, delay: 0.5 },
    { left: 80, top: 30, duration: 5, delay: 1.0 },
    { left: 25, top: 70, duration: 6, delay: 1.5 },
    { left: 70, top: 15, duration: 3, delay: 0.2 },
    { left: 40, top: 50, duration: 5, delay: 0.8 },
    { left: 90, top: 60, duration: 4, delay: 1.2 },
    { left: 15, top: 40, duration: 7, delay: 1.8 },
    { left: 60, top: 80, duration: 4, delay: 0.3 },
  ];

  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      {/* Base Gradient Layer */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/20 via-indigo-50/15 to-purple-50/25 dark:from-blue-900/10 dark:via-indigo-900/8 dark:to-purple-900/12"></div>

      {/* Animated Gradient Orbs */}
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

      {/* Geometric Grid Pattern */}
      <div className="absolute inset-0 opacity-15 dark:opacity-10">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      </div>

      {/* Subtle Corner Accents */}
      <div className="absolute top-0 left-0 w-48 h-48 bg-gradient-to-br from-blue-400/10 to-transparent rounded-full blur-xl"></div>
      <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-purple-400/10 to-transparent rounded-full blur-xl"></div>
      <div className="absolute bottom-0 left-0 w-36 h-36 bg-gradient-to-tr from-indigo-400/10 to-transparent rounded-full blur-xl"></div>
      <div className="absolute bottom-0 right-0 w-44 h-44 bg-gradient-to-tl from-pink-400/10 to-transparent rounded-full blur-xl"></div>

      {/* Animated Particles - Fixed deterministic positions */}
      <div className="absolute inset-0">
        {particles.map((particle, i) => (
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
  );
};

export default AnimatedBackground;
