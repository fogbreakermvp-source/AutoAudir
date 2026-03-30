from seleniumbase import SB
import os

def auth_session():
    user_data_dir = os.path.abspath("data/whatsapp_session")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        
    print(f"[*] Opening WhatsApp Web to persist session in: {user_data_dir}")
    print("[!] PLEASE SCAN THE QR CODE AND WAIT FOR CHATS TO LOAD.")
    print("[!] ONCE YOU ARE LOGGED IN, PRESS ENTER IN THIS TERMINAL TO SAVE AND CLOSE.")
    
    with SB(uc=True, user_data_dir=user_data_dir, headless=False) as sb:
        sb.open("https://web.whatsapp.com")
        input("\n>>> PRESS ENTER HERE AFTER SUCCESSFUL SCAN TO SAVE SESSION...")
        print("[+] Session saved. Closing browser.")

if __name__ == "__main__":
    auth_session()
