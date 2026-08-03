import type { Metadata } from "next"
import { Providers } from "./providers"
import "./globals.css"

export const metadata: Metadata = {
  title: "Vod Tracker - Valorant Crosshair Analyzer",
  description: "AI-powered video analysis for Valorant crosshair placement coaching",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-brand-dark text-white">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
