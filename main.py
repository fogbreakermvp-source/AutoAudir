import os
import sys
import time
import asyncio

# AuditAutoPro 2026 - Cloud-Ready Pipeline
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from libs.google_maps_scraper.main import GoogleMapsScraper
from libs.seo_audit_tool.main import HyperAuditor
from src.form_sniper import FormSniper
from src.auditor import Auditor
from src.database import Database
from src.logger import audit_logger

IS_CLOUD = os.getenv('GITHUB_ACTIONS') == 'true'

def main():
    print("=== AUDITAUTOPRO 2026: CLOUD PIPELINE ===")
    db = Database()
    
    # 1. Scrape Leads
    print("\n[Step 1/4] Scraping High-Ticket Leads...")
    scraper = GoogleMapsScraper()
    scraper.run()
    
    # 2. Audit Leads (real audits via requests, no browser needed)
    print("\n[Step 2/4] Auditing Leads...")
    auditor = Auditor()
    auditor.run_all()
    
    # 3. Count what we found
    all_leads = db.get_pending_leads()
    audited = db.get_audited_leads() if hasattr(db, 'get_audited_leads') else []
    print(f"\n[Stats] Scraped: {len(all_leads)} pending | Audited: {len(audited)}")
    
    # 4. Outreach via Form Injection (WORKS IN CLOUD - no browser needed)
    print("\n[Step 3/4] Form Injection Outreach (Cloud-Compatible)...")
    sniper = FormSniper()
    asyncio.run(sniper.run_batch(limit=100))
    
    # 5. Log results
    print("\n[Step 4/4] Logging Results...")
    contacted = db.get_contacted_leads() if hasattr(db, 'get_contacted_leads') else []
    audit_logger.log("PIPELINE_COMPLETE", f"Leads scraped: {len(all_leads)} | Contacted: {len(contacted)}")
    
    for lead in contacted[:10]:  # Log first 10 contacts as proof
        audit_logger.log("CONTACT_PROOF", f"✅ {lead.get('name','?')} | {lead.get('website','?')} | {lead.get('contacted_at','?')}")
    
    print(f"\n=== PIPELINE COMPLETE: {len(contacted)} leads contacted ===")

if __name__ == "__main__":
    main()
