'use client'

import Image from 'next/image'
import { useState } from 'react'

export default function AppHeader() {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <header className="relative h-[500px] w-full">
      <div className="absolute inset-0">
        <Image
          src="/images/cover_image_2.jpg"
          alt="Real Estate Background"
          fill
          priority
          className="object-cover"
          quality={100}
        />
        <div className="absolute inset-0 bg-black/40" /> {/* Overlay */}
      </div>
      
      {/* Top Bar with Menu, Logo, and Sign In */}
      <div className="relative z-10 w-full flex justify-between items-center px-8 pt-8">
        {/* Menu Button */}
        <button className="text-white cursor-pointer p-2 hover:bg-white/10 rounded-lg transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-6 h-6">
            <path fillRule="evenodd" d="M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z" />
          </svg>
        </button>

        {/* Centered Logo */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
          <Image
            src="/Logo3.svg"
            alt="NadlanAI Logo"
            width={200}
            height={100}
            className="object-contain"
            priority
          />
        </div>

        {/* Sign In Button */}
        <button className="bg-white/10 hover:bg-white/20 text-white px-6 py-2 rounded-lg border border-white/20 transition-colors cursor-pointer">
          התחברות
        </button>
      </div>

      <div className="relative h-full flex flex-col items-center justify-center text-white px-4">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center">
          נדלן AI - פורטל הנדל&quot;ן החכם של ישראל
        </h1>
        <p className="text-xl md:text-2xl text-center max-w-2xl mb-8">
          מצא את הנכס המושלם שלך מכל אתרי הנדל&quot;ן בישראל במקום אחד
        </p>
        
        {/* Search Bar */}
        <div className="w-full max-w-xl">
          <div className="flex items-center gap-2 bg-white/90 backdrop-blur-sm p-3 rounded-2xl shadow-lg">
            <input
              type="text"
              placeholder="חיפוש נכס..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 py-2 px-4 border-0 rounded-xl text-gray-800 focus:outline-none focus:ring-0"
            />
            <button
              className="p-2 text-gray-800 hover:text-gray-900 transition-colors"
              onClick={() => {
                // TODO: Implement search functionality
                console.log('Searching for:', searchQuery)
              }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                <path d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}