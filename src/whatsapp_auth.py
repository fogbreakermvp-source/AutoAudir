from seleniumbase import SB
import time
import os

def generate_session(user_data_dir="data/whatsapp_session"):
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        
    print("=== WhatsApp Sessions Generator 2026 ===")
    print(f"[*] Creando sesión en: {user_data_dir}")
    print("[!] INSTRUCCIONES:")
    print("1. Se abrirá un navegador.")
    print("2. ESCANEA EL CÓDIGO QR con tu teléfono.")
    print("3. Una vez que carguen tus chats, espera 15 segundos.")
    print("4. Cierra el navegador.")
    print("5. Sube esta carpeta 'data/whatsapp_session' a tu GitHub junto con el código.")
    
    with SB(uc=True, user_data_dir=user_data_dir) as sb:
        sb.open("https://web.whatsapp.com")
        # Keep open until user closes or 2 minutes pass
        time.sleep(120)
        
if __name__ == "__main__":
    generate_session()
