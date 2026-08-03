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
            {['Upload', 'Features', 'About'].map((item) => (
              <motion.a
                key={item}
                href={item === 'Upload' ? '/upload' : `#${item.toLowerCase()}`}
                whileHover={{ color: '#8B5CF6' }}
                className="text-gray-300 hover:text-brand-purple transition cursor-pointer"
              >
                {item}
              </motion.a>
            ))}
          </div>

          {/* CTA Button */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="hidden md:block"
          >
            <Link 
              href="/upload"
              className="bg-gradient-brand text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg hover:shadow-brand-purple/50 transition inline-block"
            >
              Upload Video
            </Link>
          </motion.div>

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
          {['Upload', 'Features', 'About'].map((item) => (
            <Link
              key={item}
              href={item === 'Upload' ? '/upload' : `#${item.toLowerCase()}`}
              className="block text-gray-300 hover:text-brand-purple py-2"
            >
              {item}
            </Link>
          ))}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="w-full"
          >
            <Link
              href="/upload"
              className="w-full bg-gradient-brand text-white px-4 py-2 rounded-lg font-semibold block text-center"
            >
              Upload Video
            </Link>
          </motion.div>
        </div>
      </motion.div>
    </motion.nav>
  )
}
