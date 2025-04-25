import { Property, PropertyNotification } from '../../types/property.js';

export class PropertyNotificationService {
  private readonly PROFITABILITY_THRESHOLD = -0.05; // 5% below market average
  private readonly LOCALE = 'he-IL'; // Hebrew locale for Israel

  public analyzeAndNotify(property: Property): PropertyNotification {
    const pricePerSqm = this.calculatePricePerSqm(property);
    const priceDifferencePercent = this.calculatePriceDifference(property);
    const isProfitable = this.isProfitable(priceDifferencePercent);
    
    const notification: PropertyNotification = {
      property,
      pricePerSqm,
      priceDifferencePercent,
      isProfitable,
      timestamp: new Date()
    };

    this.sendNotification(notification);
    return notification;
  }

  private calculatePricePerSqm(property: Property): number {
    return property.requestedPrice / property.size;
  }

  private calculatePriceDifference(property: Property): number {
    return (property.pricePerMeterActual - property.pricePerMeterAverage) / property.pricePerMeterAverage;
  }

  private isProfitable(priceDifferencePercent: number): boolean {
    return priceDifferencePercent < this.PROFITABILITY_THRESHOLD;
  }

  private sendNotification(notification: PropertyNotification): void {
    const message = this.formatMessage(notification);
    console.log('Sending notification:', message);
    // TODO: Implement actual notification sending
  }

  private formatMessage(notification: PropertyNotification): string {
    const { property, pricePerSqm, priceDifferencePercent, isProfitable } = notification;
    
    // Calculate total market value and difference
    const totalMarketValue = property.pricePerMeterAverage * property.size;
    const totalPriceDifference = totalMarketValue - property.requestedPrice;
    const totalPriceDifferencePercent = (totalPriceDifference / totalMarketValue) * 100;
    
    // Format numbers with Hebrew locale
    const formattedPrice = property.requestedPrice.toLocaleString(this.LOCALE);
    const formattedPricePerSqm = pricePerSqm.toLocaleString(this.LOCALE, { maximumFractionDigits: 0 });
    const formattedMarketPrice = property.pricePerMeterAverage.toLocaleString(this.LOCALE, { maximumFractionDigits: 0 });
    const formattedDifference = (Math.abs(priceDifferencePercent) * 100).toLocaleString(this.LOCALE, { maximumFractionDigits: 2 });
    const formattedTotalDifference = Math.abs(totalPriceDifference).toLocaleString(this.LOCALE);
    const formattedTotalDifferencePercent = Math.abs(totalPriceDifferencePercent).toLocaleString(this.LOCALE, { maximumFractionDigits: 2 });
    
    return `📢 Property Analysis Results\n\n` +
           `📍 Location: ${property.neighborhood}, ${property.city}\n` +
           `💰 Price: ₪${formattedPrice}\n` +
           `📏 Size: ${property.size} sqm (${property.rooms} rooms)\n` +
           `🏷️ Price per sqm: ₪${formattedPricePerSqm}\n` +
           `📊 ${formattedDifference}% ${priceDifferencePercent < 0 ? 'lower' : 'higher'} than the market price per sqm (₪${formattedMarketPrice})\n` +
           `💵 Total Price Analysis:\n` +
           `   - Market Value: ₪${totalMarketValue.toLocaleString(this.LOCALE)}\n` +
           `   - ${totalPriceDifference < 0 ? 'Overpriced' : 'Underpriced'} by: ₪${formattedTotalDifference} (${formattedTotalDifferencePercent}%)\n` +
           `💡 Condition: ${property.condition}\n` +
           `🔗 Ad link: [Here]`;
  }
} 