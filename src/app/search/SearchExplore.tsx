'use client'

import { useState, useEffect } from 'react'
import tzurHadassahData from '@/data/search_data/tzur_hadassah_properties_20250423_194654.json'
import PropertyList from '@/components/lists/PropertyList'
import Pagination from '@/components/ui/Pagination'

export default function SearchExplore({ url }: { url: string }) {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 9

  // Transform the data to match PropertyList's expected format
  const properties = tzurHadassahData.map((property, index) => ({
    id: index.toString(),
    title: property.title,
    price: property.price,
    location: property.location,
    rooms: property.rooms,
    size: property.size,
    image: property.image.startsWith('//') ? `https:${property.image}` : property.image,
    description: property.broker,
    link: property.link
  }))

  // Calculate pagination
  const totalPages = Math.ceil(properties.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentProperties = properties.slice(startIndex, endIndex)

  // Scroll to top when page changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [currentPage])

  return (
    <div className="w-full">
      <PropertyList properties={currentProperties} />
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      />
    </div>
  )
}