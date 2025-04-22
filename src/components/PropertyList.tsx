'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import { Property, mockProperties } from '@/data/mockProperties'

export default function PropertyList() {
  const [properties, setProperties] = useState<Property[]>([])

  useEffect(() => {
    // Simulating API call with mock data
    setProperties(mockProperties)
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {properties.map((property) => (
        <div key={property.id} className="border rounded-lg overflow-hidden shadow-lg">
          <div className="relative w-full h-48">
            <Image
              src={property.imageUrl}
              alt={property.title}
              fill
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              className="object-cover"
              onError={(e) => {
                const target = e.target as HTMLImageElement
                target.src = '/images/default-property.jpg'
              }}
            />
          </div>
          <div className="p-4">
            <h3 className="text-xl font-semibold mb-2">{property.title}</h3>
            <p className="text-gray-600 mb-2">{property.location}</p>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">{property.rooms} חדרים</span>
              <span className="text-gray-600">{property.size} מ"ר</span>
            </div>
            <p className="text-lg font-bold">{property.price.toLocaleString()} ₪</p>
            <p className="text-sm text-gray-500 mt-2">מקור: {property.source}</p>
          </div>
        </div>
      ))}
    </div>
  )
} 