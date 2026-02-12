import imaplib
import email
from email.header import decode_header
import logging

logger = logging.getLogger("mail_reader")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def fetch_unread_mails(imap_server, email_user, email_pass):
    """
    Récupère les mails non lus dans la boîte IMAP.
    Retourne une liste de tuples : (subject, body, from_addr)
    """
    mails = []
    try:
        logger.info("Connexion à la boîte IMAP...")
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        logger.info("Connexion IMAP réussie ✅")

        # Sélection de la boîte INBOX
        status, messages = mail.select("INBOX")
        logger.info(f"IMAP select status: {status}, nombre de messages: {messages[0].decode()}")
        if status != "OK":
            logger.error("Impossible de sélectionner la boîte INBOX.")
            return mails

        # Chercher les mails non lus
        status, response = mail.search(None, 'UNSEEN')
        logger.info(f"IMAP search status: {status}")
        if status != "OK":
            logger.error("Erreur lors de la recherche des mails non lus.")
            return mails

        mail_ids = response[0].split()
        logger.info(f"{len(mail_ids)} mail(s) non lu(s) trouvé(s).")

        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK":
                logger.warning(f"Impossible de récupérer le mail ID {mail_id.decode()}")
                continue

            msg = email.message_from_bytes(msg_data[0][1])

            # Sujet
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            # Expéditeur
            from_addr = msg.get("From")

            # Corps
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            mails.append((subject, body, from_addr))

        mail.logout()

    except imaplib.IMAP4.error as e:
        logger.error(f"Erreur lors de la récupération des mails : {e}")
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")

    return mails
