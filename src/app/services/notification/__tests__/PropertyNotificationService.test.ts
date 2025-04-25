// @ts-ignore
declare const describe: (name: string, fn: () => void) => void;
// @ts-ignore
declare const it: (name: string, fn: () => void) => void;
// @ts-ignore
declare const expect: any;
// @ts-ignore
declare const beforeEach: (fn: () => void) => void;

import { PropertyNotificationService } from '../PropertyNotificationService';
import { Property } from '../../../types/property';

describe('PropertyNotificationService', () => {
  let service: PropertyNotificationService;

  beforeEach(() => {
    service = new PropertyNotificationService();
  });

  describe('analyzeAndNotify', () => {
    it('should match the example notification format and calculations', () => {
      const property: Property = {
        id: "001",
        city: "Haifa",
        neighborhood: "Hadar Center",
        requestedPrice: 950000,
        size: 65,
        rooms: 3,
        condition: "Renovated",
        pricePerMeterActual: 14615, // 950,000 / 65
        pricePerMeterAverage: 16000
      };

      const result = service.analyzeAndNotify(property);
      
      // Verify calculations
      expect(result.pricePerSqm).toBe(14615.384615384615); // 950,000 / 65
      expect(result.priceDifferencePercent).toBeCloseTo(-0.0866, 4); // (14,615 - 16,000) / 16,000
      expect(result.isProfitable).toBe(true);

      // Get the formatted message
      const message = service['formatMessage'](result);
      
      // Verify message format matches example
      expect(message).toContain('📢 A good deal was found!');
      expect(message).toContain('📍 Location: Hadar Center, Haifa');
      expect(message).toContain('💰 Price: ₪950,000');
      expect(message).toContain('📏 Size: 65 sqm (3 rooms)');
      expect(message).toContain('🏷️ Price per sqm: ₪14,615');
      expect(message).toContain('📊 8.66% lower than the market price (₪16,000 per sqm)');
      expect(message).toContain('💡 Condition: Renovated');
      expect(message).toContain('🔗 Ad link: [Here]');
    });

    it('should analyze and notify for non-profitable property', () => {
      const property: Property = {
        id: "002",
        city: "חיפה",
        neighborhood: "הדר מרכז",
        requestedPrice: 1200000,
        size: 70,
        rooms: 3,
        condition: "ישנה",
        pricePerMeterActual: 17143,
        pricePerMeterAverage: 16000
      };

      const result = service.analyzeAndNotify(property);
      
      expect(result.isProfitable).toBe(false);
      expect(result.priceDifferencePercent).toBeGreaterThan(0);
    });

    it('should analyze and notify for Kiryat Bialik property', () => {
      // Create property data based on the provided information
      const property: Property = {
        id: 'test-1',
        city: 'Kiryat Bialik',
        neighborhood: 'Keren HaYesod',
        size: 60,
        rooms: 3,
        condition: 'Renovated',
        requestedPrice: 1080000,
        pricePerMeterActual: 18000, // 1,080,000 / 60
        pricePerMeterAverage: 20000, // Assuming market average
        url: 'test-url',
        timestamp: new Date()
      };

      const notification = service.analyzeAndNotify(property);

      // Verify the notification
      expect(notification).toBeDefined();
      expect(notification.property).toEqual(property);
      expect(notification.pricePerSqm).toBe(18000);
      expect(notification.priceDifferencePercent).toBeLessThan(0); // Should be below market average
      expect(notification.isProfitable).toBe(true);
    });
  });
}); 