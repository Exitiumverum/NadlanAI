'use client'

import { useState } from 'react'

export default function PropertySearch() {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div className="mb-8">
      <div className="flex flex-col md:flex-row gap-4">
        <input
          type="text"
          placeholder="חיפוש נכס..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 p-3 border rounded-lg"
        />
        <button
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          onClick={() => {
            // TODO: Implement search functionality
            console.log('Searching for:', searchQuery)
          }}
        >
          חיפוש
        </button>
      </div>
    </div>
  )
} 