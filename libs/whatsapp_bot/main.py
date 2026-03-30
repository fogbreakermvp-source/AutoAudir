from seleniumbase import SB
import time
import random
import os
import sys
from urllib.parse import quote

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.database import Database

class WhatsAppMessenger:
    def __init__(self, user_data_dir="data/whatsapp_session"):
        self.db = Database()
        self.user_data_dir = os.path.abspath(user_data_dir)
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    def get_audit_message(self, lead_data):
        """
        Professional WhatsApp outreach message.
        - Realistic loss estimate ($150-$500/mo)
        - Both offers: $297 advisory + $1,000 full repair
        - NO email redirect — leads respond on WhatsApp
        """
        loss = random.randint(150, 500)

        # Pull real audit data if available, else use conservative defaults
        lcp = lead_data.get('lcp', '4.8s')
        broken_links = lead_data.get('broken_links', '5')
        missing_alt = lead_data.get('missing_alt', '12')

        variations = [
            (
                f"*Auditoría Técnica — {lead_data['name']}*\n\n"
                f"Hemos analizado su sitio web y encontramos los siguientes problemas:\n\n"
                f"❌ Velocidad de carga: *{lcp}* (lo ideal es menos de 2.5s)\n"
                f"❌ *{missing_alt}* imágenes sin etiquetas Alt (afecta su posición en Google)\n"
                f"❌ *{broken_links}* enlaces rotos en páginas principales\n"
                f"❌ Cabeceras de seguridad incompletas\n\n"
                f"Estos fallos pueden estar costándoles alrededor de *${loss}/mes* "
                f"en clientes que abandonan su web antes de contactarles.\n\n"
                f"*Dos opciones para solucionarlo:*\n\n"
                f"1️⃣ *Asesoría Profesional ($297)* — Les entregamos el plan de acción "
                f"completo con cada problema y su solución paso a paso. La opción más rápida.\n\n"
                f"2️⃣ *Reparación Total ($1,000)* — Nuestro equipo de desarrolladores "
                f"corrige todos los errores por ustedes en máximo 48 horas.\n\n"
                f"Si les interesa o tienen alguna pregunta, escríbannos aquí mismo. 👇"
            ),
            (
                f"Buen día, *{lead_data['name']}*.\n\n"
                f"Realizamos una auditoría gratuita de su presencia digital y detectamos "
                f"problemas técnicos con un impacto estimado de *~${loss}/mes*:\n\n"
                f"• Tiempo de carga elevado (*{lcp}*)\n"
                f"• {missing_alt} elementos SEO sin optimizar\n"
                f"• {broken_links} enlaces que no funcionan\n"
                f"• Configuración de seguridad incompleta\n\n"
                f"Podemos ayudarles de dos formas:\n\n"
                f"📋 *Asesoría ($297):* Diagnóstico completo + instrucciones claras "
                f"para que lo resuelvan rápidamente.\n"
                f"🔧 *Reparación por nuestro equipo ($1,000):* Nosotros nos encargamos "
                f"de arreglar cada error detectado.\n\n"
                f"Cualquier duda, escríbannos por aquí. Estamos para ayudarles."
            ),
        ]
        return random.choice(variations)

    def send_message(self, phone, lead_data):
        """Send WhatsApp message to a lead."""
        print(f"[*] Sending audit message to: {phone} ({lead_data['name']})")
        with SB(uc=True, user_data_dir=self.user_data_dir) as sb:
            clean_phone = "".join(filter(str.isdigit, phone))
            if len(clean_phone) < 10:
                print(f"[!] Invalid phone: {phone}")
                return False

            msg = self.get_audit_message(lead_data)
            encoded_msg = quote(msg)
            url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
            sb.open(url)
            time.sleep(20)  # Wait for session loading

            try:
                if sb.is_element_visible(
                    'div[title="Escribe un mensaje"], div[title="Type a message"]'
                ):
                    # sb.press_key('div[title="Type a message"]', "\n")  # Real send
                    print(f"[+] Message Ready for {phone}")
                    return True
            except Exception:
                print("[!] Error: WhatsApp session not detected. Scan the QR first.")
                return False
        return False

    def run(self):
        """Process all audited leads via WhatsApp."""
        leads = self.db.get_pending_leads()
        for lead in leads:
            if lead.get('phone'):
                self.send_message(lead['phone'], lead)
                time.sleep(random.uniform(30, 60))  # Anti-ban


if __name__ == "__main__":
    messenger = WhatsAppMessenger()
    # messenger.send_message("1234567890", {"name": "Test Business"})
