'use client'

import { FaHome, FaKey, FaHandshake } from 'react-icons/fa'

export default function PropertyTypes() {
  return (
    <div className="bg-gray-50 py-16">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          מה תרצו לעשות?
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Rent Card */}
          <div className="bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow cursor-pointer group">
            <div className="w-16 h-16 bg-blue-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-blue-100 transition-colors">
              <FaKey className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-4 text-gray-800">להשכיר</h3>
            <p className="text-gray-600 mb-6">
              מצאו את הדירה המושלמת להשכרה. אנחנו נעזור לכם למצוא את המקום המתאים ביותר לצרכים שלכם
            </p>
            <button className="text-blue-600 font-medium hover:text-blue-700 transition-colors">
              התחל חיפוש להשכרה →
            </button>
          </div>

          {/* Buy Card */}
          <div className="bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow cursor-pointer group">
            <div className="w-16 h-16 bg-green-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-100 transition-colors">
              <FaHome className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-4 text-gray-800">לקנות</h3>
            <p className="text-gray-600 mb-6">
              קניית דירה היא השקעה משמעותית. אנחנו נעזור לכם למצוא את הנכס המושלם במחיר הטוב ביותר
            </p>
            <button className="text-green-600 font-medium hover:text-green-700 transition-colors">
              התחל חיפוש לקנייה →
            </button>
          </div>

          {/* Sell Card */}
          <div className="bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow cursor-pointer group">
            <div className="w-16 h-16 bg-purple-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-purple-100 transition-colors">
              <FaHandshake className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-2xl font-semibold mb-4 text-gray-800">למכור</h3>
            <p className="text-gray-600 mb-6">
              מכירת נכס היא תהליך מורכב. אנחנו נעזור לכם למכור את הנכס במחיר הטוב ביותר ובזמן הקצר ביותר
            </p>
            <button className="text-purple-600 font-medium hover:text-purple-700 transition-colors">
              התחל תהליך מכירה →
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 