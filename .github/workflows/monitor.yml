import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "8719288520")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PRODUCTS = [
    {"name": "🌸 CartePlus - Gardevoir", "url": "https://cartesplus.fr/produit/coffret-poster-premium-mega-gardevoir-me02-5/", "site": "cartesplus"},
    {"name": "🐾 CartePlus - Lucario", "url": "https://cartesplus.fr/produit/coffret-poster-premium-mega-lucario-me02-5/", "site": "cartesplus"},
    {"name": "🌸 Philibert - Gardevoir", "url": "https://www.philibertnet.com/fr/pokemon/171401-pokemon-collection-poster-premium-mega-evolution-heros-transcendants-mega-gardevoir-2100001310110.html", "site": "philibert"},
    {"name": "🐾 Philibert - Lucario", "url": "https://www.philibertnet.com/fr/pokemon/171402-pokemon-collection-poster-premium-mega-evolution-heros-transcendants-mega-lucario-2100001310103.html", "site": "philibert"},
    {"name": "🎴 Philibert - Premiers Partenaires", "url": "https://www.philibertnet.com/fr/pokemon/171406-pokemon-coffret-pokemon-collection-illustration-premiers-partenaires-serie-1-2100001310141.html", "site": "philibert"},
    {"name": "👑 King Jouet - Poster Gardevoir/Lucario", "url": "https://www.king-jouet.com/jeu-jouet/jeux-societes/cartes-a-collectionner/ref-1007742-coffret-pokemon-collection-poster-premium-heros-transcendants-mega-lucario-ex-ou-mega-gardevoir.htm", "site": "kingjouet"},
    {"name": "🎴 King Jouet - Premiers Partenaires", "url": "https://www.king-jouet.com/jeu-jouet/jeux-societes/cartes-a-collectionner/ref-1007722-coffret-pokemon-collection-illustration-premiers-partenaires-serie-1.htm", "site": "kingjouet"},
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print(f"Erreur Telegram : {e}")

def is_available_cartesplus(soup):
    btn = soup.find("button", {"name": "add-to-cart"})
    page_text = soup.get_text().lower()
    for kw in ["rupture de stock", "indisponible", "épuisé"]:
        if kw in page_text:
            return False
    return btn is not None and not btn.get("disabled")

def is_available_philibert(soup):
    page_text = soup.get_text().lower()
    for kw in ["rupture de stock", "indisponible", "épuisé"]:
        if kw in page_text:
            return False
    btn = soup.find("button", class_=lambda x: x and "add-to-cart" in x.lower())
    if btn:
        return True
    return soup.find("input", {"type": "submit", "name": "add"}) is not None

def is_available_kingjouet(soup):
    page_text = soup.get_text().lower()
    for kw in ["non dispo", "indisponible à la livraison", "rupture"]:
        if kw in page_text:
            return False
    for btn in soup.find_all("button"):
        if any(k in btn.get_text().lower() for k in ["ajouter", "commander", "précommander"]):
            if not btn.get("disabled"):
                return True
    return False

def check_product(product):
    try:
        r = requests.get(product["url"], headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return False
        soup = BeautifulSoup(r.text, "html.parser")
        if product["site"] == "cartesplus":
            return is_available_cartesplus(soup)
        elif product["site"] == "philibert":
            return is_available_philibert(soup)
        elif product["site"] == "kingjouet":
            return is_available_kingjouet(soup)
    except Exception as e:
        print(f"Erreur : {e}")
    return False

def main():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"🔍 Vérification à {now}")
    for product in PRODUCTS:
        available = check_product(product)
        print(f"{'✅' if available else '❌'} {product['name']}")
        if available:
            send_telegram(f"🚨 <b>DISPONIBLE !</b>\n\n{product['name']}\n\n🔗 <a href='{product['url']}'>Commande vite !</a>\n\n⏰ {now}")
        time.sleep(2)

if __name__ == "__main__":
    main()
