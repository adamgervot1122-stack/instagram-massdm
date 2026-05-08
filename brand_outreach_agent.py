"""
Agent IA de prospection de marques lifestyle par email.
Utilise Gemini (gratuit) pour générer des emails personnalisés et les envoyer.
Utilise Google Places API (New) pour trouver automatiquement des boutiques/marques.
"""

import os
import json
import smtplib
import time
import requests
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

    # Google Places API
    google_places_api_key: str = os.getenv("GOOGLE_PLACES_API_KEY", "")

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


# ─── Google Places Finder ────────────────────────────────────────────────────

class PlacesFinder:
    """Trouve automatiquement des boutiques/marques via Google Places API (New)."""

    PLACES_URL = "https://places.googleapis.com/v1/places:searchText"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, max_results: int = 10) -> list:
        """
        Recherche des lieux/boutiques correspondant à la requête.
        Retourne une liste de Brand prête à prospecter.
        """
        if not self.api_key:
            print("[ERREUR] GOOGLE_PLACES_API_KEY manquante dans le .env")
            return []

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "places.displayName,places.websiteUri,places.formattedAddress,places.types,places.internationalPhoneNumber"
        }
        payload = {
            "textQuery": query,
            "pageSize": max_results,
            "languageCode": "fr"
        }

        try:
            response = requests.post(self.PLACES_URL, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"[ERREUR] Google Places API : {e}")
            return []

        brands = []
        for place in data.get("places", []):
            name = place.get("displayName", {}).get("text", "")
            website = place.get("websiteUri", "")
            address = place.get("formattedAddress", "")
            types = place.get("types", [])

            # Génère un email de contact probable depuis le site web
            email = self._guess_email(website)

            brand = Brand(
                name=name,
                email=email,
                website=website,
                description=f"{', '.join(types[:2])} — {address}",
                instagram=""
            )
            brands.append(brand)
            print(f"[Places] Trouvé : {name} | {website} | email estimé : {email}")

        return brands

    def _guess_email(self, website: str) -> str:
        """Génère une adresse email probable depuis le domaine du site."""
        if not website:
            return ""
        try:
            domain = website.replace("https://", "").replace("http://", "").split("/")[0]
            return f"contact@{domain}"
        except Exception:
            return ""


# ─── Agent IA ────────────────────────────────────────────────────────────────

class BrandOutreachAgent:
    def __init__(self, config: Config):
        self.config = config
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_email(self, brand: Brand) -> dict:
        """Génère un email de prospection personnalisé pour une marque lifestyle."""

        prompt = f"""Tu es un expert en prospection commerciale et personal branding.

Génère un email de prospection en suivant EXACTEMENT ce style et cette structure :

--- EXEMPLE DE STYLE À RESPECTER ---
Bonjour [Nom] 👋🏼

J'espère que vous allez bien !?

[Compliment sincère et précis sur ce qui inspire dans leur marque/activité — communication, ambiance, clientèle, valeurs...]

Je voulais savoir si vous cherchez des [type de collaboration] pour vous amener un maximum de [bénéfice concret] selon votre accord ?!

Merci d'avance !
À bientôt !

[Prénom]
--- FIN DE L'EXEMPLE ---

**Profil de l'expéditeur :**
- Nom : {self.config.your_name}
- Instagram : {self.config.your_instagram}
- Niche : {self.config.your_niche}
- Audience : {self.config.your_followers} abonnés
- Email : {self.config.your_email}

**Entreprise à contacter :**
- Nom : {brand.name}
- Site web : {brand.website or "non renseigné"}
- Description : {brand.description or "entreprise lifestyle"}
- Instagram : {brand.instagram or "non renseigné"}

**Règles strictes :**
1. Objet court et accrocheur (max 50 caractères)
2. Ton chaleureux, humain, direct — jamais corporate
3. Le compliment doit sembler sincère et spécifique à cette marque
4. Proposition claire en une seule phrase
5. Pas de blabla inutile — court et percutant
6. Terminer par le prénom uniquement ({self.config.your_name.split()[0]})

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
    agent = BrandOutreachAgent(config)

    # ── Option 1 : Recherche automatique via Google Places ──────────────────
    # Décommente et modifie la recherche selon ta niche
    # Exemples : "boutique streetwear Paris", "label house music France",
    #            "marque skincare naturelle", "boutique lifestyle Lyon"

    USE_PLACES = bool(config.google_places_api_key)

    if USE_PLACES:
        finder = PlacesFinder(config.google_places_api_key)
        print("[Places] Recherche automatique de boutiques...")
        brands = finder.search("boutique lifestyle mode Paris", max_results=10)
    else:
        # ── Option 2 : Liste manuelle ────────────────────────────────────────
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

    if not brands:
        print("[INFO] Aucune marque trouvée. Vérifie ta clé API ou ta liste manuelle.")
        return

    # dry_run=True = simulation (affiche sans envoyer)
    # dry_run=False = envoi réel (nécessite SMTP configuré)
    agent.prospect_brands(brands, dry_run=True)


if __name__ == "__main__":
    main()
