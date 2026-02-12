import os
import logging
from main import generate_response
from mail_reader import fetch_unread_mails
from notifier import notify_telegram

# ------------------ Logging ------------------
logger = logging.getLogger("mail_agent")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Config mail depuis .env
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def process_mails():
    """
    Récupère les mails non lus et envoie des notifications Telegram
    """
    logger.info("Lancement du mail agent...")

    mails = fetch_unread_mails(IMAP_SERVER, EMAIL_USER, EMAIL_PASS)
    logger.info(f"{len(mails)} mail(s) non lu(s) trouvé(s).")

    for subject, body, from_addr in mails:
        subj_lower = subject.lower() if subject else ""

        try:
            if "candidature" in subj_lower:
                # Prompt pour LLM : classification
                prompt = f"""
Analyse ce mail de candidature et retourne uniquement REFUS, ACCEPTÉ ou AUTRE :

Sujet : {subject}
Corps :
{body[:4000]}
"""
                logger.info(f"Analyse du mail de candidature : {subject}")
                statut = generate_response(prompt).strip()
                entreprise = subject.split("-")[0].strip() if "-" in subject else subject
                message = f"{entreprise} : {statut}"
            else:
                # Notification simple pour tout autre mail
                message = f"Nouveau mail de : {from_addr}\nSujet : {subject}"
                logger.info(f"Mail non candidature détecté : {subject}")

            notify_telegram(message)
            logger.info(f"Notification envoyée : {message}")

        except Exception as e:
            logger.error(f"Erreur lors du traitement du mail '{subject}': {e}")

    logger.info("Fin du traitement des mails.")

if __name__ == "__main__":
    process_mails()
