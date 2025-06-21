import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            SafeRent SF
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Find safe and affordable rental properties in San Francisco with real-time crime data and neighborhood insights.
          </p>
          
          <div className="mt-8 flex justify-center">
            <Link href="/login" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
              Get Started
            </Link>
          </div>
          
          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg font-medium text-gray-900">Crime Data</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Real-time crime statistics and safety ratings for every neighborhood.
                </p>
              </div>
            </div>
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg font-medium text-gray-900">Interactive Maps</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Explore neighborhoods with interactive maps and detailed property information.
                </p>
              </div>
            </div>
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg font-medium text-gray-900">AI Insights</h3>
                <p className="mt-2 text-sm text-gray-500">
                  Get personalized recommendations and neighborhood analysis powered by AI.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 