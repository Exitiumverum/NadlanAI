import asyncio
import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup

class MadlanService:
    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.url: url = "https://www.madlan.co.il/for-sale/%D7%A9%D7%9B%D7%95%D7%A0%D7%94-%D7%94%D7%93%D7%A8-%D7%94%D7%9B%D7%A8%D7%9E%D7%9C-%D7%97%D7%99%D7%A4%D7%94-%D7%99%D7%A9%D7%A8%D7%90%D7%9C?bbox=34.98849%2C32.80289%2C35.00644%2C32.81710&tracking_search_source=map&marketplace=residential"
        self.properties: List[Dict[str, Any]] = []
        self.cities_url_list: cities_url_list = [];

    async def setup_browser(self):
        """Set up browser with human-like settings"""
        print("Setting up browser...")
        playwright = await async_playwright().start()
        
        # Use a more realistic user agent
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.browser = await playwright.chromium.launch(
            headless=False,  # Run in non-headless mode to appear more human
            slow_mo=50,  # Add slight delay between actions
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-web-security',
                '--disable-features=BlockInsecurePrivateNetworkRequests'
            ]
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1400, 'height': 700},
            user_agent=user_agent,
            locale='he-IL',
            timezone_id='Asia/Jerusalem',
            geolocation={'latitude': 31.7683, 'longitude': 35.2137},  # Jerusalem coordinates
            permissions=['geolocation']
        )
        
        # Add human-like mouse movements
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page = await self.context.new_page()
        print("Browser setup complete")

    async def handle_modals(self):
        """Handle modal dialogs and popups"""
        try:
            # First try to find and click the specific close button
            close_button_selectors = [
                'button.bz-close-btn',
                'button[aria-label="Close Message"]',
                'button#ipl2',
                '.bz-close-btn',
                'button[aria-label="סגור"]',
                'button[aria-label="סגירה"]'
            ]
            
            for selector in close_button_selectors:
                try:
                    button = await self.page.wait_for_selector(selector, timeout=5000)
                    if button and await button.is_visible():
                        print(f"Found close button with selector: {selector}")
                        await button.click()
                        await self.human_like_delay(0.2, 0.5)  # Reduced delay
                        return True
                except Exception as e:
                    print(f"Close button selector {selector} failed: {str(e)}")
                    continue
            
            return False
                    
        except Exception as e:
            print(f"Error in handle_modals: {str(e)}")
            return False

    async def human_like_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

    async def human_like_scroll(self):
        """Simulate human-like scrolling behavior"""
        viewport_height = await self.page.evaluate("window.innerHeight")
        total_height = await self.page.evaluate("document.body.scrollHeight")
        
        for i in range(0, total_height, viewport_height):
            # Random scroll speed and pauses
            scroll_amount = random.randint(viewport_height // 2, viewport_height)
            await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            await self.human_like_delay(0.5, 1.5)
            
            # Check for ads after scrolling
            await self.handle_modals()
            
            # Occasionally scroll back up a bit
            if random.random() < 0.2:
                await self.page.evaluate(f"window.scrollBy(0, -{random.randint(100, 300)})")
                await self.human_like_delay(0.5, 1.0)

    async def scrape_tzur_hadassah_properties(self) -> List[Dict[str, Any]]:
        """Scrape properties from Yad2 with direct link"""
        try:
            print("Starting browser...")
            await self.setup_browser()
            
            print("Navigating to Yad2...")
            # Go directly to the Tzur Hadassah properties page
            
            await self.page.goto(self.url)
            await self.human_like_delay(2, 4)
            
            # Handle any initial ads/popups and modals
            # await self.handle_modals()
            
            # Wait for results to load
            await self.page.wait_for_selector('.css-u1nut8.e10ue70710', state="visible", timeout=30000)
            await self.human_like_delay(2, 3)
            
            # Scroll through results
            await self.human_like_scroll()
            
            # Get page content
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all property listings
            listings = soup.find_all('div', class="css-u1nut8 e10ue70710")
            
            for listing in listings:
                try:
                    # Extract property details with error handling
                    title_elem = listing.find(['div', 'h2'], class_=['title', 'item-title'])
                    title = title_elem.text.strip() if title_elem else "No title"
                    
                                # Extract the property price using the `data-auto` attribute
                    price_elem = listing.find('div', attrs={'data-auto': 'property-price'})
                    price = price_elem.text.strip() if price_elem else "Price not available"
                    print("The price is: ", price)
                                
                    location_elem = listing.find(['div', 'span'], class_=['location', 'item-location', 'address'])
                    location = location_elem.text.strip() if location_elem else "Location not available"
                    
                    details = listing.find_all(['div', 'span'], class_=['data', 'item-data', 'details'])
                    rooms = details[0].text.strip() if len(details) > 0 else "N/A"
                    size = details[1].text.strip() if len(details) > 1 else "N/A"
                    
                    image_elem = listing.find('img')
                    image_url = image_elem['src'] if image_elem and 'src' in image_elem.attrs else None
                    
                    description_elem = listing.find(['div', 'p'], class_=['description', 'item-description'])
                    description = description_elem.text.strip() if description_elem else "No description"
                    
                    link_elem = listing.find('a', href=True)
                    property_link = f"https://www.yad2.co.il{link_elem['href']}" if link_elem else None
                    
                    property_data = {
                        'title': title,
                        'price': price,
                        'location': location,
                        'rooms': rooms,
                        'size': size,
                        'image': image_url,
                        'description': description,
                        'link': property_link,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    self.properties.append(property_data)
                    await self.human_like_delay(0.5, 1.5)  # Pause between processing each property
                    
                except Exception as e:
                    print(f"Error processing listing: {str(e)}")
                    continue
            
            # Save results to JSON file
            with open('tzur_hadassah_properties.json', 'w', encoding='utf-8') as f:
                json.dump(self.properties, f, ensure_ascii=False, indent=2)
            
            return self.properties
            
        except Exception as e:
            print(f"Error scraping properties: {str(e)}")
            return []
        
        finally:
            print("Closing browser...")
            if self.browser:
                await self.browser.close()
            print("Browser closed")

async add_city(self):
    # url = https://www.madlan.co.il/for-sale/;
    # url += self.state + "/"
    # url += self.city + "/"
    # with_street_url = url
    # with_street_url += self.houseNumber + "/"
    # with_street_url += self.street;
    self.url = "https://www.madlan.co.il/for-sale/%D7%A6%D7%95%D7%A8-%D7%94%D7%93%D7%A1%D7%94-%D7%99%D7%A9%D7%A8%D7%90%D7%9C,%D7%94%D7%A8-%D7%9B%D7%AA%D7%A8%D7%95%D7%9F-66-%D7%A6%D7%95%D7%A8-%D7%94%D7%93%D7%A1%D7%94-%D7%99%D7%A9%D7%A8%D7%90%D7%9C?tracking_search_source=new_search"
    # if(!validStreet())
        self.url = url;

async def main(self):
    
    self.cities_url_list.append()
    scraper = MadlanService()
    properties = await scraper.scrape_tzur_hadassah_properti    es()
    print(f"Found {len(properties)} properties")

if __name__ == "__main__":
    asyncio.run(main()) 