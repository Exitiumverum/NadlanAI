import { Suspense } from 'react'
import Loading from '@/components/Loading'
import SearchExplore from './SearchExplore'
import AppHeader from '@/components/AppHeader'

export default function SearchPage({ 
  searchParams 
}: { 
  searchParams: { 
    q?: string
    type?: string
    minPrice?: string
    maxPrice?: string
    location?: string
  } 
}) {
  return (
    <main className="min-h-screen">
      <AppHeader />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <h1 className="text-3xl font-bold mb-8">תוצאות חיפוש</h1>
        <Suspense fallback={<Loading />}>
          {/* Your search results component will go here */}
          <div>Search Results for: {searchParams.q}</div>
        <SearchExplore url="צור הדסה" />
        </Suspense>
      </div>
    </main>
  )
} 