import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import pytz

# Configurazione
EMAIL_SENDER = "lodovico.soliera@gmail.com"
EMAIL_RECEIVERS = ["lodovico.soliera@gmail.com", "l.soliera@gmail.com"]
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_test_email():
    rome_tz = pytz.timezone("Europe/Rome")
    now = datetime.now(rome_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    print(f"[{now}] Avvio invio email di test...")
    
    if not GMAIL_PASSWORD:
        print("ERRORE: GMAIL_PASSWORD non trovata nei Secrets!")
        return

    msg = EmailMessage()
    msg.set_content(f"TEST FUNZIONANTE!\n\nSe ricevi questa email, il tuo sistema è pronto.\n\nInviato il: {now}")
    msg['Subject'] = f"TEST Tracker Dreame - {now}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(EMAIL_RECEIVERS)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, GMAIL_PASSWORD)
            server.send_message(msg)
        print("EMAIL INVIATA CON SUCCESSO!")
    except Exception as e:
        print(f"ERRORE: {e}")

if __name__ == "__main__":
    send_test_email()
