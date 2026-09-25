import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# ============================================
# SEITEN-KONFIGURATION
# ============================================
st.set_page_config(
    page_title="🛒 Preis-Vergleich Bot",
    page_icon="🛒",
    layout="wide"
)

# ============================================
# CUSTOM CSS FÜR SCHÖNES DESIGN
# ============================================
st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .price-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0px;
    }
    .best-price {
        background-color: #d4edda;
        border: 3px solid #28a745;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SCRAPER FUNKTION FÜR MARKTGURU
# ============================================
def scrape_marktguru(suchbegriff):
    """
    Sucht Angebote auf Marktguru.de
    Gibt Liste von Dictionaries mit Angebots-Infos zurück
    """
    ergebnisse = []
    
    try:
        # Marktguru Such-URL
        url = f"https://www.marktguru.de/suche?q={suchbegriff}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Finde alle Angebots-Links
        angebote = soup.find_all('a', class_='js-offer-link-item')
        
        for angebot in angebote:
            try:
                # Link extrahieren
                link = angebot.get('href', '')
                if link and not link.startswith('http'):
                    link = f"https://www.marktguru.de{link}"
                
                # Store Name extrahieren (aus Link oder Attribut)
                store_name = "Unbekannt"
                if '/geschaefte/' in link:
                    store_name = link.split('/geschaefte/')[1].split('/')[0].capitalize()
                
                # Produkt-Name
                product_elem = angebot.find(class_='offer-title') or angebot.find('h3')
                product_name = product_elem.text.strip() if product_elem else "Unbekanntes Produkt"
                
                # Preise extrahieren
                price_elem = angebot.find(class_='offer-price') or angebot.find(class_='price')
                offer_price = price_elem.text.strip() if price_elem else "N/A"
                
                old_price_elem = angebot.find(class_='old-price')
                old_price = old_price_elem.text.strip() if old_price_elem else None
                
                # Bild-URL
                img_elem = angebot.find('img')
                image_url = img_elem.get('src', '') if img_elem else ''
                if image_url and not image_url.startswith('http'):
                    image_url = f"https://www.marktguru.de{image_url}"
                
                # Gültigkeitszeitraum
                validity_elem = angebot.find(class_='validity') or angebot.find(class_='date-range')
                validity = validity_elem.text.strip() if validity_elem else "Zeitraum unbekannt"
                
                ergebnisse.append({
                    'store': store_name,
                    'product': product_name,
                    'price': offer_price,
                    'old_price': old_price,
                    'validity': validity,
                    'link': link,
                    'image': image_url
                })
                
            except Exception as e:
                continue
        
        return ergebnisse
        
    except Exception as e:
        st.error(f"⚠️ Fehler beim Abrufen der Daten: {str(e)}")
        return []

# ============================================
# BEISPIEL-DATEN (FALLBACK falls Scraping fehlschlägt)
# ============================================
def get_sample_data(suchbegriff):
    """Fallback Beispiel-Daten"""
    sample_products = {
        "nutella": [
            {"store": "Lidl", "product": "Nutella 450g", "price": "2.99€", 
             "old_price": "3.49€", "validity": "01.-07.06.2025", 
             "link": "#", "image": ""},
            {"store": "Rewe", "product": "Nutella 450g", "price": "3.29€", 
             "old_price": "3.99€", "validity": "01.-07.06.2025", 
             "link": "#", "image": ""},
            {"store": "Kaufland", "product": "Nutella 450g", "price": "3.15€", 
             "old_price": None, "validity": "01.-07.06.2025", 
             "link": "#", "image": ""},
        ],
        "kaffee": [
            {"store": "Aldi", "product": "Jacobs Kaffee 500g", "price": "4.99€", 
             "old_price": "6.99€", "validity": "01.-07.06.2025", 
             "link": "#", "image": ""},
            {"store": "Penny", "product": "Jacobs Kaffee 500g", "price": "5.49€", 
             "old_price": None, "validity": "01.-07.06.2025", 
             "link": "#", "image": ""},
        ]
    }
    
    suchbegriff_lower = suchbegriff.lower()
    for key in sample_products:
        if key in suchbegriff_lower:
            return sample_products[key]
    
    return []

# ============================================
# PREIS-PARSER (String zu Float)
# ============================================
def parse_price(price_str):
    """Konvertiert '3.99€' zu 3.99"""
    try:
        cleaned = price_str.replace('€', '').replace(',', '.').strip()
        return float(cleaned)
    except:
        return float('inf')

# ============================================
# HAUPTPROGRAMM
# ============================================
def main():
    # HEADER
    st.title("🛒 Preis-Vergleich Bot")
    st.markdown("### 🔍 Finde die besten Angebote in deiner Nähe!")
    st.markdown("---")
    
    # SUCHFELD
    col1, col2 = st.columns([3, 1])
    
    with col1:
        suchbegriff = st.text_input(
            "🔎 Was möchtest du kaufen?",
            placeholder="z.B. Nutella, Kaffee, Waschmittel..."
        )
    
    with col2:
        st.write("")
        st.write("")
        suche_button = st.button("🔍 SUCHEN", type="primary")
    
    # PRODUKT-VORSCHLÄGE
    st.markdown("**💡 Beliebte Suchen:**")
    vorschlag_cols = st.columns(5)
    vorschlaege = ["Nutella", "Kaffee", "Waschmittel", "Toilettenpapier", "Milch"]
    
    for i, vorschlag in enumerate(vorschlaege):
        with vorschlag_cols[i]:
            if st.button(vorschlag, key=f"vorschlag_{i}"):
                suchbegriff = vorschlag
                suche_button = True
    
    st.markdown("---")
    
    # SUCHE AUSFÜHREN
    if suche_button and suchbegriff:
        with st.spinner(f"🔄 Suche nach '{suchbegriff}'..."):
            
            # Versuche echtes Scraping
            ergebnisse = scrape_marktguru(suchbegriff)
            
            # Falls Scraping keine Ergebnisse liefert, nutze Sample-Daten
            if not ergebnisse:
                st.info("ℹ️ Nutze Beispiel-Daten (Live-Scraping nicht verfügbar)")
                ergebnisse = get_sample_data(suchbegriff)
        
        if ergebnisse:
            # Sortiere nach Preis
            for r in ergebnisse:
                r['price_numeric'] = parse_price(r['price'])
            
            ergebnisse_sorted = sorted(ergebnisse, key=lambda x: x['price_numeric'])
            
            # BESTER PREIS ANZEIGEN
            bester = ergebnisse_sorted[0]
            
            st.markdown("## 🏆 BESTER PREIS GEFUNDEN!")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if bester['image']:
                    st.image(bester['image'], width=200)
                else:
                    st.markdown("### 📦")
            
            with col2:
                st.markdown(f"""
                <div class="best-price">
                    <h2>🏪 {bester['store']}</h2>
                    <h1 style="color: #28a745;">💰 {bester['price']}</h1>
                    <p>📦 {bester['product']}</p>
                    <p>📅 Gültig: {bester['validity']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if bester['link'] and bester['link'] != '#':
                    st.markdown(f"[🔗 Zum Angebot]({bester['link']})")
            
            st.markdown("---")
            
            # ALLE ANDEREN ANGEBOTE
            st.markdown("## 📊 Alle gefundenen Angebote")
            
            for i, angebot in enumerate(ergebnisse_sorted):
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 1])
                    
                    with col1:
                        st.markdown(f"### 🏪 {angebot['store']}")
                    
                    with col2:
                        st.markdown(f"**{angebot['product']}**")
                        if angebot['old_price']:
                            st.markdown(f"~~{angebot['old_price']}~~ → **{angebot['price']}**")
                        else:
                            st.markdown(f"**{angebot['price']}**")
                        st.caption(f"📅 {angebot['validity']}")
                    
                    with col3:
                        if angebot['link'] and angebot['link'] != '#':
                            st.markdown(f"[🔗 Angebot]({angebot['link']})")
                    
                    st.markdown("---")
        
        else:
            st.warning(f"❌ Keine Angebote für '{suchbegriff}' gefunden. Versuche einen anderen Suchbegriff!")
    
    elif suche_button and not suchbegriff:
        st.warning("⚠️ Bitte gib einen Suchbegriff ein!")
    
    # FOOTER
    st.markdown("---")
    st.markdown("### ℹ️ Hinweise")
    st.info("""
    - 🔄 Daten werden live von Marktguru.de abgerufen
    - 📅 Angebote sind zeitlich begrenzt gültig
    - 🔗 Klicke auf die Links für Details zum Angebot
    - ⚠️ Preise können sich ändern
    """)

if __name__ == "__main__":
    main()
