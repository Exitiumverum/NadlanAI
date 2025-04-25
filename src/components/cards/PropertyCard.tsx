'use client'

import Image from 'next/image'

interface Property {
  id: string
  title: string
  price: string
  location: string
  rooms: string
  size: string
  image: string
  description: string
  link: string
}

interface PropertyCardProps {
  property: Property
}

export default function PropertyCard({ property }: PropertyCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
      <div className="relative w-full h-48">
        <Image
          src={property.image}
          alt={property.title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover"
          onError={(e) => {m
            const target = e.target as HTMLImageElement
            target.src = '/images/default-property.jpg'
          }}
        />
      </div>
      <div className="p-4">
        <h3 className="text-xl font-semibold mb-2 text-gray-800">{property.title}</h3>
        <p className="text-gray-600 mb-2">{property.location}</p>
        <div className="flex justify-between items-center mb-2 text-gray-700">
          <span>{property.rooms}</span>
          <span>{property.size}</span>
        </div>
        <p className="text-lg font-bold text-black mb-2">{property.price}</p>
        <p className="text-sm text-gray-500">{property.description}</p>
      </div>
    </div>
  )
} 