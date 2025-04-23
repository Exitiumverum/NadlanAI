import { Suspense } from 'react'
import PropertyList from '@/components/lists/PropertyList'
import Loading from '@/components/Loading'
import AppHeader from '@/components/AppHeader'
import DealHighlights from '@/components/DealHighlights'
import PropertyTypes from '@/components/PropertyTypes'

export default function Home() {
  return (
    <main className="min-h-screen">
      <AppHeader />
      <DealHighlights />
      <PropertyTypes />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <Suspense fallback={<Loading />}>
        </Suspense>
      </div>
    </main>
  )
}
