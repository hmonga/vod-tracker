# Frontend Setup Guide - Building the Modern Gen Z UI

## Quick Start: Project Setup

### Step 1: Initialize React Project with Next.js
```bash
npx create-next-app@latest vod-tracker-ui --typescript --tailwind
cd vod-tracker-ui
```

### Step 2: Install Required Dependencies
```bash
# Animations & Interactions
npm install framer-motion

# UI Components & Icons
npm install @heroicons/react @radix-ui/react-primitives @headlessui/react

# Form handling
npm install react-hook-form zod @hookform/resolvers

# State management
npm install zustand @tanstack/react-query axios

# Notifications
npm install react-hot-toast

# Video player
npm install react-player

# Data visualization
npm install recharts

# Smooth scroll & animations
npm install aos react-intersection-observer

# Color utilities
npm install clsx tailwind-merge
```

### Step 3: Configure Tailwind Theme

Create `tailwind.config.ts`:
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          purple: '#8B5CF6',
          pink: '#EC4899',
          cyan: '#06B6D4',
          dark: '#0F172A',
          darker: '#0A0E27',
        },
        status: {
          success: '#10B981',
          warning: '#F97316',
          danger: '#EF4444',
          info: '#3B82F6',
        }
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
        'gradient-cyan': 'linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%)',
        'gradient-success': 'linear-gradient(135deg, #10B981 0%, #06B6D4 100%)',
        'gradient-warning': 'linear-gradient(135deg, #F97316 0%, #EF4444 100%)',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        }
      },
      backdropBlur: {
        'xl': '20px',
      }
    },
  },
  plugins: [],
}
export default config
```

---

## Core Components to Build

### 1. Layout/Navbar Component

**File**: `src/components/Navbar.tsx`
```tsx
'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { useState } from 'react'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <motion.nav 
      className="sticky top-0 z-50 bg-brand-dark/80 backdrop-blur-xl border-b border-brand-purple/20"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex-shrink-0"
          >
            <Link href="/" className="text-2xl font-bold bg-gradient-brand bg-clip-text text-transparent">
              📊 Vod Tracker
            </Link>
          </motion.div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            {['Features', 'About', 'Pricing'].map((item) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                whileHover={{ color: '#8B5CF6' }}
                className="text-gray-300 hover:text-brand-purple transition"
              >
                {item}
              </motion.a>
            ))}
          </div>

          {/* CTA Button */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="hidden md:block bg-gradient-brand text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg hover:shadow-brand-purple/50 transition"
          >
            Upload Video
          </motion.button>

          {/* Mobile menu button */}
          <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? (
              <XMarkIcon className="w-6 h-6 text-brand-purple" />
            ) : (
              <Bars3Icon className="w-6 h-6 text-brand-purple" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <motion.div
        initial={{ height: 0 }}
        animate={{ height: isOpen ? 'auto' : 0 }}
        className="md:hidden overflow-hidden bg-brand-darker border-t border-brand-purple/20"
      >
        <div className="px-4 py-4 space-y-3">
          {['Features', 'About', 'Pricing'].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="block text-gray-300 hover:text-brand-purple"
            >
              {item}
            </a>
          ))}
          <motion.button
            whileHover={{ scale: 1.02 }}
            className="w-full bg-gradient-brand text-white px-4 py-2 rounded-lg font-semibold"
          >
            Upload Video
          </motion.button>
        </div>
      </motion.div>
    </motion.nav>
  )
}
```

### 2. Hero Section Component

**File**: `src/components/Hero.tsx`
```tsx
'use client'

import { motion } from 'framer-motion'
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'

export default function Hero() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  }

  return (
    <section className="min-h-screen bg-brand-dark relative overflow-hidden flex items-center justify-center">
      {/* Animated background */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-brand-purple/20 rounded-full blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-brand-pink/20 rounded-full blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Content */}
      <motion.div
        className="relative z-10 text-center max-w-3xl mx-auto px-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants} className="mb-6">
          <span className="inline-block px-4 py-2 bg-brand-purple/20 border border-brand-purple/50 rounded-full text-brand-purple font-semibold text-sm">
            🎮 AI-Powered Valorant Coach
          </span>
        </motion.div>

        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
        >
          Analyze Your{' '}
          <span className="bg-gradient-brand bg-clip-text text-transparent">
            Crosshair Placement
          </span>
        </motion.h1>

        <motion.p
          variants={itemVariants}
          className="text-xl text-gray-400 mb-8"
        >
          Get instant feedback on your placement, find weak areas, and improve like a pro.
          Powered by AI and professional player benchmarks.
        </motion.p>

        <motion.div
          variants={itemVariants}
          className="flex gap-4 justify-center"
        >
          <motion.button
            whileHover={{ scale: 1.05, boxShadow: '0 0 30px rgba(139, 92, 246, 0.6)' }}
            whileTap={{ scale: 0.95 }}
            className="bg-gradient-brand text-white px-8 py-4 rounded-lg font-bold text-lg flex items-center gap-2 hover:shadow-2xl transition"
          >
            <ArrowUpTrayIcon className="w-6 h-6" />
            Upload Video Now
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 rounded-lg font-bold text-lg border-2 border-brand-purple text-brand-purple hover:bg-brand-purple/10 transition"
          >
            Learn More
          </motion.button>
        </motion.div>
      </motion.div>
    </section>
  )
}
```

### 3. Upload Zone Component

**File**: `src/components/UploadZone.tsx`
```tsx
'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'

