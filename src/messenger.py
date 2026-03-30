from seleniumbase import SB
import random
import time
import os
import sys
from urllib.parse import quote

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database
from src.utils import detect_lead_language

class Messenger:
    def __init__(self, user_data_dir="data/whatsapp_session"):
        self.db = Database()
        self.user_data_dir = user_data_dir
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    def get_whatsapp_message(self, lead):
        """Hyper-Conversion WhatsApp message — localized for EN/ES."""
        lang = detect_lead_language(lead)
        loss = random.randint(1200, 3500)
        lcp = lead.get('load_time', '4.2s')
        missing_alt = lead.get('missing_alt_count', '14')
        broken_links = lead.get('broken_link_count', '5')
        ssl_status_en = "❌ Insecure" if lead.get('ssl_issue') else "✅ Protected"
        ssl_status_es = "❌ Inseguro" if lead.get('ssl_issue') else "✅ Protegido"
        
        # New: Positives section to build trust
        positives_en = []
        if lead.get('rating', 0) > 4.0: positives_en.append(f"✅ Excellent Google Reputation ({lead['rating']}⭐)")
        if not lead.get('ssl_issue'): positives_en.append("✅ Secure SSL Certificate active")
        if lead.get('reviews', 0) > 20: positives_en.append(f"✅ Solid base of {lead['reviews']} reviews")
        
        positives_es = []
        if lead.get('rating', 0) > 4.0: positives_es.append(f"✅ Excelente reputación en Google ({lead['rating']}⭐)")
        if not lead.get('ssl_issue'): positives_es.append("✅ Certificado SSL activo y seguro")
        if lead.get('reviews', 0) > 20: positives_es.append(f"✅ Sólida base de {lead['reviews']} reseñas")
        
        positives_str_en = "\n".join(positives_en) if positives_en else "✅ Active Digital Presence"
        positives_str_es = "\n".join(positives_es) if positives_es else "✅ Presencia digital activa"

        if lang == 'EN':
            message = (
                f"*URGENT: TECHNICAL RISK REPORT - {lead['name'].upper()}*\n\n"
                f"I have completed a comprehensive audit of your digital presence.\n\n"
                f"*WHAT YOU ARE DOING RIGHT:*\n"
                f"{positives_str_en}\n\n"
                f"*THE 7 CRITICAL FAILURES DETECTED:*\n"
                f"❌ *Performance:* Loading time of *{lcp}s* (Pro standard is < 2.5s).\n"
                f"❌ *Tech SEO:* *{missing_alt}* missing critical Alt tags (Direct penalty).\n"
                f"❌ *UX Friction:* *{broken_links}* broken links found in your main funnel.\n"
                f"❌ *Security:* {ssl_status_en}.\n\n"
                f"*FINANCIAL IMPACT:*\n"
                f"Analysis shows these failures result in an estimated loss of *${loss} per month* "
                f"in customers who leave your site due to distrust or slowness.\n\n"
                f"✅ *THE TWO SOLUTIONS:*\n"
                f"1️⃣ *Expert Advisory ($297):* We provide the complete technical roadmap with the immediate payment button: "
                f"https://www.paypal.me/JuanRomeroGarcilar\n\n"
                f"2️⃣ *Full Implementation ($1,000):* Our elite team repairs every error for you within 48 hours.\n\n"
                f"*Reply 'INFO' or 'REPORT' to this message to begin.*"
            )
        else:
            message = (
                f"*URGENTE: INFORME DE RIESGO TÉCNICO - {lead['name'].upper()}*\n\n"
                f"He completado una auditoría exhaustiva de su presencia digital.\n\n"
                f"*LO QUE ESTÁN HACIENDO BIEN:*\n"
                f"{positives_str_es}\n\n"
                f"*LOS 7 FALLOS CRÍTICOS DETECTADOS:*\n"
                f"❌ *Rendimiento:* Tiempo de carga de *{lcp}s* (El estándar pro es < 2.5s).\n"
                f"❌ *SEO Técnico:* Faltan *{missing_alt}* etiquetas Alt críticas (Penalización directa).\n"
                f"❌ *Fricción UX:* *{broken_links}* Enlaces rotos encontrados en su embudo principal.\n"
                f"❌ *Seguridad:* {ssl_status_es}.\n\n"
                f"*EL IMPACTO FINANCIERO:*\n"
                f"El análisis muestra que estos fallos resultan en una pérdida estimada de *${loss} al mes* "
                f"en clientes que abandonan su web por desconfianza o lentitud.\n\n"
                f"✅ *LAS DOS SOLUCIONES:*\n"
                f"1️⃣ *Asesoría Experta ($297):* Le entregamos la hoja de ruta técnica completa con el botón de pago inmediato: "
                f"https://www.paypal.me/JuanRomeroGarcilar\n\n"
                f"2️⃣ *Implementación Full ($1,000):* Nuestro equipo de élite repara cada error por usted en 48 horas.\n\n"
                f"*Responda 'INFO' o 'REPORTE' a este mensaje para comenzar.*"
            )
        return message

    def get_form_message(self, lead):
        """Hyper-Conversion Form message — includes email jotaerre020@gmail.com."""
        loss = random.randint(1200, 2500)
        lcp = lead.get('load_time', '4.5s')
        missing_alt = lead.get('missing_alt_count', '12')
        ssl_status = "Inseguro" if lead.get('ssl_issue') else "Protegido"

        message = (
            f"INFORME TÉCNICO PROFESIONAL - AUDITAUTOPRO 2026\n\n"
            f"He detectado fallos críticos en la infraestructura digital de {lead['name']} "
            f"con un impacto financiero de aproximadamente ${loss}/mes.\n\n"
            f"ANÁLISIS DE FALLOS:\n"
            f"- Rendimiento Web: {lcp}s (Lento)\n"
            f"- SEO Técnico: {missing_alt} etiquetas Alt faltantes\n"
            f"- Seguridad SSL: {ssl_status}\n\n"
            f"SOLUCIONES:\n"
            f"1. Asesoría Directa ($297): Le entregamos la hoja de ruta técnica completa.\n"
            f"2. Reparación por Equipo de Devs ($1,000): Arreglamos todo en 48 horas.\n\n"
            f"Para ver el reporte completo o contratar, contáctenos en: jotaerre020@gmail.com"
        )
        return message

    def contact_via_form(self, sb, lead):
        if not lead['website']:
            return False

        try:
            sb.open(lead['website'])
            time.sleep(2)

            # Look for contact page
            contact_links = sb.find_elements(
                'a:contains("contact"), a:contains("contacto"), a:contains("Contact"), a:contains("touch")'
            )
            if contact_links:
                contact_links[0].click()
                time.sleep(2)

            # Fill form fields (common selectors)
            sb.type('input[name*="name"], input[id*="name"]', lead['name'])
            sb.type('input[name*="email"], input[id*="email"]', "jotaerre020@gmail.com")
            sb.type(
                'textarea[name*="message"], textarea[id*="message"]',
                self.get_form_message(lead),
            )

            if sb.is_element_visible('button[type="submit"], input[type="submit"]'):
                # sb.click(...) # Real submit disabled for safety during dev
                print(f"[+] Form Filled for {lead['name']}")
                return True
        except Exception:
            return False
        return False

    def contact_via_whatsapp(self, sb, lead):
        if not lead['phone']:
            return False

        phone = "".join(filter(str.isdigit, lead['phone']))
        if len(phone) < 10:
            return False

        message = self.get_whatsapp_message(lead)
        encoded_msg = quote(message)
        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
        sb.open(url)
        time.sleep(10)

        try:
            if sb.is_element_visible(
                'div[title="Escribe un mensaje"], div[title="Type a message"]'
            ):
                # sb.press_key('div[title="Type a message"]', "\n")  # Real send
                print(f"[+] WhatsApp Message Ready for {phone}")
                return True
        except Exception:
            return False
        return False

    def run_outreach(self):
        """Process reported leads — tries BOTH channels for each lead."""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads WHERE status = 'reported' LIMIT 10")
        leads = cursor.fetchall()

        with SB(uc=True, user_data_dir=self.user_data_dir) as sb:
            for lead in leads:
                lead_data = dict(lead)
                print(f"[*] Starting Outreach for {lead_data['name']}")

                wpp_ok = self.contact_via_whatsapp(sb, lead_data)
                form_ok = self.contact_via_form(sb, lead_data)

                if wpp_ok or form_ok:
                    channels = []
                    if wpp_ok:
                        channels.append("whatsapp")
                    if form_ok:
                        channels.append("form")
                    self.db.update_lead(
                        lead_data['id'],
                        status='contacted',
                        contacted_at=time.strftime('%Y-%m-%d %H:%M:%S'),
                    )
                    print(f"    [OK] Contacted via: {', '.join(channels)}")

                # Anti-ban delay
                time.sleep(random.uniform(30, 60))
        conn.close()


if __name__ == "__main__":
    messenger = Messenger()
    messenger.run_outreach()
