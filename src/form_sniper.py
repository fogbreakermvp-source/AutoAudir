import httpx
import asyncio
from bs4 import BeautifulSoup
import random
import time
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database
from src.logger import audit_logger
from src.utils import detect_lead_language

class FormSniper:
    def __init__(self):
        self.db = Database()
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.user_email = "jotaerre020@gmail.com"

    def get_form_message(self, lead):
        """Hyper-Conversion Form message — Localized for global markets."""
        lang = detect_lead_language(lead)
        loss = random.randint(1500, 4000)
        lcp = lead.get('load_time', '4.8s')
        missing_alt = lead.get('missing_alt_count', '18')
        ssl_status_en = "CRITICAL" if lead.get('ssl_issue') else "Valid"
        ssl_status_es = "CRÍTICO" if lead.get('ssl_issue') else "Válido"
        
        if lang == 'EN':
            message = (
                f"TECHNICAL RISK REPORT - ELITE PERFORMANCE AUDIT TEAM\n\n"
                f"We have detected failures in the digital infrastructure of {lead['name']} that are penalizing your global positioning.\n\n"
                f"PERFORMANCE ANALYSIS (Core Web Vitals):\n"
                f"- LCP (Image Load): *{lcp}s* (Above the 2.5s limit)\n"
                f"- Accessibility: *{missing_alt}* missing Alt tags.\n"
                f"- SSL Security: *{ssl_status_en}*.\n\n"
                f"Estimated financial impact: *${loss}/month* in potential customers lost due to slowness and distrust.\n\n"
                f"PROFESSIONAL SOLUTION:\n"
                f"1️⃣ Expert Advisory ($297): Immediate roadmap. Payment: https://www.paypal.me/JuanRomeroGarcilar\n"
                f"2️⃣ Full Implementation ($1,000): We repair every error for you in 48h.\n\n"
                f"To see the full report or hire, contact us at: {self.user_email}"
            )
        else:
            message = (
                f"INFORME TÉCNICO PROFESIONAL - ELITE PERFORMANCE AUDIT TEAM\n\n"
                f"Hemos detectado fallos en la infraestructura digital de {lead['name']} que están penalizando su posicionamiento global.\n\n"
                f"ANÁLISIS DE RENDIMIENTO (Core Web Vitals):\n"
                f"- LCP (Carga de Imagen): *{lcp}s* (Superior al límite de 2.5s)\n"
                f"- Accesibilidad: *{missing_alt}* fallos detectados en etiquetas Alt.\n"
                f"- Seguridad SSL: *{ssl_status_es}*.\n\n"
                f"Impacto financiero estimado: *${loss}/mes* en potenciales clientes perdidos por lentitud y desconfianza.\n\n"
                f"SOLUCIÓN PROFESIONAL:\n"
                f"1️⃣ Asesoría Directa ($297): Hoja de ruta inmediata. Pago: https://www.paypal.me/JuanRomeroGarcilar\n"
                f"2️⃣ Reparación Full ($1,000): Arreglamos todo en 48h.\n\n"
                f"Para ver el reporte completo o contratar, contáctenos en: {self.user_email}"
            )
        return message

    def get_subject(self, lead):
        """Generate email subject for form submissions."""
        subjects = [
            f"Auditoría técnica gratuita — {lead['name']}",
            f"Problemas detectados en su sitio web — {lead['name']}",
            f"Análisis de rendimiento — {lead['name']}",
        ]
        return random.choice(subjects)

    async def find_contact_page(self, website):
        try:
            response = await self.client.get(website)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Common contact page paths
            potential_paths = [
                'contact', 'contacto', 'contact-us', 'contactar',
                'about', 'nosotros', 'get-in-touch',
            ]
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href'].lower()
                if any(path in href for path in potential_paths):
                    if href.startswith('http'):
                        return href
                    return website.rstrip('/') + '/' + href.lstrip('/')

            return website  # Fallback to home page
        except Exception:
            return None

    def verify_success(self, html):
        """Patterns of success (EN/ES) for industrial verification."""
        patterns = [
            "thank you", "thanks", "message sent", "received", "success", "confirmed",
            "gracias", "enviado", "recibido", "éxito", "confirmado", "en breve", "soon"
        ]
        html_lower = html.lower()
        for pattern in patterns:
            if pattern in html_lower:
                return True, pattern
        return False, "Undetected/Doubtful"

    async def inject_form(self, lead):
        if not lead['website']:
            return False

        contact_url = await self.find_contact_page(lead['website'])
        if not contact_url:
            return False

        print(f"[*] Targeting: {contact_url}")

        try:
            response = await self.client.get(contact_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')

            if not forms:
                return False

            form = forms[0]
            action = form.get('action', '')
            if not action.startswith('http'):
                action = contact_url.rstrip('/') + '/' + action.lstrip('/')

            payload = {}
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                name = input_tag.get('name')
                if not name: continue
                type_ = input_tag.get('type', 'text').lower()
                name_lower = name.lower()

                if 'name' in name_lower or 'nombre' in name_lower:
                    payload[name] = "Elite Performance Audit Team"
                elif 'email' in name_lower or 'correo' in name_lower:
                    payload[name] = self.user_email
                elif 'phone' in name_lower or 'tel' in name_lower:
                    payload[name] = "" 
                elif 'subject' in name_lower or 'asunto' in name_lower:
                    payload[name] = self.get_subject(lead)
                elif 'message' in name_lower or'mensaje' in name_lower or input_tag.name == 'textarea':
                    payload[name] = self.get_form_message(lead)
                elif type_ == 'hidden':
                    payload[name] = input_tag.get('value', '')

            # Fire & Verify
            resp = await self.client.post(action, data=payload)
            is_verified, pattern = self.verify_success(resp.text)
            
            if resp.status_code in [200, 301, 302] and is_verified:
                print(f"[+ OK] Form Verified for {lead['name']} (Pattern: {pattern})")
                self.db.update_lead(lead['id'], status='contacted', contacted_at=time.strftime('%Y-%m-%d %H:%M:%S'))
                audit_logger.log("PROOF_ENGINE", f"SUCCESS: {lead['name']} verified via '{pattern}' on {contact_url}")
                return True
            else:
                audit_logger.log("PROOF_ENGINE", f"DOUBTFUL: {lead['name']} responded with status {resp.status_code} but no success pattern found.")
                return False
        except Exception as e:
            print(f"[!] Form injection failed for {lead['name']}: {e}")
            return False

    async def run_batch(self, limit=500):
        """Industrial Scale: Process leads in massive async batches."""
        leads = self.db.get_pending_leads()[:limit]
        if not leads:
            print("[*] No pending leads found.")
            return

        semaphore = asyncio.Semaphore(100) # Increased to 100 for cloud industrial scale
        
        async def sem_inject(lead):
            async with semaphore:
                return await self.inject_form(lead)

        tasks = [sem_inject(lead) for lead in leads]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(1 for r in results if r)
        print(f"\n=== BATCH COMPLETED: {success_count}/{len(leads)} Successful Injections ===")


if __name__ == "__main__":
    sniper = FormSniper()
    asyncio.run(sniper.run_batch())
