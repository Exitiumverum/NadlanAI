'use client'

import { FaRobot, FaChartLine, FaSearch, FaBell } from 'react-icons/fa'

export default function DealHighlights() {
  return (
    <div className="bg-white py-16">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          אנחנו נמצא עבורך את העסקה הטובה ביותר
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* AI Analysis Card */}
          <div className="bg-gray-50 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
              <FaRobot className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800">ניתוח AI מתקדם</h3>
            <p className="text-gray-600">
              מערכת AI חכמה שמנתחת אלפי נכסים ומזהה את העסקאות הטובות ביותר בשוק
            </p>
          </div>

          {/* Market Trends Card */}
          <div className="bg-gray-50 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-4">
              <FaChartLine className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800">ניתוח מגמות שוק</h3>
            <p className="text-gray-600">
              מעקב אחר מגמות שוק בזמן אמת והמלצות מבוססות נתונים
            </p>
          </div>

          {/* Smart Search Card */}
          <div className="bg-gray-50 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4">
              <FaSearch className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800">חיפוש חכם</h3>
            <p className="text-gray-600">
              חיפוש מתקדם שמתאים את התוצאות להעדפות האישיות שלך
            </p>
          </div>

          {/* Alerts Card */}
          <div className="bg-gray-50 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
              <FaBell className="w-6 h-6 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-800">התראות בזמן אמת</h3>
            <p className="text-gray-600">
              קבלת התראות מיידיות על עסקאות חדשות שמתאימות לקריטריונים שלך
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 