from seleniumbase import SB
import time
import random
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.database import Database

class GoogleMapsScraper:
    def __init__(self):
        self.db = Database()
        self.niches = ["Luxury Real Estate Agency", "High-End Dental Clinic", "Law Firm"]
        self.locations = ["Miami, FL", "Los Angeles, CA", "New York, NY", "Beverly Hills, CA"]

    def run(self):
        print("[+] SCRAPING USA: Using high-ticket US parameters...")
        for niche in self.niches:
            for loc in self.locations:
                self.scrape(niche, loc)

    def scrape(self, keyword, location):
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

            # Scroll to load more results (Robust scroll logic from GH tools)
            for _ in range(2): 
                sb.execute_script("""
                    {
                        const el = document.querySelector('div[role="feed"]') || 
                                   document.querySelector('div[aria-label^="Results for"]') || 
                                   document.querySelector('.m67qEc');
                        if (el) el.scrollTop += 1000;
                    }
                """)
                time.sleep(1.5)

            # Extract lead details
            leads = sb.find_elements('div[role="article"]')
            for lead in leads[:3]: # Limited to 3 for demo
                try:
                    lead.click()
                    time.sleep(2)
                    
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
                        print(f"[+] Lead Saved: {data['name']}")
                except:
                    continue
