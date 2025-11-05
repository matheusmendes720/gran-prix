import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Nova Corrente - Supply Chain Analytics',
  description: 'Production-Ready Full-Stack Predictive Analytics Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-100">
          <nav className="bg-gray-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex items-center justify-between h-16">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-white text-xl font-bold">Nova Corrente</span>
                  </div>
                </div>
                <div className="hidden md:block">
                  <div className="ml-4 flex items-center md:ml-6">
                    <span className="text-sm text-gray-300">Welcome, User</span>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          
          <div className="flex">
            <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
              {/* Sidebar content */}
              <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
                <div className="flex-1 px-2 space-y-1">
                  <a href="/" className="bg-gray-900 text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Dashboard
                  </a>
                  <a href="/materials" className="text-gray-300 hover:bg-gray-700 hover:text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Materials
                  </a>
                  <a href="/forecasts" className="text-gray-300 hover:bg-gray-700 hover:text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Forecasts
                  </a>
                  <a href="/inventory" className="text-gray-300 hover:bg-gray-700 hover:text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Inventory
                  </a>
                  <a href="/recommendations" className="text-gray-300 hover:bg-gray-700 hover:text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Recommendations
                  </a>
                  <a href="/alerts" className="text-gray-300 hover:bg-gray-700 hover:text-white group flex items-center px-2 py-2 text-base font-medium rounded-md">
                    Alerts
                  </a>
                </div>
              </div>
            </div>
            <div className="md:pl-64 flex-1">
              <main>
                {children}
              </main>
            </div>
          </div>
        </div>
      </body>
    </html>
  )
}