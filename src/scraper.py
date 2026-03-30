from seleniumbase import SB
import time
import random
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database

class GoogleMapsScraper:
    def __init__(self):
        self.db = Database()
        # Industrial Global Target List
        self.targets = [
            {"niche": "Plastic Surgeon", "locations": ["Miami, FL", "Beverly Hills, CA", "Madrid, ES", "London, UK", "Dubai, UAE"]},
            {"niche": "Luxury Real Estate", "locations": ["Manhattan, NY", "Mayfair, London", "Dubai Marina, UAE", "Monaco", "Zurich, CH"]},
            {"niche": "Wealth Management", "locations": ["Geneva, CH", "Singapore", "Hong Kong", "Wall Street, NY", "Grand Cayman"]},
            {"niche": "Commercial Law Firm", "locations": ["Sydney, AU", "Toronto, CA", "Berlin, DE", "Paris, FR", "Tokyo, JP"]}
        ]
        self.current_idx = 0

    def scrape(self, keyword, location, limit=50):
        search_query = f"{keyword} in {location}"
        print(f"[*] Searching for: {search_query}")
        
        with SB(uc=True, headless=True) as sb:
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            sb.open(url)
            
            # Consent button if present
            try:
                if sb.is_element_visible('button[aria-label="Accept all"]'):
                    sb.click('button[aria-label="Accept all"]')
            except:
                pass

            # Scroll to load more results
            try:
                if sb.is_element_present('div[role="feed"]'):
                    for _ in range(5):
                        sb.execute_script("document.querySelector('div[role=\"feed\"]').scrollTop += 1000")
                        time.sleep(random.uniform(1, 2))
                else:
                    # Fallback scroll if 'feed' role is not found
                    for _ in range(3):
                        sb.press_key("body", "PageDown")
                        time.sleep(1)
            except:
                pass

            # Extract lead details
            leads = sb.find_elements('div[role="article"]')
            count = 0
            for lead in leads:
                if count >= limit: break
                try:
                    # Click to load details
                    lead.click()
                    time.sleep(random.uniform(1.5, 2.5))
                    
                    data = {
                        "name": sb.get_text('h1.DUwDvf'),
                        "website": sb.get_attribute('a[data-item-id="authority"]', "href") if sb.is_element_present('a[data-item-id="authority"]') else None,
                        "phone": sb.get_text('button[data-item-id^="phone:tel"]') if sb.is_element_present('button[data-item-id^="phone:tel"]') else None,
                        "address": sb.get_text('button[data-item-id="address"]') if sb.is_element_present('button[data-item-id="address"]') else None,
                        "rating": float(sb.get_text('span.ceNzR').replace(',', '.')) if sb.is_element_present('span.ceNzR') else 0.0,
                        "reviews": int(sb.get_text('span.F7nice span:nth-child(2)').strip('()').replace('.', '')) if sb.is_element_present('span.F7nice span:nth-child(2)') else 0,
                        "niche": keyword,
                        "location": location
                    }
                    
                    if self.db.add_lead(data):
                        print(f"[+] Lead Saved: {data['name']} - {data['website']}")
                        count += 1
                except Exception as e:
                    print(f"[!] Error extracting lead: {e}")
                    continue

    def run_all(self):
        for target in self.targets:
            for loc in target['locations']:
                self.scrape(target['niche'], loc)

if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    scraper.run_all()
