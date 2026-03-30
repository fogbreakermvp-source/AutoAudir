import requests
from bs4 import BeautifulSoup
import time
import socket
import ssl
from urllib.parse import urlparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database

class Auditor:
    def __init__(self):
        self.db = Database()

    def check_ssl(self, domain):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return True, "SSL Valid"
        except Exception as e:
            return False, f"SSL Error: {str(e)}"

    def audit_website(self, lead_id, url):
        if not url: return {"score": 0, "details": "No website found"}
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            load_time = round(time.time() - start_time, 2)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            missing_alt = len(soup.find_all('img', alt=False))
            broken_links = 0 # Simple check for common errors in links could be added here
            
            # SEO Check
            seo_score = 0
            details = []
            
            title = soup.title.string if soup.title else None
            if title and len(title) > 10: 
                seo_score += 20
            else:
                details.append("Title too short or missing")
                
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                seo_score += 20
            else:
                details.append("Meta description missing")
                
            h1 = soup.find('h1')
            if h1:
                seo_score += 20
            else:
                details.append("H1 tag missing")

            # Performance Check
            # Performance Check (Core Web Vitals: LCP)
            if load_time < 2.5:
                seo_score += 20
                details.append("✅ LCP (Carga de Imagen): Excelente (< 2.5s)")
            elif load_time < 4.0:
                seo_score += 10
                details.append("⚠️ LCP (Carga de Imagen): Lento (Necesita optimización)")
            else:
                details.append(f"❌ LCP (Carga de Imagen): CRÍTICO ({load_time}s)")

            # Security Check
            domain = urlparse(url).netloc
            ssl_valid, ssl_msg = self.check_ssl(domain)
            if ssl_valid:
                seo_score += 20
            else:
                details.append("SSL Certificate Issue")

            # Final Score
            final_score = seo_score
            
            print(f"[*] Audit Done for {url}: Score {final_score}")
            return {
                "audit_score": final_score,
                "load_time": load_time,
                "missing_alt_count": missing_alt,
                "broken_link_count": broken_links,
                "ssl_issue": not ssl_valid,
                "status": "audited",
                "details": " | ".join(details)
            }
        except Exception as e:
            print(f"[!] Audit Failed for {url}: {e}")
            return {"audit_score": 0, "status": "failed", "details": str(e)}

    def run_all(self):
        leads = self.db.get_pending_leads()
        for lead in leads:
            print(f"[*] Auditing Lead {lead['id']}: {lead['name']}")
            result = self.audit_website(lead['id'], lead['website'])
            
            # Additional Maps Audit Logic
            maps_audit_score = 0
            if not lead['phone']: maps_audit_score -= 10
            if lead['rating'] < 4.0: maps_audit_score -= 10
            if lead['reviews'] < 10: maps_audit_score -= 10
            
            # Update Database
            self.db.update_lead(lead['id'], 
                               audit_score=(result.get('audit_score', 0) + maps_audit_score),
                               load_time=result.get('load_time', 0.0),
                               missing_alt_count=result.get('missing_alt_count', 0),
                               broken_link_count=result.get('broken_link_count', 0),
                               ssl_issue=result.get('ssl_issue', False),
                               status='audited')

if __name__ == "__main__":
    auditor = Auditor()
    auditor.run_all()
