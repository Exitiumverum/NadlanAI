import { Suspense } from 'react'
import PropertyList from '@/components/PropertyList'
import Loading from '@/components/Loading'
import AppHeader from '@/components/AppHeader'

export default function PropertiesPage() {
  return (
    <main className="min-h-screen">
      <AppHeader />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <h1 className="text-3xl font-bold mb-8">כל הנכסים</h1>
        <Suspense fallback={<Loading />}>
          <PropertyList />
        </Suspense>
      </div>
    </main>
  )
} 