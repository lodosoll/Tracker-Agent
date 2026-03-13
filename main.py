import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import pytz
import os
import sys

# Configurazione
URL = "https://it.dreametech.com/products/collegamento-acqua-aqua-series?_pos=11&_sid=085e122f1&_ss=r"
EMAIL_SENDER = "lodovico.soliera@gmail.com"
EMAIL_RECEIVERS = ["lodovico.soliera@gmail.com", "l.soliera@gmail.com"]
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def check_availability():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://it.dreametech.com/"
    }
    
    print(f"[{get_now_rome()}] Controllo disponibilità...")
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo il testo nel corpo della pagina o in elementi specifici
        # Tipicamente Shopify usa un pulsante con testo "Esaurito" o simili.
        page_text = soup.get_text().lower()
        
        # Condizione: Se "esaurito" non è presente, il prodotto potrebbe essere disponibile.
        # Supporta sia "Esaurito" che "[Esaurito]"
        if "esaurito" not in page_text:
            print("!!! PRODOTTO DISPONIBILE !!!")
            send_notification()
        else:
            print("Stato attuale: Ancora esaurito.")
            
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete/timeout: {e}")
    except Exception as e:
        print(f"Errore imprevisto: {e}")

def get_now_rome():
    rome_tz = pytz.timezone("Europe/Rome")
    return datetime.now(rome_tz).strftime("%d/%m/%Y %H:%M:%S")

def send_notification():
    if not GMAIL_PASSWORD:
        print("ERRORE: GMAIL_PASSWORD non impostata nei Secrets/Variabili d'ambiente.")
        return

    now = get_now_rome()
    
    msg = EmailMessage()
    msg.set_content(f"Il prodotto Dreame è tornato disponibile!\n\nVerifica qui: {URL}\n\nRilevato il: {now} (Fuso orario Roma)")
    msg['Subject'] = f"DISPONIBILE: Kit Collegamento Acqua Dreame - {now}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(EMAIL_RECEIVERS)

    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, GMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email di notifica inviata con successo a {EMAIL_RECEIVERS}")
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")

if __name__ == "__main__":
    if not GMAIL_PASSWORD and len(sys.argv) == 1:
        print("Avviso: GMAIL_PASSWORD non trovata. Lo script funzionerà solo in modalità log.")
    check_availability()
