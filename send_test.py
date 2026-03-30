"""
Test: Audit a real lead and SEND the result via WhatsApp (LIVE).
"""
import os
import sys
import time
from urllib.parse import quote

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from libs.seo_audit_tool.main import HyperAuditor
from libs.whatsapp_bot.main import WhatsAppMessenger
from seleniumbase import SB

# --- 1. Audit a REAL lead ---
lead_name = "Engel & Volkers Miami"
lead_website = "https://www.evrealestate.com/en-us/miami/"

print(f"[Step 1] Auditing: {lead_name}")
auditor = HyperAuditor()
results = auditor.run_comprehensive_audit(lead_name, lead_website)

print("[+] Audit complete. Preparing message...")

# --- 2. Build lead data from real audit ---
lead_data = {
    "name": lead_name,
    "lcp": results["performance"]["lcp"].split("(")[0].strip(),
    "broken_links": results["ux"]["broken_links"].split(" ")[1],
    "missing_alt": results["seo"]["alt_tags"].split(" ")[1],
}

# --- 3. Send LIVE via WhatsApp ---
phone = "59895574199"
print(f"[Step 2] Sending LIVE to WhatsApp: {phone}")

messenger = WhatsAppMessenger()
msg = messenger.get_audit_message(lead_data)
encoded_msg = quote(msg)

user_data_dir = os.path.abspath("data/whatsapp_session")
url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

with SB(uc=True, user_data_dir=user_data_dir, headless=False) as sb:
    sb.open(url)
    print("[*] Waiting for WhatsApp to load...")
    time.sleep(15)
    
    # Wait for the send button to appear
    try:
        sb.wait_for_element_visible('span[data-icon="send"]', timeout=30)
        print("[*] Send button found. Sending...")
        sb.click('span[data-icon="send"]')
        print("[+] MESSAGE SENT SUCCESSFULLY!")
        time.sleep(5)  # Let it send
    except Exception as e:
        print(f"[!] Could not find send button, trying Enter key...")
        try:
            sb.press_keys('div[title="Type a message"], div[title="Escribe un mensaje"]', "\n")
            print("[+] MESSAGE SENT VIA ENTER KEY!")
            time.sleep(5)
        except Exception as e2:
            print(f"[!] Failed to send: {e2}")
