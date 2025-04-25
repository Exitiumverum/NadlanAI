'use client'

import { useState } from 'react'
import PropertyCard from '../cards/PropertyCard'

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

interface PropertyListProps {
  properties: Property[]
}

export default function PropertyList({ properties }: PropertyListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {properties.map((property) => (
        <div key={property.id} className="transform transition-all duration-300 hover:scale-105">
          <PropertyCard property={property} />
        </div>
      ))}
    </div>
  )
} 