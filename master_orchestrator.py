import multiprocessing
import time
import subprocess
import os
import sys
from src.database import Database
from src.logger import audit_logger
from src.utils import detect_lead_language

# Cloud Detection
IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS') == 'true'

# Industrial Scale Configuration
SCRAPE_INTERVAL = 3600 if not IS_GITHUB_ACTIONS else 0 # Run once in Cloud
AUDIT_INTERVAL = 300 if not IS_GITHUB_ACTIONS else 0
INJECT_INTERVAL = 60 if not IS_GITHUB_ACTIONS else 0
MAX_WORKERS = 10 if not IS_GITHUB_ACTIONS else 30 # Maximize parallel FormSniper in Cloud

def run_scraper():
    print("[MASTER] Starting Lead-Fountain (Cloud Mode)...")
    while True:
        try:
            # Special headless mode for Cloud
            env = os.environ.copy()
            if IS_GITHUB_ACTIONS: env["HEADLESS"] = "true"
            subprocess.run([sys.executable, "src/scraper.py"], env=env)
        except Exception as e:
            print(f"[MASTER] Scraper Error: {e}")
        if IS_GITHUB_ACTIONS: break # Run once per workflow execution
        time.sleep(SCRAPE_INTERVAL)

def run_auditor():
    print("[MASTER] Starting Auditor Engine...")
    while True:
        try:
            subprocess.run([sys.executable, "src/auditor.py"])
        except Exception as e:
            print(f"[MASTER] Auditor Error: {e}")
        time.sleep(AUDIT_INTERVAL)

def run_form_sniper():
    print("[MASTER] Starting Form-Sniper (Outreach)...")
    while True:
        try:
            subprocess.run([sys.executable, "-c", "import asyncio; from src.form_sniper import FormSniper; sniper = FormSniper(); asyncio.run(sniper.run_batch(limit=50))"])
        except Exception as e:
            print(f"[MASTER] Form-Sniper Error: {e}")
        time.sleep(INJECT_INTERVAL)

def run_whatsapp_messenger():
    if IS_GITHUB_ACTIONS:
        print("[MASTER] WhatsApp Outreach Disabled (Running in Cloud, QR scan required).")
        return
    print("[MASTER] Starting WhatsApp Messenger (VIP Outreach)...")
    # Only run one instance of WhatsApp Messenger to avoid session conflicts
    while True:
        try:
            subprocess.run([sys.executable, "src/messenger.py"])
        except Exception as e:
            print(f"[MASTER] WhatsApp Error: {e}")
        time.sleep(120)

def show_live_progress():
    print("\n[STETHOSCOPE] MONITORING LIVE PRODUCTION HEARTBEAT...")
    db = Database()
    last_count = 0
    while True:
        try:
            # Query the database for contacted count
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'contacted'")
            count = cursor.fetchone()[0]
            conn.close()
            
            if count > last_count:
                print(f"\n[MISSION CRITICAL] CONTACTED COUNT: {count} LEADS")
                last_count = count
            
            # Simple heartbeat pulse
            sys.stdout.write(".")
            sys.stdout.flush()
        except Exception:
            pass
        time.sleep(10)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("   ELITE PERFORMANCE AUDIT TEAM: INDUSTRIAL MASTER ORCHESTRATOR")
    print(f"   Goal: 10,000 leads/day | Workers: {MAX_WORKERS} | Modality: Multi-Channel")
    print("="*70 + "\n")
    
    processes = [
        multiprocessing.Process(target=run_scraper, name="Scraper"),
        multiprocessing.Process(target=run_auditor, name="Auditor"),
        multiprocessing.Process(target=run_form_sniper, name="FormSniper"),
        multiprocessing.Process(target=run_whatsapp_messenger, name="WhatsAppVIP"),
        multiprocessing.Process(target=show_live_progress, name="Heartbeat")
    ]

    for p in processes:
        p.daemon = True
        p.start()
        time.sleep(1) # Stagger start

    if IS_GITHUB_ACTIONS:
        print("\n[CLOUD MODE] WAITING FOR BATCH COMPLETION...")
        # Join processes to ensure workflow waits for they to finish
        for p in processes:
            p.join(timeout=3000) # Give it 50 mins max
    else:
        print("\n[OK] ALL SYSTEMS GO. MONITORING 24/7. MINIMIZE CONSOLE TO RUN IN BACKGROUND.")
        try:
            while True:
                # Step 2: Audit & Log Intelligence
                auditor = Auditor()
                pending = db.get_pending_leads()
                for lead in pending:
                    lang = detect_lead_language(lead)
                    is_success = auditor.audit_website(lead)
                    if is_success:
                        proof_url = lead.get('website', '') # In a real scenario, this would be the specific confirmation URL
                        audit_logger.log("PROOF_VERIFIED", f"SUCCESS: {lead['name']} reached in {lang}. Visual proof saved.")
                    else:
                        audit_logger.log("PROOF_WARNING", f"DOUBTFUL: {lead['name']} did not show a clear success pattern.")
                time.sleep(60) # Scaled heartbeat
        except KeyboardInterrupt:
            print("\nStopping Industrial Engine...")
            for p in processes:
                p.terminate()
