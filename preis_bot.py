import streamlit as st
import streamlit as st
from datetime import datetime

# Cache nur für 5 Minuten (statt 1 Stunde)
@st.cache_data(ttl=300)
def scrape_data(query):
    # ... dein Scraping-Code ...
    pass

# Manueller Refresh-Button
if st.button("🔄 Daten jetzt aktualisieren"):
    st.cache_data.clear()  # Löscht den Cache
    st.rerun()

# Zeige aktuellen Timestamp
st.caption(f"⏰ Zuletzt geupdatet: {datetime.now().strftime('%H:%M:%S')}")
import requests
from bs4 import BeautifulSoup
import re
import time

# ============================================
# 🎨 SEITEN-KONFIGURATION
# ============================================
st.set_page_config(
    page_title="🛒 Preis-Vergleich Bot",
    page_icon="🛒",
    layout="wide"
)

# ============================================
# 🎨 CUSTOM CSS für große, schöne Buttons
# ============================================
st.markdown("""
<style>
    .big-button {
        font-size: 24px !important;
        padding: 20px !important;
    }
    .price-card {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .best-price {
        background-color: #d4edda;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 8px solid #28a745;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .other-offer {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #ffc107;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# 🕷️ SCRAPER FUNKTIONEN
# ============================================

@st.cache_data(ttl=3600, show_spinner=False)  # Cache für 1 Stunde
def scrape_prospektangebote(product_name):
    """
    Scraper für prospektangebote.de
    Cached für 1 Stunde, damit wir die Seite nicht überlasten
    """
    url = f"https://www.prospektangebote.de/angebote/{product_name.lower()}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "de-DE,de;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e), "offers": []}
    
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all("div", class_="product")
    
    offers = []
    for container in product_containers:
        try:
            offer = extract_offer_data(container)
            if offer:
                offers.append(offer)
        except Exception:
            continue
    
    return {"error": None, "offers": offers}


def extract_offer_data(container):
    """Extrahiert alle Daten aus einem .product Container"""
    
    # Händlername + Logo
    store_img = container.find("div", class_="store-image")
    store_name = "Unbekannt"
    store_logo = None
    
    if store_img:
        img_tag = store_img.find("img")
        if img_tag:
            store_name = img_tag.get("alt", "Unbekannt")
            store_logo = img_tag.get("src", None)
    
    # Produktname
    name_tag = container.find("h3", class_="product__name")
    product_name = name_tag.get_text(strip=True) if name_tag else "Unbekannt"
    
    # Gültigkeit
    validity_tag = container.find("div", class_="product-date")
    validity = validity_tag.get_text(strip=True) if validity_tag else "Unbekannt"
    
    # Preis
    price_tag = container.find("div", class_="product__price-offer")
    price_text = price_tag.get_text(strip=True) if price_tag else None
    price = parse_price(price_text)
    
    # Alter Preis (falls vorhanden)
    old_price_tag = container.find("div", class_="product__price-old")
    old_price_text = old_price_tag.get_text(strip=True) if old_price_tag else None
    old_price = parse_price(old_price_text) if old_price_text else None
    
    # Link zum Angebot
    link_tag = container.find("a", class_="js-offer-link-item")
    offer_link = None
    if link_tag:
        href = link_tag.get("href", "")
        if href.startswith("/"):
            offer_link = f"https://www.prospektangebote.de{href}"
        else:
            offer_link = href
    
    # Produkt-Bild
    product_img_tag = container.find("div", class_="product__image")
    product_image = None
    if product_img_tag:
        img = product_img_tag.find("img")
        if img:
            product_image = img.get("src", None)
    
    if price is None or store_name == "Unbekannt":
        return None
    
    return {
        "store": store_name,
        "store_logo": store_logo,
        "product": product_name,
        "price": price,
        "old_price": old_price,
        "validity": validity,
        "link": offer_link,
        "product_image": product_image
    }


def parse_price(price_text):
    """Wandelt '€2,69' in float 2.69 um"""
    if not price_text:
        return None
    cleaned = re.sub(r'[^\d,\.]', '', price_text)
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None


# ============================================
# 🎯 HAUPT-APP
# ============================================

st.title("🛒 Preis-Vergleich Bot")
st.markdown("### Finde die günstigsten Angebote für deine Lieblingsprodukte! 💰")

st.markdown("---")

# 🔍 SUCHFELD
st.markdown("## 🔍 Was möchtest du suchen?")

# Vorschläge als Buttons
st.markdown("**Beliebte Produkte:**")
col1, col2, col3, col4, col5 = st.columns(5)

suggestions = {
    "🍫 Nutella": "nutella",
    "☕ Kaffee": "kaffee",
    "🧼 Waschmittel": "waschmittel",
    "🧻 Toilettenpapier": "toilettenpapier",
    "🥛 Milch": "milch"
}

selected_product = None

with col1:
    if st.button("🍫 Nutella", use_container_width=True):
        selected_product = "nutella"
with col2:
    if st.button("☕ Kaffee", use_container_width=True):
        selected_product = "kaffee"
with col3:
    if st.button("🧼 Waschmittel", use_container_width=True):
        selected_product = "waschmittel"
with col4:
    if st.button("🧻 Toilettenpapier", use_container_width=True):
        selected_product = "toilettenpapier"
with col5:
    if st.button("🥛 Milch", use_container_width=True):
        selected_product = "milch"

# Manuelles Suchfeld
search_input = st.text_input(
    "Oder gib deinen eigenen Suchbegriff ein:",
    placeholder="z.B. Butter, Joghurt, Zucker..."
)

if search_input:
    selected_product = search_input.strip().lower()

st.markdown("---")

# ============================================
# 🎯 SUCHERGEBNISSE ANZEIGEN
# ============================================

if selected_product:
    
    with st.spinner(f"🔍 Suche Angebote für '{selected_product}'..."):
        result = scrape_prospektangebote(selected_product)
    
    if result["error"]:
        st.error(f"❌ Fehler beim Abrufen der Daten: {result['error']}")
        st.info("💡 Tipp: Versuche es später erneut oder wähle einen anderen Suchbegriff.")
    
    elif not result["offers"]:
        st.warning(f"😕 Keine Angebote für '{selected_product}' gefunden.")
        st.info("💡 Tipp: Probiere einen anderen Suchbegriff, z.B. ohne Umlaute oder Sonderzeichen.")
    
    else:
        offers = result["offers"]
        
        # Sortiere nach Preis (günstigstes zuerst)
        sorted_offers = sorted(offers, key=lambda x: x["price"])
        best_offer = sorted_offers[0]
        
        st.success(f"✅ {len(offers)} Angebote gefunden!")
        
        # 🏆 BESTES ANGEBOT GROSS ANZEIGEN
        st.markdown("## 🏆 Bestes Angebot")
        
        with st.container():
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                if best_offer["store_logo"]:
                    st.image(best_offer["store_logo"], width=150)
            
            with col_info:
                st.markdown(f"""
                <div class="best-price">
                    <h2>🏪 {best_offer['store']}</h2>
                    <h1 style="color: #28a745;">💰 €{best_offer['price']:.2f}</h1>
                    <p style="font-size: 18px;">📅 Gültig: {best_offer['validity']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if best_offer["link"]:
                    st.link_button(
                        "🔗 Zum Angebot",
                        best_offer["link"],
                        use_container_width=True
                    )
        
        st.markdown("---")
        
        # 📊 ALLE ANDEREN ANGEBOTE
        if len(sorted_offers) > 1:
            st.markdown("## 📊 Weitere Angebote")
            
            for i, offer in enumerate(sorted_offers[1:], 1):
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if offer["store_logo"]:
                        st.image(offer["store_logo"], width=80)
                
                with col2:
                    st.markdown(f"""
                    <div class="other-offer">
                        <strong>🏪 {offer['store']}</strong><br>
                        💰 €{offer['price']:.2f}<br>
                        📅 {offer['validity']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if offer["link"]:
                        st.link_button("🔗 Ansehen", offer["link"], use_container_width=True)
        
        # 💾 Datenquelle
        st.markdown("---")
        st.caption("📊 Datenquelle: prospektangebote.de | 🔄 Daten werden stündlich aktualisiert")

else:
    st.info("👆 Wähle ein Produkt oben aus oder gib einen Suchbegriff ein, um zu starten!")

# ============================================
# ℹ️ FOOTER
# ============================================
st.markdown("---")
st.caption("🛒 Preis-Vergleich Bot | Made with ❤️ using Streamlit")
