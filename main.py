import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import pytz
import os

# CONFIGURAZIONE
URL = "https://it.dreametech.com/products/collegamento-acqua-aqua-series?_pos=11&_sid=085e122f1&_ss=r"
EMAIL_SENDER = "lodovico.soliera@gmail.com"
EMAIL_RECEIVERS = ["lodovico.soliera@gmail.com", "l.soliera@gmail.com"]
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def check_availability():
    # Header per far sembrare la richiesta un browser reale
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://it.dreametech.com/"
    }
    
    rome_tz = pytz.timezone("Europe/Rome")
    now_str = datetime.now(rome_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    print(f"[{now_str}] Avvio controllo disponibilità...")
    
    try:
        # 1. Scarica la pagina
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        # 2. Analizza il testo
        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.get_text().lower()
        
        # 3. Verifica se il prodotto è ancora esaurito
        # Cerchiamo la parola "esaurito" nel testo della pagina
        if "esaurito" not in page_content:
            print("!!! PRODOTTO DISPONIBILE !!!")
            send_notification(now_str)
        else:
            print("Stato attuale: Ancora esaurito.")
            
    except Exception as e:
        print(f"Errore durante il controllo: {e}")

def send_notification(timestamp):
    if not GMAIL_PASSWORD:
        print("Errore: GMAIL_PASSWORD non configurata.")
        return

    msg = EmailMessage()
    msg.set_content(f"Il Kit Collegamento Acqua Dreame è TORNATO DISPONIBILE!\n\nAcquista subito qui: {URL}\n\nRilevato il: {timestamp} (Ora di Roma)")
    msg['Subject'] = f"DISPONIBILE: Kit Acqua Dreame - {timestamp}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(EMAIL_RECEIVERS)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, GMAIL_PASSWORD)
            server.send_message(msg)
        print("Email di notifica inviata con successo!")
    except Exception as e:
        print(f"Errore invio email: {e}")

if __name__ == "__main__":
    check_availability()
