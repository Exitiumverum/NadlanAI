import AppHeader from '@/components/AppHeader'

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      <AppHeader />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <h1 className="text-3xl font-bold mb-8">אודות</h1>
        <div className="prose max-w-none">
          <p className="text-lg mb-4">
            נדלן AI הוא פלטפורמה חדשנית המחברת בין קונים למוכרים בשוק הנדל"ן.
          </p>
          <p className="text-lg mb-4">
            אנו משתמשים בטכנולוגיה מתקדמת כדי לספק את המידע המדויק והמעודכן ביותר על נכסים.
          </p>
        </div>
      </div>
    </main>
  )
} 