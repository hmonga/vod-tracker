'use client'

import Navbar from '@/components/Navbar'
import { motion } from 'framer-motion'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-brand-dark">
      <Navbar />
      
      {/* Hero Section */}
      <section className="min-h-[calc(100vh-64px)] relative overflow-hidden flex items-center justify-center">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-72 h-72 bg-brand-purple/20 rounded-full blur-3xl opacity-30 animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-72 h-72 bg-brand-pink/20 rounded-full blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        {/* Content */}
        <div className="relative z-10 text-center max-w-3xl mx-auto px-4">
          <motion.div 
            className="mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="inline-block px-4 py-2 bg-brand-purple/20 border border-brand-purple/50 rounded-full text-brand-purple font-semibold text-sm">
              🎮 AI-Powered Valorant Coach
            </span>
          </motion.div>

          <motion.h1
            className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
          >
            Analyze Your{' '}
            <span className="bg-gradient-brand bg-clip-text text-transparent">
              Crosshair Placement
            </span>
          </motion.h1>

          <motion.p
            className="text-xl text-gray-400 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Get instant feedback on your placement, find weak areas, and improve like a pro.
            Powered by AI and professional player benchmarks.
          </motion.p>

          <motion.div
            className="flex gap-4 justify-center flex-wrap"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <Link href="/upload">
              <motion.button
                whileHover={{ scale: 1.05, boxShadow: '0 0 30px rgba(139, 92, 246, 0.6)' }}
                whileTap={{ scale: 0.95 }}
                className="bg-gradient-brand text-white px-8 py-4 rounded-lg font-bold text-lg flex items-center gap-2 hover:shadow-2xl transition"
              >
                📤 Upload Video Now
              </motion.button>
            </Link>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 rounded-lg font-bold text-lg border-2 border-brand-purple text-brand-purple hover:bg-brand-purple/10 transition"
            >
              📖 Learn More
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-brand-darker">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">Why Choose Vod Tracker?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: '⚡',
                title: 'Instant Analysis',
                desc: 'Upload and get results in minutes'
              },
              {
                icon: '📊',
                title: 'Detailed Scoring',
                desc: 'Comprehensive placement metrics'
              },
              {
                icon: '🏆',
                title: 'Pro Comparison',
                desc: 'Compare vs professional players'
              },
              {
                icon: '📈',
                title: 'Improvement Plans',
                desc: 'Actionable recommendations'
              },
            ].map((feature, i) => (
              <motion.div
                key={i}
                className="bg-brand-dark rounded-lg p-6 border border-brand-purple/20 hover:border-brand-purple/50 transition"
                whileHover={{ y: -8 }}
              >
                <div className="text-4xl mb-3">{feature.icon}</div>
                <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Improve Your Game?</h2>
          <p className="text-xl text-gray-400 mb-8">
            Start analyzing your Valorant gameplay today and level up your crosshair placement.
          </p>
          <Link href="/upload">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-brand text-white px-10 py-4 rounded-lg font-bold text-lg hover:shadow-2xl transition"
            >
              Get Started Free
            </motion.button>
          </Link>
        </div>
      </section>
    </main>
  )
}
