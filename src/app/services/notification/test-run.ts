import { PropertyNotificationService } from './PropertyNotificationService.js';
import { Property } from '../../types/property.js';

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

const service = new PropertyNotificationService();
const notification = service.analyzeAndNotify(property);

// Log the notification
console.log('Notification Result:');
console.log(JSON.stringify(notification, null, 2)); 