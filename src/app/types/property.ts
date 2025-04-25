export interface Property {
  id: string;
  city: string;
  neighborhood: string;
  size: number;
  rooms: number;
  condition: string;
  requestedPrice: number;
  pricePerMeterActual: number;
  pricePerMeterAverage: number;
  url: string;
  timestamp: Date;
}

export interface PropertyNotification {
  property: Property;
  pricePerSqm: number;
  priceDifferencePercent: number;
  isProfitable: boolean;
  timestamp: Date;
} 