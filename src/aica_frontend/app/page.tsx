import { Hero } from '@/components/Hero';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="min-h-screen">
      <Hero />
      
      {/* Footer Section with University Logos */}
      <footer className="bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 border-t border-slate-200 dark:border-slate-700">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col items-center space-y-6">
            <p className="text-sm text-slate-600 dark:text-slate-400 text-center">
              This research paper is part of an undergraduate research paper by Gamboa, Hidalgo, Mahandog, Santia for University of Saint La Salle - College of Computing Studies.
            </p>
            
            <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16">
              <div className="flex flex-col items-center">
                <div className="relative h-24 w-24 md:h-32 md:w-32">
                  <Image
                    src="/usls.png"
                    alt="University of St. La Salle"
                    fill
                    className="object-contain"
                    sizes="128px"
                  />
                </div>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="relative h-24 w-24 md:h-32 md:w-32">
                  <Image
                    src="/ccs.png"
                    alt="College of Computing Studies"
                    fill
                    className="object-contain"
                    sizes="128px"
                  />
                </div>
              </div>
            </div>
            
            <div className="text-center pt-4">
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                All Rights Reserved.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
