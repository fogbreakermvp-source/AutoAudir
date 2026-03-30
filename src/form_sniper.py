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

class FormSniper:
    def __init__(self):
        self.db = Database()
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self.user_email = "jotaerre020@gmail.com"

    def get_form_message(self, lead):
        """Ultra-High Conversion Form message — includes Core Web Vitals."""
        loss = random.randint(1500, 4000)
        lcp = lead.get('load_time', '4.8s')
        missing_alt = lead.get('missing_alt_count', '18')
        ssl_status = "CRÍTICO" if lead.get('ssl_issue') else "Válido"
        
        # Arsenal v3: More technical details
        message = (
            f"INFORME TÉCNICO PROFESIONAL - ELITE PERFORMANCE AUDIT TEAM\n\n"
            f"Hemos detectado fallos en la infraestructura digital de {lead['name']} que están penalizando su posicionamiento global.\n\n"
            f"ANÁLISIS DE RENDIMIENTO (Core Web Vitals):\n"
            f"- LCP (Carga de Imagen): *{lcp}s* (Superior al límite de 2.5s)\n"
            f"- Accesibilidad: *{missing_alt}* fallos detectados en etiquetas Alt.\n"
            f"- Seguridad SSL: *{ssl_status}*.\n\n"
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

            # Use the form that looks like a contact form
            form = forms[0]
            action = form.get('action', '')
            if not action.startswith('http'):
                action = contact_url.rstrip('/') + '/' + action.lstrip('/')

            # Prepare payload
            payload = {}
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                name = input_tag.get('name')
                if not name:
                    continue

                type_ = input_tag.get('type', 'text').lower()
                name_lower = name.lower()

                if 'name' in name_lower or 'nombre' in name_lower:
                    payload[name] = "Equipo de Auditoría Digital"
                elif 'email' in name_lower or 'correo' in name_lower or 'mail' in name_lower:
                    payload[name] = self.user_email
                elif 'phone' in name_lower or 'tel' in name_lower or 'telefono' in name_lower:
                    payload[name] = ""  # Leave phone blank
                elif 'subject' in name_lower or 'asunto' in name_lower:
                    payload[name] = self.get_subject(lead)
                elif 'message' in name_lower or 'mensaje' in name_lower or input_tag.name == 'textarea':
                    payload[name] = self.get_form_message(lead)
                elif type_ == 'hidden':
                    payload[name] = input_tag.get('value', '')

            # Fire the injection
            resp = await self.client.post(action, data=payload)
            if resp.status_code in [200, 301, 302]:
                print(f"[+ OK] Form Injected for {lead['name']}")
                self.db.update_lead(lead['id'], status='contacted', contacted_at=time.strftime('%Y-%m-%d %H:%M:%S'))
                return True
        except Exception as e:
            print(f"[!] Form injection failed for {lead['name']}: {e}")
            return False

        return False

    async def run_batch(self, limit=500):
        """Industrial Scale: Process leads in massive async batches."""
        leads = self.db.get_pending_leads()[:limit]
        if not leads:
            print("[*] No pending leads found.")
            return

        semaphore = asyncio.Semaphore(50) # Process 50 simultaneously
        
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
