"""
Email Prospector - Outil de prospection marques/influenceurs par email
Auteur: Claude
Usage: python email_prospector.py [--test] [--ai]
  --test  : envoie uniquement à toi-même pour vérifier le rendu
  --ai    : active la personnalisation IA (coûte des crédits)
"""

import csv
import json
import smtplib
import time
import os
import sys
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("prospection.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# --- Couleurs terminal ---
class C:
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BLUE   = "\033[96m"
    RESET  = "\033[0m"


def load_config(path="email_config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_brands(path="brands.csv"):
    brands = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("email", "").strip():
                brands.append(row)
    return brands


# ──────────────────────────────────────────────
# TEMPLATE EMAIL (mode rapide, 0 crédit IA)
# ──────────────────────────────────────────────
EMAIL_TEMPLATE_TEXT = """\
Bonjour {contact_name},

Je me permets de vous contacter car je suis un(e) créateur(trice) de contenu spécialisé(e) dans le {your_niche} avec une communauté engagée de {your_followers} abonnés sur Instagram ({your_instagram}).

J'admire sincèrement le travail de {name} et je pense qu'une collaboration entre nous pourrait apporter une belle visibilité authentique à votre marque auprès de mon audience.

Je serais ravi(e) de discuter d'un partenariat adapté à vos objectifs : placement de produit, code promo exclusif, contenu sponsorisé...

Seriez-vous disponible pour en discuter cette semaine ?

Cordialement,
{your_name}
Instagram : {your_instagram}
"""

EMAIL_TEMPLATE_HTML = """\
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <p>Bonjour <strong>{contact_name}</strong>,</p>

  <p>Je me permets de vous contacter car je suis un(e) créateur(trice) de contenu spécialisé(e) dans le <strong>{your_niche}</strong> avec une communauté engagée de <strong>{your_followers}</strong> abonnés sur Instagram (<strong>{your_instagram}</strong>).</p>

  <p>J'admire sincèrement le travail de <strong>{name}</strong> et je pense qu'une collaboration entre nous pourrait apporter une belle visibilité authentique à votre marque auprès de mon audience.</p>

  <p>Je serais ravi(e) de discuter d'un partenariat adapté à vos objectifs :<br>
  &nbsp;&nbsp;• Placement de produit<br>
  &nbsp;&nbsp;• Code promo exclusif<br>
  &nbsp;&nbsp;• Contenu sponsorisé</p>

  <p>Seriez-vous disponible pour en discuter cette semaine ?</p>

  <br>
  <p>Cordialement,<br>
  <strong>{your_name}</strong><br>
  Instagram : <strong>{your_instagram}</strong></p>

  <hr style="border:none;border-top:1px solid #eee;margin-top:30px;">
  <p style="font-size:11px;color:#999;">
    Vous recevez cet email car vous êtes référencé comme contact partenariat.<br>
    Pour ne plus recevoir nos propositions, répondez simplement "STOP".
  </p>
</body>
</html>
"""


def render_template(template: str, brand: dict, cfg: dict) -> str:
    campaign = cfg["campaign"]
    return template.format(
        name=brand.get("name", ""),
        contact_name=brand.get("contact_name", "l'équipe"),
        niche=brand.get("niche", ""),
        website=brand.get("website", ""),
        your_name=campaign["your_name"],
        your_instagram=campaign["your_instagram"],
        your_niche=campaign["your_niche"],
        your_followers=campaign["your_followers"],
    )


# ──────────────────────────────────────────────
# PERSONNALISATION IA (optionnelle, use_ai=True)
# Appelle Claude UNE FOIS par marque pour
# personnaliser l'email — coûte des crédits
# ──────────────────────────────────────────────
def personalize_with_ai(brand: dict, base_text: str, api_key: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # modèle le moins cher
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": (
                    f"Réécris cet email de prospection en le personnalisant légèrement "
                    f"pour la marque '{brand['name']}' qui opère dans le secteur '{brand['niche']}'. "
                    f"Garde la même structure et longueur. Ne change que 2-3 phrases pour coller "
                    f"au secteur. Réponds uniquement avec l'email réécrit, rien d'autre.\n\n"
                    f"EMAIL:\n{base_text}"
                )
            }]
        )
        return message.content[0].text
    except Exception as e:
        log.warning(f"IA indisponible, utilisation du template standard: {e}")
        return base_text


