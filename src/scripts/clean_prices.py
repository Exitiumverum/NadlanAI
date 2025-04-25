import json
import os

def clean_price(price_str):
    if price_str == "Price not available":
        return "Price not available"
    # Remove currency symbol (₪) and any commas, keep only digits
    return ''.join(filter(str.isdigit, price_str))

def process_json_file(filepath):
    # Read the JSON file
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Clean prices for each property
    for property in data:
        property['price'] = clean_price(property['price'])
    
    # Write back to the same file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(data)} properties in {filepath}")

if __name__ == "__main__":
    filepath = "src/data/search_data/Location not available_properties_20250425_152428.json"
    process_json_file(filepath) 