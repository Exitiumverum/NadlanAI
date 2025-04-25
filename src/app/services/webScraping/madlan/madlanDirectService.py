import asyncio
import json
import random
import time
import os
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup

class MadlanDirectService:
    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.properties: List[Dict[str, Any]] = []
        # Create data directory structure
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')
        self.search_data_dir = os.path.join(self.data_dir, 'search_data')
        self.madlan_data_dir = os.path.join(self.search_data_dir, 'madlan')
        os.makedirs(self.madlan_data_dir, exist_ok=True)

    async def setup_browser(self):
        """Set up browser with human-like settings"""
        print("Setting up browser...")
        playwright = await async_playwright().start()
        
        # Use a more realistic user agent and viewport
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        # Random viewport size within common desktop resolutions
        viewport_width = random.choice([1366, 1440, 1536, 1920])
        viewport_height = random.choice([768, 900, 864, 1080])
        
        self.browser = await playwright.chromium.launch(
            headless=False,
            slow_mo=random.randint(50, 150),  # Random delay between actions
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-web-security',
                '--disable-features=BlockInsecurePrivateNetworkRequests',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                f'--window-size={viewport_width},{viewport_height}',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-web-security',
                '--disable-features=BlockInsecurePrivateNetworkRequests'
            ]
        )
        
        # Create a new context with more realistic settings
        self.context = await self.browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height},
            user_agent=user_agent,
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
        
        # Add additional headers to appear more like a real browser
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
            'DNT': '1'
        })
        
        # Add more sophisticated anti-bot detection scripts
        await self.context.add_init_script("""
            // Override navigator properties
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Add realistic plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
                    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                    { name: 'Native Client', filename: 'internal-nacl-plugin' }
                ]
            });
            
            // Add realistic languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['he-IL', 'he', 'en-US', 'en']
            });
            
            // Add realistic platform
            Object.defineProperty(navigator, 'platform', {
                get: () => 'MacIntel'
            });
            
            // Add realistic hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            
            // Add realistic device memory
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
            
            // Add realistic screen properties
            Object.defineProperty(window, 'screen', {
                get: () => ({
                    width: """ + str(viewport_width) + """,
                    height: """ + str(viewport_height) + """,
                    colorDepth: 24,
                    pixelDepth: 24
                })
            });
        """)
        
        self.page = await self.context.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(30000)
        
        # Enable JavaScript
        await self.page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'
        })
        
        print("Browser setup complete")

    async def handle_modals(self):
        """Handle modal dialogs and popups"""
        try:
            close_button_selectors = [
                'button[aria-label="סגור"]',
                'button[aria-label="סגירה"]',
                '.close-button',
                '.modal-close'
            ]
            
            for selector in close_button_selectors:
                try:
                    button = await self.page.wait_for_selector(selector, timeout=5000)
                    if button and await button.is_visible():
                        print(f"Found close button with selector: {selector}")
                        await button.click()
                        await self.human_like_delay(0.2, 0.5)
                        return True
                except Exception as e:
                    print(f"Close button selector {selector} failed: {str(e)}")
                    continue
            
            return False
                    
        except Exception as e:
            print(f"Error in handle_modals: {str(e)}")
            return False

    async def human_like_delay(self, min_seconds: float = 0.1, max_seconds: float = 0.3):
        """Add minimal delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

    async def human_like_scroll(self):
        """Simulate human-like scrolling"""
        viewport_height = await self.page.evaluate("window.innerHeight")
        total_height = await self.page.evaluate("document.body.scrollHeight")
        
        # Random scroll amount between 1/4 and 3/4 of viewport
        scroll_amount = random.randint(viewport_height // 4, viewport_height * 3 // 4)
        current_position = 0
        
        while current_position < total_height:
            # Random delay between scrolls
            await self.human_like_delay(0.1, 0.3)
            
            # Scroll with random speed
            scroll_speed = random.uniform(0.5, 1.5)
            current_position += int(scroll_amount * scroll_speed)
            
            # Scroll to current position
            await self.page.evaluate(f"window.scrollTo(0, {current_position})")
            
            # Random pause sometimes
            if random.random() < 0.2:
                await self.human_like_delay(0.5, 1.5)

    async def scroll_to_bottom(self):
        """Scroll to the bottom of the page quickly"""
        print("Scrolling to bottom of page...")
        
        # Get the total height of the page
        total_height = await self.page.evaluate("document.body.scrollHeight")
        viewport_height = await self.page.evaluate("window.innerHeight")
        
        # Scroll in larger steps (3/4 of viewport height at a time)
        scroll_step = (viewport_height * 3) // 4
        current_position = 0
        
        while current_position < total_height:
            # Scroll by the step amount
            await self.page.evaluate(f"window.scrollTo(0, {current_position})")
            
            # Add minimal delay between scrolls
            await self.human_like_delay(0.1, 0.2)
            
            # Update current position
            current_position += scroll_step
        
        # Final scroll to ensure we're at the bottom
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await self.human_like_delay(0.2, 0.3)

    async def scrape_properties(self, city: str) -> List[Dict[str, Any]]:
        """Scrape properties from Madlan for a specific city"""
        try:
            print("Starting browser...")
            await self.setup_browser()
            
            print(f"Navigating to Madlan for {city}...")
            base_url = "https://www.madlan.co.il/for-sale/חיפה-ישראל"
            
            all_properties = []
            current_page = 1
            max_pages = 1000  # Increased maximum pages
            
            while current_page <= max_pages:
                print(f"\nProcessing page {current_page}...")
                
                # Navigate to the current page
                page_url = f"{base_url}?page={current_page}" if current_page > 1 else base_url
                print(f"Navigating to: {page_url}")
                
                try:
                    # Try to load the page
                    response = await self.page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
                    
                    # Check if we got a 404
                    if response.status == 404:
                        print("Reached the last page (404)")
                        break
                    
                    # Quick scroll to bottom
                    await self.scroll_to_bottom()
                    
                    # Wait briefly for any dynamic content
                    await self.human_like_delay(0.5, 1)
                    
                    # Check for property listings
                    listings = await self.page.query_selector_all('[data-auto="listed-bulletin-clickable"]')
                    if not listings:
                        # Try alternative selector
                        listings = await self.page.query_selector_all('.bulletin-card')
                    
                    print(f"Found {len(listings)} property listings")
                    
                    if not listings:
                        print("No listings found, assuming end of results")
                        break
                    
                    # Process the listings
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
                            
                            # Extract floor
                            floor_elem = await listing.query_selector('[data-auto="property-floor"]')
                            if floor_elem:
                                floor_text = await floor_elem.text_content()
                                if 'קומת קרקע' in floor_text:
                                    floor = 0
                                else:
                                    floor = ''.join(filter(str.isdigit, floor_text))
                                property_data['floor'] = int(floor) if floor else None
                            
                            # Extract address
                            address_elem = await listing.query_selector('[data-auto="property-address"]')
                            if address_elem:
                                address_text = await address_elem.text_content()
                                address_parts = address_text.split(',')
                                if len(address_parts) >= 3:
                                    property_data['property_type'] = address_parts[0].strip()
                                    property_data['street'] = address_parts[1].strip()
                                    property_data['neighborhood'] = address_parts[2].strip()
                                elif len(address_parts) == 2:
                                    property_data['property_type'] = address_parts[0].strip()
                                    property_data['address'] = address_parts[1].strip()
                                else:
                                    property_data['address'] = address_text
                            
                            property_data['city'] = city
                            property_data['scraped_at'] = datetime.now().isoformat()
                            
                            all_properties.append(property_data)
                            
                        except Exception as e:
                            print(f"Error processing property listing: {str(e)}")
                            continue
                    
                    await self.page.goto(page_url, wait_until="domcontentloaded", timeout=60000)
                    print("Page loaded successfully")
                except Exception as e:
                    print(f"Error loading page: {str(e)}")
                    # Take a screenshot for debugging
                    await self.page.screenshot(path=f"madlan_page_load_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    break
                
                await self.human_like_delay(2, 4)
                
                # Scroll to the bottom gradually
                await self.scroll_to_bottom()
                
                # Wait for content to load after scrolling
                print("Waiting for content to load...")
                try:
                    await self.page.wait_for_load_state("networkidle", timeout=30000)
                    print("Content loaded successfully")
                except Exception as e:
                    print(f"Timeout waiting for content to load: {str(e)}")
                    # Take a screenshot for debugging
                    await self.page.screenshot(path=f"madlan_content_load_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                
                # Check for property listings
                print("Checking for property listings...")
                listings = await self.page.query_selector_all('[data-auto="listed-bulletin-clickable"]')
                print(f"Found {len(listings)} property listings on page {current_page}")
                
                if not listings:
                    print("No listings found, taking screenshot for debugging...")
                    await self.page.screenshot(path=f"madlan_no_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    
                    # Try alternative selector
                    print("Trying alternative selector...")
                    listings = await self.page.query_selector_all('.bulletin-card')
                    print(f"Found {len(listings)} listings with alternative selector")
                    
                    if not listings:
                        has_more_pages = False
                        break
                
                # Process the listings
                for listing in listings:
                    try:
                        # Extract property details
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
                        
                        # Extract floor
                        floor_elem = await listing.query_selector('[data-auto="property-floor"]')
                        if floor_elem:
                            floor_text = await floor_elem.text_content()
                            if 'קומת קרקע' in floor_text:
                                floor = 0
                            else:
                                floor = ''.join(filter(str.isdigit, floor_text))
                            property_data['floor'] = int(floor) if floor else None
                        
                        # Extract address
                        address_elem = await listing.query_selector('[data-auto="property-address"]')
                        if address_elem:
                            address_text = await address_elem.text_content()
                            address_parts = address_text.split(',')
                            if len(address_parts) >= 3:
                                property_data['property_type'] = address_parts[0].strip()
                                property_data['street'] = address_parts[1].strip()
                                property_data['neighborhood'] = address_parts[2].strip()
                            elif len(address_parts) == 2:
                                property_data['property_type'] = address_parts[0].strip()
                                property_data['address'] = address_parts[1].strip()
                            else:
                                property_data['address'] = address_text
                        
                        # Add city
                        property_data['city'] = city
                        
                        # Add timestamp
                        property_data['scraped_at'] = datetime.now().isoformat()
                        
                        all_properties.append(property_data)
                        print(f"Added property: {property_data.get('street', 'Unknown address')}")
                        
                    except Exception as e:
                        print(f"Error processing property listing: {str(e)}")
                        continue
                
                # Check if there are more pages by looking at the next page button
                print("Checking for next page button...")
                next_button = await self.page.query_selector('[data-auto="bulletins-pagination-2"]')
                if next_button:
                    is_visible = await next_button.is_visible()
                    print(f"Next button found, visible: {is_visible}")
                    has_more_pages = is_visible
                else:
                    print("Next button not found")
                    has_more_pages = False
                
                if has_more_pages:
                    current_page += 1
                    print(f"Moving to page {current_page}")
                    # Add a small delay before moving to the next page
                    await self.human_like_delay(1, 2)
                else:
                    print("\nNo more pages to scrape")
                    break
            
            if all_properties:
                # Save all properties to a single JSON file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'madlan_properties_{timestamp}.json'
                filepath = os.path.join(self.madlan_data_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(all_properties, f, ensure_ascii=False, indent=2)
                
                print(f"\nSaved {len(all_properties)} properties to {filepath}")
            else:
                print("\nNo properties found")
            
            return all_properties
            
        except Exception as e:
            print(f"Error scraping properties: {str(e)}")
            return []
        
        finally:
            print("Closing browser...")
            if self.browser:
                await self.browser.close()
            print("Browser closed")

async def main():
    scraper = MadlanDirectService()
    # Example: Scrape properties for Haifa
    properties = await scraper.scrape_properties("חיפה")
    print(f"Found {len(properties)} properties")

if __name__ == "__main__":
    asyncio.run(main()) 