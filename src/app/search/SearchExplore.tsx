'use client'

import { useState, useEffect } from 'react'
// import haifaData from '@/data/search_data/haifa_properties.json'
// import haifaData from '@/app/data/search_data/haifa_properties.json'
import tzurHadassahData from '@/data/search_data/yad2/tzur_hadassah_properties.json'
import PropertyList from '@/components/lists/PropertyList'
import Pagination from '@/components/ui/Pagination'

interface Property {
  title: string
  price: string
  location: string
  rooms: string
  size: string
  image: string
  broker: string
  link: string
}

export default function SearchExplore({ url }: { url: string }) {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 9

  // Transform the data to match PropertyList's expected format
  // const properties = haifaData.map((property: Property, index: number) => ({
  const properties = tzurHadassahData.map((property: Property, index: number) => ({
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
    <div className="w-full bg-gray-100 min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <PropertyList properties={currentProperties} />
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  )
}