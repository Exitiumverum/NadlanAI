'use client'

import { useState } from 'react'
import PropertyCard from './PropertyCard'

export default function PropertyList() {
  const [properties] = useState([
    {
      id: 1,
      title: 'דירה מרווחת בתל אביב',
      price: '2,500,000 ₪',
      location: 'תל אביב',
      rooms: 4,
      size: 120,
      image: '/images/property1.jpg',
      description: 'דירה מרווחת ומעוצבת במרכז תל אביב, קרובה לכל השירותים והתחבורה הציבורית.'
    },
    {
      id: 2,
      title: 'דירת גן ברמת גן',
      price: '1,800,000 ₪',
      location: 'רמת גן',
      rooms: 3,
      size: 90,
      image: '/images/property2.jpg',
      description: 'דירת גן שקטה ומוארת ברמת גן, עם גינה פרטית וחניה.'
    },
    {
      id: 3,
      title: 'דירת פנטהאוס בהרצליה',
      price: '3,200,000 ₪',
      location: 'הרצליה',
      rooms: 5,
      size: 150,
      image: '/images/property3.jpg',
      description: 'נטהאוס מפואר בהרצליה עם נוף לים, מרפסת גדולה ומעלית פרטית.'
    }
  ])

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold mb-8 text-center">נכסים מומלצים</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {properties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>
    </div>
  )
} 