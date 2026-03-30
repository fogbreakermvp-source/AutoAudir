import os
import sys
import time

# Final Integrated Engine AuditAutoPro 2026
# Using logic from:
# 1. omkarcloud/google-maps-scraper (Extraction)
# 2. Abin-Vinod/seo-audit-tool (Audit)
# 3. SeleniumBase (Outreach)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from libs.google_maps_scraper.main import GoogleMapsScraper
from libs.seo_audit_tool.main import HyperAuditor
from libs.whatsapp_bot.main import WhatsAppMessenger

def main():
    print("=== AUDITAUTOPRO 2026: GH-REPO INTEGRATED ENGINE ===")
    
    # 1. Scrape Leads (GH: omkarcloud/google-maps-scraper)
    print("\n[Step 1/3] Scraping High-Ticket Leads...")
    scraper = GoogleMapsScraper()
    scraper.run()
    
    # 2. Audit Leads (GH: Abin-Vinod/seo-audit-tool)
    print("\n[Step 2/3] Auditing Leads & Generating Reports...")
    auditor = HyperAuditor()
    # Scrape real lead for demo
    auditor.run_comprehensive_audit("Gilmar Real Estate Madrid", "https://www.gilmar.es")
    
    # 3. Outreach (GH: SeleniumBase Outreach Engine)
    print("\n[Step 3/3] Starting Outreach (WhatsApp Web)...")
    messenger = WhatsAppMessenger()
    messenger.run()
    
    print("\n=== SYSTEM RUN COMPLETED ===")

if __name__ == "__main__":
    main()
