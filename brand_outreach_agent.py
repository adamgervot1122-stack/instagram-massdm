"""
Agent IA de prospection de marques lifestyle par email.
Utilise Gemini (gratuit) pour générer des emails personnalisés et les envoyer.
"""

import os
import json
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from typing import Optional


# ─── Configuration ────────────────────────────────────────────────────────────

@dataclass
class Config:
    # Gemini (gratuit)
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    # Ton profil (à remplir dans le .env)
    your_name: str = os.getenv("YOUR_NAME", "Ton Prénom")
    your_instagram: str = os.getenv("YOUR_INSTAGRAM", "@toncompte")
    your_niche: str = os.getenv("YOUR_NICHE", "lifestyle / mode / bien-être")
    your_followers: str = os.getenv("YOUR_FOLLOWERS", "10K")
    your_email: str = os.getenv("YOUR_EMAIL", "")

    # SMTP (Gmail recommandé)
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")  # Mot de passe d'application Gmail


# ─── Modèles de données ────────────────────────────────────────────────────────

@dataclass
class Brand:
    name: str
    email: str
    website: str = ""
    description: str = ""
    instagram: str = ""


# ─── Agent IA ────────────────────────────────────────────────────────────────

class BrandOutreachAgent:
    def __init__(self, config: Config):
        self.config = config
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_email(self, brand: Brand) -> dict:
        """Génère un email de prospection personnalisé pour une marque lifestyle."""

        prompt = f"""Tu es un expert en marketing d'influence et en prospection de marques lifestyle.

Génère un email de prospection professionnel, chaleureux et personnalisé pour contacter cette marque.

**Profil de l'influenceur/créateur :**
- Nom : {self.config.your_name}
- Instagram : {self.config.your_instagram}
- Niche : {self.config.your_niche}
- Audience : {self.config.your_followers} abonnés
- Email : {self.config.your_email}

**Marque à contacter :**
- Nom : {brand.name}
- Site web : {brand.website or "non renseigné"}
- Description : {brand.description or "marque lifestyle"}
- Instagram : {brand.instagram or "non renseigné"}

**Instructions pour l'email :**
1. Objet accrocheur et professionnel (max 60 caractères)
2. Introduction personnalisée qui montre que tu connais la marque
3. Présentation concise de ton profil et de ta valeur ajoutée
4. Proposition de collaboration claire (partenariat, code promo, ambassadeur...)
5. Call-to-action simple et direct
6. Signature professionnelle
7. Ton : chaleureux, professionnel, enthousiaste — pas générique

Réponds UNIQUEMENT en JSON avec ce format exact :
{{
  "subject": "Objet de l'email",
  "body": "Corps complet de l'email en texte avec des sauts de ligne \\n"
}}"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        # Nettoyer si le modèle ajoute des balises markdown
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip().rstrip("```").strip()

        return json.loads(text)

    def send_email(self, brand: Brand, subject: str, body: str, dry_run: bool = False) -> bool:
        """Envoie l'email via SMTP. Si dry_run=True, affiche seulement sans envoyer."""

        if dry_run:
            print(f"\n{'='*60}")
            print(f"[DRY RUN] Email pour : {brand.name} <{brand.email}>")
            print(f"Objet : {subject}")
            print(f"{'─'*60}")
            print(body)
            print(f"{'='*60}\n")
            return True

        if not self.config.smtp_user or not self.config.smtp_password:
            print(f"[ERREUR] SMTP non configuré. Ajoute SMTP_USER et SMTP_PASSWORD dans le .env")
            return False

        msg = MIMEMultipart("alternative")
        msg["From"] = f"{self.config.your_name} <{self.config.smtp_user}>"
        msg["To"] = brand.email
        msg["Subject"] = subject
        msg["Reply-To"] = self.config.your_email or self.config.smtp_user

        msg.attach(MIMEText(body, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.sendmail(self.config.smtp_user, brand.email, msg.as_string())
            print(f"[OK] Email envoyé à {brand.name} ({brand.email})")
            return True
        except Exception as e:
            print(f"[ERREUR] Envoi échoué pour {brand.name}: {e}")
            return False

    def prospect_brands(self, brands: list, dry_run: bool = True) -> dict:
        """Lance la prospection complète sur une liste de marques."""

        results = {"sent": [], "failed": [], "total": len(brands)}

        print(f"\n Démarrage de la prospection — {len(brands)} marque(s)")
        print(f"Mode : {'DRY RUN (simulation)' if dry_run else 'ENVOI RÉEL'}\n")

        for i, brand in enumerate(brands, 1):
            print(f"[{i}/{len(brands)}] Génération email pour {brand.name}...")

            try:
                email_data = self.generate_email(brand)
                subject = email_data["subject"]
                body = email_data["body"]

                success = self.send_email(brand, subject, body, dry_run=dry_run)

                if success:
                    results["sent"].append(brand.name)
                else:
                    results["failed"].append(brand.name)

            except Exception as e:
                print(f"[ERREUR] {brand.name}: {e}")
                results["failed"].append(brand.name)

        print(f"\nRésultats : {len(results['sent'])} envoyé(s), {len(results['failed'])} échoué(s)")
        return results


# ─── Exemple d'utilisation ────────────────────────────────────────────────────

def main():
    from dotenv import load_dotenv
    load_dotenv()

    config = Config()

    # Liste de marques lifestyle à prospecter
    brands = [
        Brand(
            name="Sézane",
            email="contact@sezane.com",
            website="https://www.sezane.com",
            description="Marque de mode française éco-responsable, vêtements féminins chic",
            instagram="@sezane"
        ),
        Brand(
            name="Asphalte",
            email="bonjour@asphalte.com",
            website="https://www.asphalte.com",
            description="Marque de mode masculine durable et intemporelle",
            instagram="@asphalte_paris"
        ),
        Brand(
            name="Moodjo",
            email="hello@moodjo.com",
            website="https://www.moodjo.com",
            description="Marque lifestyle bien-être et accessoires de méditation",
            instagram="@moodjo"
        ),
    ]

    agent = BrandOutreachAgent(config)

    # dry_run=True = simulation (affiche sans envoyer)
    # dry_run=False = envoi réel (nécessite SMTP configuré)
    agent.prospect_brands(brands, dry_run=True)


if __name__ == "__main__":
    main()
