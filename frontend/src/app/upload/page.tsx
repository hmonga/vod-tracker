'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'
import Navbar from '@/components/Navbar'

export default function UploadZone() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)

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
      handleFileSelect(droppedFiles[0])
    }
  }

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    simulateUpload()
  }

  const simulateUpload = () => {
    setIsUploading(true)
    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 30
      if (progress >= 100) {
        setUploadProgress(100)
        setIsUploading(false)
        clearInterval(interval)
      } else {
        setUploadProgress(progress)
      }
    }, 500)
  }

  return (
    <div className="min-h-screen bg-brand-dark">
      <Navbar />
      
      <div className="max-w-4xl mx-auto py-20 px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12 text-center"
        >
          <h1 className="text-5xl font-bold mb-4">Upload Your Video</h1>
          <p className="text-gray-400 text-lg">
            Drop your Valorant gameplay video here and we'll analyze your crosshair placement
          </p>
        </motion.div>

        <motion.div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          animate={{
            borderColor: isDragging ? '#8B5CF6' : 'rgba(139, 92, 246, 0.2)',
            backgroundColor: isDragging ? 'rgba(139, 92, 246, 0.05)' : 'transparent',
          }}
          className="border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition mb-8"
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
          <p className="text-gray-400 mb-6">
            or click to browse (MP4, MOV, WebM up to 2GB)
          </p>

          <label className="inline-block">
            <input
              type="file"
              accept=".mp4,.mov,.webm,.avi,.mkv"
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  handleFileSelect(e.target.files[0])
                }
              }}
              className="hidden"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-brand text-white px-8 py-3 rounded-lg font-semibold"
              onClick={() => (document.querySelector('input[type="file"]') as HTMLInputElement)?.click()}
            >
              Browse Files
            </motion.button>
          </label>

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
              <p className="text-sm text-gray-400">{Math.round(uploadProgress)}% {isUploading ? 'Uploading...' : 'Ready'}</p>
            </motion.div>
          )}
        </motion.div>

        {file && uploadProgress === 100 && !isUploading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-brand text-white px-10 py-4 rounded-lg font-bold text-lg"
            >
              Start Analysis
            </motion.button>
          </motion.div>
        )}

        {/* File Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {[
            {
              icon: '📹',
              title: 'Supported Formats',
              desc: 'MP4, MOV, WebM, AVI, MKV'
            },
            {
              icon: '💾',
              title: 'Maximum Size',
              desc: '2GB per video'
            },
            {
              icon: '⏱️',
              title: 'Processing Time',
              desc: '~10 min per 30 min video'
            },
          ].map((item, i) => (
            <div
              key={i}
              className="bg-brand-darker rounded-lg p-6 border border-brand-purple/20"
            >
              <div className="text-3xl mb-3">{item.icon}</div>
              <h3 className="font-bold mb-2">{item.title}</h3>
              <p className="text-gray-400 text-sm">{item.desc}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  )
}