export default function UploadZone() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFiles = Array.from(e.dataTransfer.files)
    if (droppedFiles.length > 0) {
      setFile(droppedFiles[0])
      simulateUpload()
    }
  }

  const simulateUpload = () => {
    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 30
      if (progress >= 100) {
        setUploadProgress(100)
        clearInterval(interval)
      } else {
        setUploadProgress(progress)
      }
    }, 500)
  }

  return (
    <motion.div
      className="w-full max-w-2xl mx-auto"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
    >
      <motion.div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        animate={{
          borderColor: isDragging ? '#8B5CF6' : 'rgba(139, 92, 246, 0.2)',
          backgroundColor: isDragging ? 'rgba(139, 92, 246, 0.05)' : 'transparent',
        }}
        className="border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition"
      >
        <motion.div
          animate={{ scale: isDragging ? 1.1 : 1 }}
          className="mb-4 flex justify-center"
        >
          <ArrowUpTrayIcon className="w-16 h-16 text-brand-purple" />
        </motion.div>

        <h3 className="text-2xl font-bold text-white mb-2">
          Drop your video here
        </h3>
        <p className="text-gray-400 mb-4">
          or click to browse (MP4, MOV, WebM up to 2GB)
        </p>

        {file && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 space-y-4"
          >
            <p className="text-brand-purple font-semibold">{file.name}</p>
            <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
              <motion.div
                className="bg-gradient-brand h-full"
                animate={{ width: `${uploadProgress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <p className="text-sm text-gray-400">{Math.round(uploadProgress)}% Uploading...</p>
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  )
}
```

### 4. Analysis Results Card Component

**File**: `src/components/ScoreCard.tsx`
```tsx
'use client'

import { motion } from 'framer-motion'
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/solid'

interface ScoreCardProps {
  title: string
  score: number
  maxScore?: number
  status: 'good' | 'warning' | 'weak'
  description?: string
}

export default function ScoreCard({
  title,
  score,
  maxScore = 10,
  status,
  description,
}: ScoreCardProps) {
  const percentage = (score / maxScore) * 100

  const statusConfig = {
    good: { color: '#10B981', bgColor: 'bg-status-success/20', icon: CheckCircleIcon },
    warning: { color: '#F97316', bgColor: 'bg-status-warning/20', icon: ExclamationCircleIcon },
    weak: { color: '#EF4444', bgColor: 'bg-status-danger/20', icon: ExclamationCircleIcon },
  }

  const config = statusConfig[status]
  const Icon = config.icon

  return (
    <motion.div
      whileHover={{ y: -8, boxShadow: '0 20px 40px rgba(139, 92, 246, 0.2)' }}
      className="bg-gradient-to-br from-slate-900/50 to-slate-800/50 backdrop-blur-xl border border-brand-purple/20 rounded-xl p-6 transition"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{title}</h3>
          {description && <p className="text-sm text-gray-400">{description}</p>}
        </div>
        <Icon className={`w-6 h-6 flex-shrink-0`} style={{ color: config.color }} />
      </div>

      <div className="mb-4">
        <div className="flex items-end justify-between mb-2">
          <span className="text-3xl font-bold text-white">{score.toFixed(1)}</span>
          <span className="text-sm text-gray-400">/ {maxScore}</span>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
          <motion.div
            className="h-full"
            style={{ background: config.color }}
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        </div>
      </div>

      <motion.div
        className={`${config.bgColor} rounded-lg p-3 text-sm`}
        style={{ color: config.color }}
      >
        {status === 'good' && '✓ Excellent placement in this area'}
        {status === 'warning' && '⚠ Room for improvement'}
        {status === 'weak' && '✕ This area needs focus'}
      </motion.div>
    </motion.div>
  )
}
```

### 5. Results Dashboard

**File**: `src/app/results/page.tsx`
```tsx
'use client'

import { motion } from 'framer-motion'
import ScoreCard from '@/components/ScoreCard'
import { useState } from 'react'

export default function ResultsPage() {
  const [activeTab, setActiveTab] = useState('overview')

  const tabs = ['overview', 'map-analysis', 'timeline', 'comparison']

  return (
    <div className="min-h-screen bg-brand-dark py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header Card */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-brand-purple/30 to-brand-pink/30 backdrop-blur-xl border border-brand-purple/50 rounded-2xl p-8 mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">Analysis Complete</h1>
              <p className="text-gray-300">valorant_comp_ascent.mp4 • 32:45 • 1920x1080 • 60fps</p>
            </div>
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-right"
            >
              <div className="text-6xl font-bold bg-gradient-brand bg-clip-text text-transparent">
                6.8
              </div>
              <p className="text-gray-300 font-semibold">/10 Overall Score</p>
            </motion.div>
          </div>

          {/* Score breakdown */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Head Level', score: 7.2 },
              { label: 'Angle Positioning', score: 5.9 },
              { label: 'Pre-Aim', score: 7.1 },
              { label: 'Role Alignment', score: 8.0 },
            ].map((item) => (
              <div key={item.label} className="bg-brand-dark/50 rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-1">{item.label}</p>
                <p className="text-2xl font-bold text-brand-purple">{item.score}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-brand-purple/20">
          {tabs.map((tab) => (
            <motion.button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold capitalize transition ${
                activeTab === tab
                  ? 'text-brand-purple border-b-2 border-brand-purple'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              whileHover={{ scale: 1.05 }}
            >
              {tab.replace('-', ' ')}
            </motion.button>
          ))}
        </div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <ScoreCard
                title="A Site Long"
                score={4.2}
                status="weak"
                description="Crosshair too low, not at head level"
              />
              <ScoreCard
                title="B Site"
                score={5.1}
                status="warning"
                description="Missing off-angle positions"
              />
              <ScoreCard
                title="Mid Control"
                score={7.8}
                status="good"
                description="Excellent awareness"
              />
              <ScoreCard
                title="Retake Setup"
                score={6.9}
                status="warning"
                description="Good but inconsistent"
              />
            </div>
          )}

          {activeTab === 'map-analysis' && (
            <div className="bg-slate-900/50 rounded-xl p-8 text-center">
              <p className="text-gray-400">Map heatmap visualization coming soon...</p>
            </div>
          )}
        </motion.div>

        {/* Improvement Plan */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-brand-purple/20 to-brand-cyan/20 backdrop-blur-xl border border-brand-purple/30 rounded-xl p-8 mt-8"
        >
          <h2 className="text-2xl font-bold text-white mb-6">Your Improvement Plan</h2>
          <div className="space-y-4">
            {[
              {
                week: 1,
                focus: 'A Main Head-Level Placement',
                action: '20min daily in Aim Lab at this position',
                expected: '+1.2 points',
              },
              {
                week: 2,
                focus: 'B Site Off-Angle Coverage',
                action: 'Custom coaching VOD review',
                expected: '+1.5 points',
              },
            ].map((item) => (
              <motion.div
                key={item.week}
                whileHover={{ x: 4 }}
                className="bg-brand-dark/50 rounded-lg p-4 flex items-start justify-between"
              >
                <div>
                  <p className="text-sm text-gray-400">Week {item.week}</p>
                  <h3 className="text-lg font-semibold text-white mt-1">{item.focus}</h3>
                  <p className="text-sm text-gray-400 mt-2">{item.action}</p>
                </div>
                <span className="text-brand-green font-semibold whitespace-nowrap ml-4">
                  {item.expected}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
```

---

## Directory Structure

```
vod-tracker-ui/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Home/Hero
│   │   ├── upload/
│   │   │   └── page.tsx
│   │   ├── results/
│   │   │   └── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Hero.tsx
│   │   ├── UploadZone.tsx
│   │   ├── ScoreCard.tsx
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── ...other components
│   ├── hooks/
│   │   ├── useUpload.ts
│   │   ├── useAnalysis.ts
│   │   └── ...custom hooks
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── ...utilities
│   └── types/
│       └── index.ts
├── tailwind.config.ts
├── tsconfig.json
├── next.config.js
└── package.json
```

---

## CSS Custom Animations

**File**: `src/app/globals.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.6);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Apply custom animations */
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

.animate-slide-in-right {
  animation: slideInRight 0.6s ease-out;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Glassmorphism */
.glass {
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(139, 92, 246, 0.1);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Remove default scrollbar styling */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #0F172A;
}

::-webkit-scrollbar-thumb {
  background: #8B5CF6;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #EC4899;
}
```

---

## Performance Tips

1. **Use Next.js Image component** for optimized images
2. **Code split with dynamic imports** for heavy components
3. **Lazy load animations** with `whileInView`
4. **Memoize components** to avoid unnecessary re-renders
5. **Use React Query** for efficient data fetching
6. **Optimize animations** with GPU acceleration (transform, opacity)

---

## Deployment

### Deploy to Vercel (Recommended)
```bash
npm i -g vercel
vercel login
vercel
```

### Environment Variables (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

---

## Next Steps

1. ✅ Set up Next.js + Tailwind
2. ✅ Create reusable components
3. ✅ Build pages (Home, Upload, Results)
4. ✅ Integrate animations with Framer Motion
5. ✅ Connect to backend API
6. ✅ Test on mobile devices
7. ✅ Deploy to Vercel
8. ✅ Gather user feedback & iterate

