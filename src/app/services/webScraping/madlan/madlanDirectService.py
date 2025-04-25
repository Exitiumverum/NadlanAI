import asyncio
import json
import os
import random
import time
from datetime import datetime
from typing import List, Dict, Any
from playwright.async_api import async_playwright, Page, BrowserContext

class MadlanDirectService:
    def __init__(self):
        self.browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.properties: List[Dict[str, Any]] = []
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data', 'search_data', 'madlan')
        os.makedirs(self.data_dir, exist_ok=True)

    async def human_like_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0):
        """Add human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

    async def human_like_scroll(self, distance: int):
        """Simulate human-like scrolling"""
        current_position = await self.page.evaluate("window.scrollY")
        target_position = current_position + distance
        
        while current_position < target_position:
            scroll_amount = random.randint(50, 150)
            current_position = min(current_position + scroll_amount, target_position)
            await self.page.evaluate(f"window.scrollTo(0, {current_position})")
            await self.human_like_delay(0.1, 0.3)

    async def setup_browser(self):
        """Set up Firefox with Tor proxy"""
        print("Setting up Firefox with Tor proxy...")
        playwright = await async_playwright().start()
        
        # Launch Firefox with Tor proxy
        self.context = await playwright.firefox.launch_persistent_context(
            user_data_dir="./firefox_profile",  # Create a new profile
            headless=False,
            proxy={
                "server": "socks5://127.0.0.1:9050"  # Tor SOCKS proxy
            },
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0',
            locale='he-IL',
            timezone_id='Asia/Jerusalem',
            geolocation={'latitude': 31.7683, 'longitude': 35.2137},
            permissions=['geolocation'],
            java_script_enabled=True,
            has_touch=False,
            is_mobile=False,
            color_scheme='light',
            reduced_motion='no-preference',
            forced_colors='none'
        )
        
        self.page = await self.context.new_page()
        
        # Add anti-detection scripts
        await self.context.add_init_script("""
            // Override navigator properties
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override chrome object
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
                    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                    { name: 'Native Client', filename: 'internal-nacl-plugin' }
                ]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['he-IL', 'he', 'en-US', 'en']
            });
            
            // Override platform
            Object.defineProperty(navigator, 'platform', {
                get: () => 'MacIntel'
            });
            
            // Override hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            
            // Override device memory
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
            
            // Override screen properties
            Object.defineProperty(window, 'screen', {
                get: () => ({
                    width: 1366,
                    height: 768,
                    colorDepth: 24,
                    pixelDepth: 24
                })
            });
            
            // Override requestAnimationFrame
            const originalRAF = window.requestAnimationFrame;
            window.requestAnimationFrame = function(callback) {
                return originalRAF(callback);
            };
            
            // Override performance.now()
            const originalNow = performance.now;
            performance.now = function() {
                return originalNow.apply(performance, arguments);
            };
            
            // Override canvas fingerprinting
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type) {
                const context = originalGetContext.apply(this, arguments);
                if (type === '2d') {
                    const originalGetImageData = context.getImageData;
                    context.getImageData = function() {
                        const imageData = originalGetImageData.apply(this, arguments);
                        for (let i = 0; i < imageData.data.length; i += 4) {
                            imageData.data[i] += Math.random() * 2 - 1;
                            imageData.data[i + 1] += Math.random() * 2 - 1;
                            imageData.data[i + 2] += Math.random() * 2 - 1;
                        }
                        return imageData;
                    };
                }
                return context;
            };
        """)
        
        # Set comprehensive headers
        await self.context.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Pragma': 'no-cache',
            'TE': 'trailers'
        })
        
        # Set default timeout
        self.page.set_default_timeout(60000)  # 60 seconds
        
        print("Firefox with Tor proxy setup complete")

    async def scrape_properties(self, city: str) -> List[Dict[str, Any]]:
        """Scrape properties from Madlan"""
        try:
            await self.setup_browser()
            print(f"Navigating to Madlan for {city}...")
            
            base_url = "https://www.madlan.co.il/for-sale/חיפה-ישראל"
            all_properties = []
            current_page = 1
            
            while True:
                print(f"\nProcessing page {current_page}...")
                page_url = f"{base_url}?page={current_page}" if current_page > 1 else base_url
                
                # Navigate with enhanced stealth
                await self.page.goto(page_url, wait_until="networkidle", timeout=60000)
                await asyncio.sleep(random.uniform(3, 5))  # Wait for page to load
                
                # Get property listings
                listings = await self.page.query_selector_all('[data-auto="listed-bulletin-clickable"]')
                if not listings:
                    break
                
                for listing in listings:
                    try:
                        property_data = {}
                        
                        # Extract price
                        price_elem = await listing.query_selector('[data-auto="property-price"]')
                        if price_elem:
                            price_text = await price_elem.text_content()
                            price = ''.join(filter(str.isdigit, price_text))
                            property_data['price'] = int(price) if price else None
                        
                        # Extract rooms
                        rooms_elem = await listing.query_selector('[data-auto="property-rooms"]')
                        if rooms_elem:
                            rooms_text = await rooms_elem.text_content()
                            rooms = ''.join(filter(str.isdigit, rooms_text))
                            property_data['rooms'] = float(rooms) if rooms else None
                        
                        # Extract size
                        size_elem = await listing.query_selector('[data-auto="property-size"]')
                        if size_elem:
                            size_text = await size_elem.text_content()
                            size = ''.join(filter(str.isdigit, size_text))
                            property_data['size'] = int(size) if size else None
                        
                        # Extract address
                        address_elem = await listing.query_selector('[data-auto="property-address"]')
                        if address_elem:
                            address_text = await address_elem.text_content()
                            property_data['address'] = address_text
                        
                        # Extract images
                        image_elements = await listing.query_selector_all('[data-auto="universal-card-image"]')
                        image_urls = []
                        for img_elem in image_elements:
                            image_src = await img_elem.get_attribute('src')
                            if image_src:
                                image_urls.append(image_src)
                        property_data['image_urls'] = image_urls if image_urls else None
                        
                        property_data['city'] = city
                        property_data['scraped_at'] = datetime.now().isoformat()
                        
                        all_properties.append(property_data)
                        await asyncio.sleep(random.uniform(1, 2))  # Wait between properties
                        
                    except Exception as e:
                        print(f"Error processing property: {str(e)}")
                        continue
                
                # Check for next page
                next_button = await self.page.query_selector(f'[data-auto="bulletins-pagination-{current_page + 1}"]')
                if not next_button:
                    break
                
                current_page += 1
                await asyncio.sleep(random.uniform(3, 5))  # Wait before next page
            
            # Save results
            if all_properties:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'madlan_properties_{timestamp}.json'
                filepath = os.path.join(self.data_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(all_properties, f, ensure_ascii=False, indent=2)
                
                print(f"\nSaved {len(all_properties)} properties to {filepath}")
            
            return all_properties
            
        except Exception as e:
            print(f"Error scraping properties: {str(e)}")
            return []
        
        finally:
            if self.context:
                await self.context.close()

async def main():
    scraper = MadlanDirectService()
    properties = await scraper.scrape_properties("חיפה")
    print(f"Found {len(properties)} properties")

if __name__ == "__main__":
    asyncio.run(main()) 