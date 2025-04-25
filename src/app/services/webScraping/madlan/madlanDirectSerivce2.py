from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import json

def log_element_details(element, prefix=""):
    """Helper function to log element details"""
    try:
        print(f"{prefix}Tag: {element.tag_name}")
        print(f"{prefix}ID: {element.get_attribute('id')}")
        print(f"{prefix}Class: {element.get_attribute('class')}")
        print(f"{prefix}Type: {element.get_attribute('type')}")
        print(f"{prefix}Placeholder: {element.get_attribute('placeholder')}")
        print(f"{prefix}Visible: {element.is_displayed()}")
        print(f"{prefix}Enabled: {element.is_enabled()}")
    except Exception as e:
        print(f"{prefix}Error getting element details: {str(e)}")

try:
    # Initialize the Firefox driver
    print("\n=== Starting Browser Setup ===")
    browser = webdriver.Firefox()
    browser.maximize_window()
    print("Browser initialized and maximized")

    # Navigate to the website
    print("\n=== Navigating to Website ===")
    browser.get("https://www.madlan.co.il/")
    print("Initial page load complete")

    # Take a screenshot before searching for elements
    browser.save_screenshot("initial_load.png")
    print("Saved initial screenshot")

    # Wait for page to be fully loaded
    time.sleep(5)
    print("\n=== Page Information ===")
    print(f"Current URL: {browser.current_url}")
    print(f"Page Title: {browser.title}")
    print(f"Page Source Length: {len(browser.page_source)}")

    # Debug: Save page source
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(browser.page_source)
    print("Saved page source to page_source.html")

    # Debug: List all iframes
    print("\n=== Checking Iframes ===")
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes")
    for idx, iframe in enumerate(iframes):
        print(f"\nIframe {idx}:")
        log_element_details(iframe, prefix="  ")

    # Debug: Check for shadow roots
    print("\n=== Checking Shadow DOM ===")
    shadow_hosts = browser.execute_script("""
        return Array.from(document.querySelectorAll('*')).filter(el => el.shadowRoot)
    """)
    print(f"Found {len(shadow_hosts)} shadow roots")

    # Debug: List all input elements
    print("\n=== Checking Input Elements ===")
    inputs = browser.find_elements(By.TAG_NAME, "input")
    print(f"Found {len(inputs)} input elements")
    for idx, inp in enumerate(inputs):
        print(f"\nInput Element {idx}:")
        log_element_details(inp, prefix="  ")

    # Debug: Check specific search container
    print("\n=== Checking Search Container ===")
    containers = browser.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
    print(f"Found {len(containers)} combobox containers")
    for idx, container in enumerate(containers):
        print(f"\nCombobox Container {idx}:")
        log_element_details(container, prefix="  ")

    # Try to find search input with various selectors
    wait = WebDriverWait(browser, 20)
    print("\n=== Attempting to Find Search Input ===")
    
    selectors_to_try = [
        # (By.CSS_SELECTOR, 'downshift-69046-input'),
        # (By.CSS_SELECTOR, '[placeholder*="חיפוש"]'),
        # (By.CSS_SELECTOR, 'input[type="search"]'),
        # (By.CSS_SELECTOR, 'input[type="text"]'),
        # (By.CSS_SELECTOR, '.search-input'),
        # (By.XPATH, "//input[contains(@placeholder, 'חיפוש')]"),
        # (By.XPATH, "//div[@role='combobox']//input"),
        (By.XPATH, "//*[@id='downshift-69046-input']"),
        # (By.XPATH, "//input[@role='combobox']")
    ]

    search_input = None
    for selector_type, selector in selectors_to_try:
        print(f"\nTrying selector: {selector_type} = {selector}")
        try:
            elements = browser.find_elements(selector_type, selector)
            print(f"Found {len(elements)} matching elements")
            
            for idx, element in enumerate(elements):
                print(f"\nMatching Element {idx}:")
                log_element_details(element, prefix="  ")
                
            search_input = wait.until(EC.presence_of_element_located((selector_type, selector)))
            print("Successfully found search input!")
            break
        except Exception as e:
            print(f"Selector failed: {str(e)}")

    if search_input:
        print("\n=== Interacting with Search Input ===")
        print("Found search input, attempting to interact...")
        log_element_details(search_input, prefix="  ")
        
        search_input.clear()
        time.sleep(1)
        print("Cleared input")
        
        search_input.send_keys("חיפה")
        time.sleep(1)
        print("Entered text")
        
        search_input.send_keys(Keys.RETURN)
        print("Pressed enter")
    else:
        print("\nFailed to find search input with any selector")
        browser.save_screenshot("failed_search.png")

    # Wait and take final screenshot
    time.sleep(5)
    browser.save_screenshot("final_state.png")

except Exception as e:
    print(f"\n=== Error Occurred ===")
    print(f"Error: {str(e)}")
    try:
        browser.save_screenshot("error_state.png")
        print("Saved error screenshot")
    except:
        print("Could not save error screenshot")

finally:
    print("\n=== Cleanup ===")
    try:
        browser.quit()
        print("Browser closed successfully")
    except:
        print("Could not close browser")




