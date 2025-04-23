import asyncio
import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup

class WebScrapeService:
    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.properties: List[Dict[str, Any]] = []

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
            
            # If specific close button not found, try other modal handling
            modal_selectors = [
                '.modal',
                '.modal-dialog',
                '.modal-content',
                '.popup',
                '.popup-content',
                '.overlay',
                '.dialog'
            ]
            
            for modal_selector in modal_selectors:
                try:
                    modals = await self.page.query_selector_all(modal_selector)
                    for modal in modals:
                        if await modal.is_visible():
                            print(f"Found modal with selector: {modal_selector}")
                            
                            # Try to find and click close buttons within the modal
                            for close_selector in close_button_selectors:
                                try:
                                    close_buttons = await modal.query_selector_all(close_selector)
                                    for button in close_buttons:
                                        if await button.is_visible():
                                            print(f"Found close button with selector: {close_selector}")
                                            await button.click()
                                            await self.human_like_delay(0.2, 0.5)  # Reduced delay
                                            return True
                                except Exception as e:
                                    print(f"Error with close button selector {close_selector}: {str(e)}")
                                    continue
                            
                            # If no close button found, try clicking the modal itself
                            try:
                                print("No close button found, trying to click the modal itself")
                                await modal.click()
                                await self.human_like_delay(0.2, 0.5)  # Reduced delay
                                return True
                            except Exception as e:
                                print(f"Error clicking modal: {str(e)}")
                except Exception as e:
                    print(f"Error with modal selector {modal_selector}: {str(e)}")
                    continue
            
            return False
                    
        except Exception as e:
            print(f"Error in handle_modals: {str(e)}")
            return False

    async def handle_ads_and_popups(self):
        """Handle ads, popups, and other overlays"""
        try:
            # First try to handle any modals
            if await self.handle_modals():
                return
            
            # Then handle other types of ads/popups
            ad_selectors = [
                '.advertisement',
                '.cookie-banner',
                '.cookie-consent',
                '.cookie-popup'
            ]
            
            # Try to close any visible ads or popups
            for selector in ad_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        if await element.is_visible():
                            print(f"Found and closing element with selector: {selector}")
                            await element.click()
                            await self.human_like_delay(0.5, 1.0)
                except Exception as e:
                    print(f"Error handling element with selector {selector}: {str(e)}")
                    continue
            
            # Handle iframe ads
            frames = self.page.frames
            for frame in frames:
                try:
                    # Try to find and click close buttons in iframes
                    close_buttons = await frame.query_selector_all('button.close, .close-button, .x-button')
                    for button in close_buttons:
                        if await button.is_visible():
                            await button.click()
                            await self.human_like_delay(0.5, 1.0)
                except Exception as e:
                    print(f"Error handling iframe: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in handle_ads_and_popups: {str(e)}")

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
            await self.handle_ads_and_popups()
            
            # Occasionally scroll back up a bit
            if random.random() < 0.2:
                await self.page.evaluate(f"window.scrollBy(0, -{random.randint(100, 300)})")
                await self.human_like_delay(0.5, 1.0)

    async def find_and_click_real_estate_link(self):
        """Find and click the real estate section link with multiple selector attempts"""
        selectors = [
            'a[href="/realestate/forsale"]',
            'a[href*="realestate"]',
            'a:has-text("נדל\"ן")',
            'a:has-text("נדל''ן")',
            'a:has-text("נדלן")'
        ]
        
        for selector in selectors:
            try:
                link = await self.page.wait_for_selector(selector, timeout=5000)
                if link:
                    print(f"Found real estate link with selector: {selector}")
                    await link.click()
                    return True
            except Exception as e:
                print(f"Selector {selector} failed: {str(e)}")
                continue
        
        return False

    async def find_and_fill_search_input(self):
        """Find and fill the location search input with multiple selector attempts"""
        selectors = [
            'input[placeholder*="אזור"]',
            'input[placeholder*="מיקום"]',
            'input[placeholder*="כתובת"]',
            'input[placeholder*="עיר"]',
            'input[placeholder*="יישוב"]',
            'input[name*="location"]',
            'input[name*="area"]',
            'input[name*="address"]',
            'input.search-input[placeholder*="חפשו"]',
            'input.search-input[placeholder*="חיפוש"]'
        ]
        
        for selector in selectors:
            try:
                search_input = await self.page.wait_for_selector(selector, timeout=5000)
                if search_input:
                    print(f"Found location search input with selector: {selector}")
                    # Clear any existing text
                    await search_input.fill("")
                    await self.human_like_delay(0.2, 0.5)  # Reduced delay
                    # Type the location with human-like typing
                    await search_input.type("צור הדסה", delay=random.uniform(50, 150))  # Reduced delay
                    
                    # Wait for dropdown to appear
                    await self.human_like_delay(0.5, 1.0)  # Reduced delay
                    
                    # Try to find and click the city name under the עיר span
                    try:
                        # First find the עיר section
                        city_section = await self.page.wait_for_selector('span.group-list_groupTitle__XSk5p:has-text("עיר")', timeout=5000)
                        if city_section:
                            print("Found עיר section")
                            # Find the city name under the עיר section
                            city_name = await self.page.wait_for_selector('ul#עיר li.option_option__vHSMz span.highlighted-text_text__SZ7eG:has-text("צור הדסה")', timeout=5000)
                            if city_name:
                                print("Found city name under עיר section")
                                await city_name.click()
                                await self.human_like_delay(0.2, 0.5)  # Reduced delay
                                return True
                    except Exception as e:
                        print(f"Error finding city name: {str(e)}")
                    
                    return True
            except Exception as e:
                print(f"Selector {selector} failed: {str(e)}")
                continue
        
        return False

    async def find_and_click_search_button(self):
        """Find and click the search button with multiple selector attempts"""
        selectors = [
            'button:has-text("חיפוש")',
            'button:has-text("חפש")',
            'button.search-button',
            'button[type="submit"]',
            'form button'
        ]
        
        for selector in selectors:
            try:
                button = await self.page.wait_for_selector(selector, timeout=5000)
                if button:
                    print(f"Found search button with selector: {selector}")
                    # Add a small delay before clicking to appear more human-like
                    await self.human_like_delay(0.5, 1.0)
                    await button.click()
                    return True
            except Exception as e:
                print(f"Selector {selector} failed: {str(e)}")
                continue
        
        return False

    async def click_nadlan_button(self):
        """Click the נדל״ן button"""
        try:
            # Try to find and click the נדל״ן button
            button = await self.page.wait_for_selector('a:has-text("נדל״ן")', timeout=5000)
            if button:
                print("Found נדל״ן button")
                await button.click()
                return True
        except Exception as e:
            print(f"Error clicking נדל״ן button: {str(e)}")
            return False

    async def wait_for_search_results(self):
        """Wait for search results to load with multiple selector attempts"""
        selectors = [
            '.feed_item',
            '.feed-list',
            '.search-results',
            '.results-list',
            '.property-list',
            '.item-list'
        ]
        
        for selector in selectors:
            try:
                print(f"Waiting for results with selector: {selector}")
                await self.page.wait_for_selector(selector, state="visible", timeout=10000)
                print(f"Found results with selector: {selector}")
                return True
            except Exception as e:
                print(f"Selector {selector} failed: {str(e)}")
                continue
        
        return False

    async def scrape_tzur_hadassah_properties(self) -> List[Dict[str, Any]]:
        """Scrape properties from Yad2 with human-like behavior"""
        try:
            print("Starting browser...")
            await self.setup_browser()
            
            print("Navigating to Yad2...")
            # First go to main page
            await self.page.goto("https://www.yad2.co.il", wait_until="domcontentloaded")
            await self.human_like_delay(2, 4)
            
            # Handle any initial ads/popups and modals
            await self.handle_ads_and_popups()
            
            # Click the נדל״ן button
            print("Looking for נדל״ן button...")
            if not await self.click_nadlan_button():
                raise Exception("Could not find נדל״ן button")
            await self.human_like_delay(2, 4)
            
            # Handle any ads/popups and modals after navigation
            await self.handle_ads_and_popups()
            
            # Find and fill search input
            if not await self.find_and_fill_search_input():
                raise Exception("Could not find search input")
            await self.human_like_delay(1, 2)
            
            # Click search button
            if not await self.find_and_click_search_button():
                raise Exception("Could not find search button")
            await self.human_like_delay(2, 4)
            
            # Handle any ads/popups and modals after search
            await self.handle_ads_and_popups()
            
            # Wait for results to load
            if not await self.wait_for_search_results():
                raise Exception("Could not find search results")
            await self.human_like_delay(2, 3)
            
            # Scroll through results
            await self.human_like_scroll()
            
            # Get page content
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all property listings with multiple selectors
            listings = []
            listing_selectors = [
                'div.feed_item',
                'div.feed-list-item',
                'div.property-item',
                'div.search-result-item',
                'div.item'
            ]
            
            for selector in listing_selectors:
                found_listings = soup.select(selector)
                if found_listings:
                    print(f"Found {len(found_listings)} listings with selector: {selector}")
                    listings = found_listings
                    break
            
            for listing in listings:
                try:
                    # Extract property details with error handling
                    title_elem = listing.find(['div', 'h2'], class_=['title', 'item-title'])
                    title = title_elem.text.strip() if title_elem else "No title"
                    
                    price_elem = listing.find(['div', 'span'], class_=['price', 'item-price'])
                    price = price_elem.text.strip() if price_elem else "Price not available"
                    
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

async def main():
    scraper = WebScrapeService()
    properties = await scraper.scrape_tzur_hadassah_properties()
    print(f"Found {len(properties)} properties")

if __name__ == "__main__":
    asyncio.run(main()) 