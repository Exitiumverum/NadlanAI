import asyncio
import json
import random
import time
import os
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup

class Yad2DirectService:
    def __init__(self):
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.properties: List[Dict[str, Any]] = []
        # Create data directory structure
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
        self.search_data_dir = os.path.join(self.data_dir, 'search_data')
        os.makedirs(self.search_data_dir, exist_ok=True)

    async def setup_browser(self):
        """Set up browser with human-like settings"""
        print("Setting up browser...")
        playwright = await async_playwright().start()
        
        # Use a more realistic user agent
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.browser = await playwright.chromium.launch(
            headless=True,  # Run in headless mode for speed
            slow_mo=0,  # Remove delay between actions
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

    async def human_like_delay(self, min_seconds: float = 0.1, max_seconds: float = 0.3):
        """Add minimal delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)

    async def human_like_scroll(self):
        """Fast scroll through the page"""
        viewport_height = await self.page.evaluate("window.innerHeight")
        total_height = await self.page.evaluate("document.body.scrollHeight")
        
        # Scroll to bottom quickly
        await self.page.evaluate(f"window.scrollTo(0, {total_height})")
        await self.human_like_delay(0.1, 0.2)
        
        # Scroll back to top
        await self.page.evaluate("window.scrollTo(0, 0)")
        await self.human_like_delay(0.1, 0.2)

    async def scrape_tzur_hadassah_properties(self) -> List[Dict[str, Any]]:
        """Scrape properties from Yad2 with direct link"""
        try:
            print("Starting browser...")
            await self.setup_browser()
            
            print("Navigating to Yad2...")
            # Go directly to the Tzur Hadassah properties page
            await self.page.goto("https://www.yad2.co.il/realestate/forsale?topArea=100&area=86&city=1113", wait_until="domcontentloaded")
            await self.human_like_delay(2, 3)  # Wait for initial load
            
            # Wait for the feed list to be visible
            print("Waiting for feed list to load...")
            try:
                await self.page.wait_for_selector('ul[data-testid="feed-list"]', state="visible", timeout=15000)
            except Exception as e:
                print(f"Error waiting for feed list: {str(e)}")
                # Try alternative selector
                await self.page.wait_for_selector('.feed-list', state="visible", timeout=15000)
            
            # Wait for at least one property item to be visible
            print("Waiting for property items to load...")
            try:
                # Wait for any of the specific item types
                await self.page.wait_for_selector('li[data-testid="king-item"], li[data-testid="platinum-item"], li[data-testid="item-basic"], li[data-testid="agency-item"]', state="visible", timeout=15000)
            except Exception as e:
                print(f"Error waiting for property items: {str(e)}")
                # Try alternative selectors
                await self.page.wait_for_selector('.feed-item, .platinum-item, .basic-item, .agency-item', state="visible", timeout=15000)
            
            all_properties = []
            current_page = 1
            max_pages = 50  # Set a reasonable maximum number of pages to scrape
            
            while current_page <= max_pages:
                print(f"\nProcessing page {current_page}...")
                
                # Scroll to load more properties on current page
                print("Scrolling to load more properties...")
                last_height = await self.page.evaluate("document.body.scrollHeight")
                scroll_attempts = 0
                max_scroll_attempts = 10  # Maximum number of scroll attempts
                no_new_properties_count = 0
                
                while scroll_attempts < max_scroll_attempts:
                    # Scroll to bottom
                    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await self.human_like_delay(1, 2)  # Wait for new content to load
                    
                    # Calculate new scroll height and compare with last scroll height
                    new_height = await self.page.evaluate("document.body.scrollHeight")
                    
                    # Count current visible properties
                    current_properties = await self.page.query_selector_all('li[data-testid="king-item"], li[data-testid="platinum-item"], li[data-testid="item-basic"], li[data-testid="agency-item"]')
                    print(f"Currently visible properties: {len(current_properties)}")
                    
                    if new_height == last_height:
                        no_new_properties_count += 1
                        if no_new_properties_count >= 2:  # If no new properties for 2 consecutive scrolls
                            print("No new properties loaded after scrolling, assuming all properties are loaded")
                            break
                    else:
                        no_new_properties_count = 0
                    
                    last_height = new_height
                    scroll_attempts += 1
                    print(f"Scroll attempt {scroll_attempts}: Scrolled to load more properties...")
                
                # Final wait to ensure all properties are loaded
                print("Waiting for all properties to be fully loaded...")
                await self.human_like_delay(2, 3)
                
                # Get page content
                content = await self.page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Try multiple selectors to find the feed list
                feed_list = None
                feed_list_selectors = [
                    ('ul', {'data-testid': 'feed-list'}),
                    ('ul', {'class_': 'feed-list'}),
                    ('div', {'class_': 'feed-list'}),
                    ('div', {'data-testid': 'feed-list'})
                ]
                
                for tag, attrs in feed_list_selectors:
                    feed_list = soup.find(tag, attrs=attrs)
                    if feed_list:
                        print(f"Found feed list with selector: {tag} {attrs}")
                        break
                
                if not feed_list:
                    print("Could not find feed list with any selector")
                    break
                
                # Find all property listings with specific data-testid values
                listings = []
                item_types = ['king-item', 'platinum-item', 'item-basic', 'agency-item']
                
                print("\nDEBUG: Starting property search...")
                # Find all items of each type
                for item_type in item_types:
                    print(f"\nDEBUG: Searching for {item_type}...")
                    # Use find_all with exact data-testid matching
                    found_listings = feed_list.find_all('li', attrs={'data-testid': item_type})
                    if found_listings:
                        print(f"Found {len(found_listings)} {item_type} listings")
                        print(f"DEBUG: First {item_type} data-testid: {found_listings[0].get('data-testid')}")
                        listings.extend(found_listings)
                    else:
                        print(f"DEBUG: No {item_type} found")
                
                print(f"\nDEBUG: Total found {len(listings)} property listings on page {current_page}")
                
                # Process properties from current page
                for i, listing in enumerate(listings, 1):
                    try:
                        print(f"\nDEBUG: Processing property {i} of {len(listings)}")
                        print(f"DEBUG: Property data-testid: {listing.get('data-testid')}")
                        
                        # Try multiple selectors for each property detail
                        title_selectors = [
                            'span.item-data-content_heading__tphH4',
                            'span.feed-item-title',
                            'h2.feed-item-title',
                            'div.feed-item-title'
                        ]
                        
                        price_selectors = [
                            'span.feed-item-price_price__ygoeF',
                            'span.feed-item-price',
                            'div.feed-item-price'
                        ]
                        
                        location_selectors = [
                            'span.item-data-content_itemInfoLine__AeoPP',
                            'span.feed-item-location',
                            'div.feed-item-location'
                        ]
                        
                        # Find title
                        title = "No title"
                        for selector in title_selectors:
                            title_elem = listing.select_one(selector)
                            if title_elem:
                                title = title_elem.text.strip()
                                print(f"DEBUG: Found title with selector {selector}: {title}")
                                break
                        
                        # Find price
                        price = "Price not available"
                        for selector in price_selectors:
                            price_elem = listing.select_one(selector)
                            if price_elem:
                                price = price_elem.text.strip()
                                print(f"DEBUG: Found price with selector {selector}: {price}")
                                break
                        
                        # Find location
                        location = "Location not available"
                        for selector in location_selectors:
                            location_elem = listing.select_one(selector)
                            if location_elem:
                                location = location_elem.text.strip()
                                print(f"DEBUG: Found location with selector {selector}: {location}")
                                break
                        
                        # Extract rooms and size
                        info_lines = listing.find_all(['span', 'div'], class_=lambda x: x and ('itemInfoLine' in x or 'feed-item-info' in x))
                        rooms_size = info_lines[1].text.strip() if len(info_lines) > 1 else "N/A"
                        print(f"DEBUG: Found rooms_size: {rooms_size}")
                        
                        rooms = "N/A"
                        size = "N/A"
                        if rooms_size != "N/A":
                            parts = rooms_size.split('•')
                            if len(parts) >= 3:
                                rooms = parts[0].strip()
                                size = parts[2].strip()
                                print(f"DEBUG: Parsed rooms: {rooms}, size: {size}")
                        
                        # Find image
                        image_url = None
                        image_elem = listing.find('img')
                        if image_elem and 'src' in image_elem.attrs:
                            image_url = image_elem['src']
                            print(f"DEBUG: Found image URL: {image_url}")
                        
                        # Find link
                        property_link = None
                        link_elem = listing.find('a', href=True)
                        if link_elem:
                            property_link = link_elem['href']
                            if not property_link.startswith('http'):
                                property_link = f"https://www.yad2.co.il{property_link}"
                            print(f"DEBUG: Found property link: {property_link}")
                        
                        # Find broker
                        broker = "N/A"
                        broker_elem = listing.find(['span', 'div'], class_=lambda x: x and ('abovePrice' in x or 'broker' in x))
                        if broker_elem:
                            broker = broker_elem.text.strip()
                            print(f"DEBUG: Found broker: {broker}")
                        
                        property_data = {
                            'title': title,
                            'price': price,
                            'location': location,
                            'rooms': rooms,
                            'size': size,
                            'image': image_url,
                            'broker': broker,
                            'link': property_link,
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        all_properties.append(property_data)
                        print(f"Added property: {title}")
                        
                    except Exception as e:
                        print(f"Error processing listing: {str(e)}")
                        continue
                
                # Check for next page button
                try:
                    next_page_button = await self.page.query_selector('a.pagination-arrow_button__ayr9j[aria-label="עמוד הבא"]')
                    if next_page_button and await next_page_button.is_visible():
                        print(f"\nFound next page button, moving to page {current_page + 1}")
                        # Get the href attribute
                        href = await next_page_button.get_attribute('href')
                        if href:
                            # Navigate to the next page URL
                            next_page_url = f"https://www.yad2.co.il{href}"
                            print(f"Navigating to next page: {next_page_url}")
                            await self.page.goto(next_page_url, wait_until="domcontentloaded")
                            await self.human_like_delay(2, 3)  # Wait for next page to load
                            current_page += 1
                        else:
                            print("\nNo href found in next page button")
                            break
                    else:
                        print("\nNo more pages to scrape")
                        break
                except Exception as e:
                    print(f"Error checking for next page: {str(e)}")
                    break
            
            if all_properties:
                # Save all properties to JSON file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'tzur_hadassah_properties_{timestamp}.json'
                filepath = os.path.join(self.search_data_dir, filename)
                
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
    scraper = Yad2DirectService()
    properties = await scraper.scrape_tzur_hadassah_properties()
    print(f"Found {len(properties)} properties")

if __name__ == "__main__":
    asyncio.run(main()) 