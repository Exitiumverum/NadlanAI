from playwright.sync_api import sync_playwright, TimeoutError
import json
import os
import time

def scrape_city_codes():
    print("Starting browser...")
    with sync_playwright() as p:
        try:
            # Configure browser for speed
            browser = p.chromium.launch(
                headless=True,  # Run in headless mode for speed
                args=['--disable-blink-features=AutomationControlled']
            )
            
            # Create context with minimal configuration
            context = browser.new_context(
                viewport={'width': 1400, 'height': 700},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            print("Navigating to Yad2...")
            # Go directly to the real estate page
            page.goto("https://www.yad2.co.il/realestate/forsale", wait_until="domcontentloaded")
            time.sleep(2)  # Wait for page to fully load
            
            # Find and click search input to open dropdown
            print("Looking for search input...")
            try:
                # Use the ID selector for the search input
                search_input = page.wait_for_selector('#downshift-551-input', timeout=5000)
                if not search_input:
                    raise Exception("Could not find search input")
                
                print("Found search input")
                search_input.click()
                time.sleep(1)  # Wait for dropdown to open
                
            except Exception as e:
                print(f"Error finding search input: {str(e)}")
                # Take screenshot for debugging
                page.screenshot(path='debug_screenshot.png')
                raise
            
            # Get all cities from the dropdown
            print("Extracting cities from dropdown...")
            cities = page.evaluate('''() => {
                // Try multiple selectors for city section
                const citySelectors = [
                    'span.group-list_groupTitle__XSk5p:has-text("עיר")',
                    'span:has-text("עיר")',
                    'div[class*="group-list"] span:has-text("עיר")',
                    'div[class*="location"] span:has-text("עיר")'
                ];
                
                let citySection = null;
                for (const selector of citySelectors) {
                    citySection = document.querySelector(selector);
                    if (citySection) break;
                }
                
                if (!citySection) return [];
                
                // Try to find the city list
                const cityList = citySection.closest('div').querySelector('ul') || 
                               citySection.parentElement.querySelector('ul') ||
                               document.querySelector('ul[class*="city"]');
                
                if (!cityList) return [];
                
                return Array.from(cityList.querySelectorAll('li')).map(li => {
                    const name = li.querySelector('span.highlighted-text_text__SZ7eG')?.textContent.trim() ||
                               li.querySelector('span')?.textContent.trim() ||
                               li.textContent.trim();
                    const code = li.getAttribute('data-value') || 
                               li.getAttribute('value') ||
                               li.getAttribute('id');
                    return { 
                        name, 
                        code,
                        url: `https://www.yad2.co.il/realestate/forsale?city=${code}`
                    };
                }).filter(city => city.name && city.code);
            }''')
            
            if not cities:
                raise Exception("No cities found in dropdown")
            
            print(f"Found {len(cities)} cities")
            
            # Create data directory if it doesn't exist
            os.makedirs('src/data', exist_ok=True)
            
            # Save to JSON file
            output_path = 'src/data/city_codes.json'
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cities, f, ensure_ascii=False, indent=2)
            
            print(f"Saved {len(cities)} cities to {output_path}")
            
            return cities
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise
        finally:
            print("Closing browser...")
            browser.close()

if __name__ == '__main__':
    print("Starting to scrape city codes...")
    try:
        cities = scrape_city_codes()
        print(f"Successfully scraped {len(cities)} cities")
    except Exception as e:
        print(f"Failed to scrape cities: {str(e)}")
        exit(1) 