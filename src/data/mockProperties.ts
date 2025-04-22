export interface Property {
  id: string;
  title: string;
  price: number;
  location: string;
  rooms: number;
  size: number; // in square meters
  imageUrl: string;
  source: 'Yad2' | 'Madlan' | 'HomeMax' | 'Komo';
  description: string;
}

export const mockProperties: Property[] = [
  {
    id: '1',
    title: 'דירת 4 חדרים מרווחת בלב תל אביב',
    price: 3850000,
    location: 'רחוב דיזנגוף 123, תל אביב',
    rooms: 4,
    size: 95,
    imageUrl: '/images/property-placeholder-1.jpg',
    source: 'Yad2',
    description: 'דירה משופצת עם מרפסת שמש, מעלית וחניה'
  },
  {
    id: '2',
    title: 'פנטהאוז יוקרתי בהרצליה פיתוח',
    price: 12500000,
    location: 'רחוב המדע 8, הרצליה פיתוח',
    rooms: 6,
    size: 200,
    imageUrl: '/images/property-placeholder-2.jpg',
    source: 'Madlan',
    description: 'פנטהאוז מפואר עם נוף לים, מרפסת ענקית ובריכה פרטית'
  },
  {
    id: '3',
    title: 'דירת 3 חדרים בחיפה',
    price: 1450000,
    location: 'רחוב הנביאים 45, חיפה',
    rooms: 3,
    size: 75,
    imageUrl: '/images/property-placeholder-3.jpg',
    source: 'HomeMax',
    description: 'דירה משופצת עם נוף להר הכרמל'
  },
  {
    id: '4',
    title: 'וילה מפוארת בקיסריה',
    price: 8900000,
    location: 'שדרות רוטשילד 10, קיסריה',
    rooms: 7,
    size: 350,
    imageUrl: '/images/property-placeholder-4.jpg',
    source: 'Komo',
    description: 'וילה עם בריכת שחייה, גינה מטופחת וחדר כושר'
  },
  {
    id: '5',
    title: 'דירת סטודיו במרכז ירושלים',
    price: 1950000,
    location: 'רחוב יפו 15, ירושלים',
    rooms: 1,
    size: 35,
    imageUrl: '/images/property-placeholder-5.jpg',
    source: 'Yad2',
    description: 'דירת סטודיו מעוצבת במיקום מרכזי'
  },
  {
    id: '6',
    title: 'דופלקס גן ברעננה',
    price: 4200000,
    location: 'רחוב אחוזה 140, רעננה',
    rooms: 5,
    size: 160,
    imageUrl: '/images/property-placeholder-6.jpg',
    source: 'Madlan',
    description: 'דופלקס גן עם גינה פרטית, מרתף ויחידת דיור נפרדת'
  }
]; 