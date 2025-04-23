import os
import sys
from scrape_city_codes import scrape_city_codes

def main():
    # Create data directory if it doesn't exist
    os.makedirs('src/data', exist_ok=True)
    
    try:
        cities = scrape_city_codes()
        print(f"Successfully scraped {len(cities)} cities")
        print("Data saved to src/data/city_codes.json")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 