import { Suspense } from 'react'
import Loading from '@/components/Loading'
import AppHeader from '@/components/AppHeader'
import PropertyDetails from '@/components/PropertyDetails'

export default function PropertyPage({ params }: { params: { id: string } }) {
  return (
    <main className="min-h-screen">
      <AppHeader />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <Suspense fallback={<Loading />}>
          <PropertyDetails propertyId={params.id} />
        </Suspense>
      </div>
    </main>
  )
} 