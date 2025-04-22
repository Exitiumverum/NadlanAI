'use client'

import Image from 'next/image'

interface Property {
  id: number
  title: string
  price: string
  location: string
  rooms: number
  size: number
  image: string
  description: string
}

interface PropertyCardProps {
  property: Property
}

export default function PropertyCard({ property }: PropertyCardProps) {
  return (
    <div className="border rounded-lg overflow-hidden shadow-lg">
      <div className="relative w-full h-48">
        <Image
          src={property.image}
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
          <span className="text-gray-600">{property.size} מ&quot;ר</span>
        </div>
        <p className="text-lg font-bold">{property.price}</p>
        <p className="text-sm text-gray-500 mt-2">{property.description}</p>
      </div>
    </div>
  )
} 