# ──────────────────────────────────────────────
# ENVOI EMAIL
# ──────────────────────────────────────────────
def send_email(smtp, sender_cfg: dict, to_email: str, subject: str, text_body: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{sender_cfg['name']} <{sender_cfg['email']}>"
    msg["To"]      = to_email

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html",  "utf-8"))

    smtp.sendmail(sender_cfg["email"], to_email, msg.as_string())


def connect_smtp(sender_cfg: dict):
    server = smtplib.SMTP(sender_cfg["smtp_host"], sender_cfg["smtp_port"])
    server.ehlo()
    server.starttls()
    server.login(sender_cfg["email"], sender_cfg["smtp_password"])
    return server


# ──────────────────────────────────────────────
# TRACKER (évite d'envoyer 2x au même email)
# ──────────────────────────────────────────────
SENT_LOG = "sent_emails.txt"

def load_sent() -> set:
    if not Path(SENT_LOG).exists():
        return set()
    return set(Path(SENT_LOG).read_text(encoding="utf-8").splitlines())

def mark_sent(email: str):
    with open(SENT_LOG, "a", encoding="utf-8") as f:
        f.write(email + "\n")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    test_mode  = "--test" in sys.argv
    use_ai     = "--ai"   in sys.argv

    print(f"""{C.GREEN}
  ███████╗███╗   ███╗ █████╗ ██╗██╗
  ██╔════╝████╗ ████║██╔══██╗██║██║
  █████╗  ██╔████╔██║███████║██║██║
  ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║
  ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗
  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
  PROSPECTEUR EMAIL - by Claude
  Mode: {"TEST" if test_mode else "PRODUCTION"} | IA: {"ON (Haiku)" if use_ai else "OFF (template)"}
{C.RESET}""")

    cfg    = load_config()
    brands = load_brands()
    sent   = load_sent()
    campaign = cfg["campaign"]
    sender   = cfg["sender"]

    if test_mode:
        # En mode test, envoie à toi-même avec les données de la 1ère marque
        brands = [brands[0]] if brands else []
        for b in brands:
            b["email"] = sender["email"]
        log.info(f"[TEST] Envoi test à {sender['email']}")

    daily_count = 0
    daily_limit = campaign["daily_limit"]

    log.info(f"Chargement de {len(brands)} marques")

    try:
        smtp = connect_smtp(sender)
        log.info(f"{C.GREEN}Connecté au serveur SMTP{C.RESET}")
    except Exception as e:
        log.error(f"Impossible de se connecter au SMTP: {e}")
        log.error("Vérifiez email_config.json et votre mot de passe d'application Gmail")
        sys.exit(1)

    for i, brand in enumerate(brands, 1):
        to_email = brand["email"].strip()

        # Vérifications
        if to_email in sent and not test_mode:
            log.info(f"[{i}/{len(brands)}] {C.YELLOW}DÉJÀ ENVOYÉ{C.RESET} → {to_email}")
            continue

        if daily_count >= daily_limit:
            log.warning(f"Limite journalière atteinte ({daily_limit}). Arrêt.")
            break

        # Génération du contenu
        subject   = campaign["subject"].format(**brand)
        text_body = render_template(EMAIL_TEMPLATE_TEXT, brand, cfg)
        html_body = render_template(EMAIL_TEMPLATE_HTML, brand, cfg)

        if use_ai and cfg["template"]["use_ai_personalization"]:
            api_key   = cfg["template"]["anthropic_api_key"]
            text_body = personalize_with_ai(brand, text_body, api_key)
            html_body = render_template(EMAIL_TEMPLATE_HTML, brand, cfg)  # HTML reste propre

        # Envoi
        try:
            send_email(smtp, sender, to_email, subject, text_body, html_body)
            mark_sent(to_email)
            daily_count += 1
            log.info(f"[{i}/{len(brands)}] {C.GREEN}ENVOYÉ{C.RESET} → {to_email} ({brand['name']})")
        except smtplib.SMTPException as e:
            log.error(f"[{i}/{len(brands)}] {C.RED}ECHEC{C.RESET} → {to_email} : {e}")
            # Reconnexion si coupure
            try:
                smtp = connect_smtp(sender)
            except Exception:
                pass

        # Délai anti-spam entre chaque email
        if i < len(brands) and not test_mode:
            delay = campaign["delay_between_emails_seconds"]
            log.info(f"Attente {delay}s avant prochain envoi...")
            time.sleep(delay)

    smtp.quit()

    print(f"""
{C.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RÉSULTAT
  Emails envoyés : {daily_count}/{len(brands)}
  Log complet    : prospection.log
  Déjà envoyés   : sent_emails.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}
""")


if __name__ == "__main__":
    main()
