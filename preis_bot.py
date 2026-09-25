import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# ============================================
# 🕷️ SCRAPER-FUNKTION (Live von Marktguru)
# ============================================

@st.cache_data(ttl=3600)  # Cached für 1 Stunde, schont den Server!
def scrape_marktguru(suchbegriff):
    """
    Sucht live auf Marktguru nach einem Produkt
    """
    url = f"https://www.marktguru.de/suche?q={suchbegriff}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        angebote = []
        
        # Alle Angebots-Links finden
        offer_links = soup.find_all('a', class_='js-offer-link-item')
        
        for link in offer_links:
            try:
                # Store-Name extrahieren
                store = link.find('div', class_='store-name')
                store_name = store.text.strip() if store else "Unbekannt"
                
                # Produktname
                title = link.find('div', class_='offer-title')
                produkt_name = title.text.strip() if title else "Unbekannt"
                
                # Preis
                price = link.find('div', class_='price')
                preis = price.text.strip() if price else "N/A"
                
                # Alter Preis (durchgestrichen)
                old_price = link.find('div', class_='old-price')
                alter_preis = old_price.text.strip() if old_price else None
                
                # Gültigkeit
                validity = link.find('div', class_='validity')
                gueltigkeit = validity.text.strip() if validity else "N/A"
                
                # Link zum Angebot
                href = link.get('href', '')
                voller_link = f"https://www.marktguru.de{href}"
                
                # Bild
                img = link.find('img')
                bild_url = img.get('src', '') if img else ''
                
                angebote.append({
                    'store': store_name,
                    'produkt': produkt_name,
                    'preis': preis,
                    'alter_preis': alter_preis,
                    'gueltigkeit': gueltigkeit,
                    'link': voller_link,
                    'bild': bild_url
                })
                
            except Exception as e:
                continue  # Überspringe fehlerhafte Einträge
        
        return angebote
        
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Fehler beim Abrufen: {e}")
        return []


# ============================================
# 🎨 STREAMLIT OBERFLÄCHE
# ============================================

st.title("🛒 Preis-Bot LIVE")
st.markdown("### 🔴 Live-Daten von Marktguru")

suchbegriff = st.text_input("🔍 Was suchst du?", placeholder="z.B. Nutella")

if st.button("🚀 Jetzt suchen!", type="primary"):
    if suchbegriff:
        with st.spinner("🔄 Suche läuft... (kann 5-10 Sek dauern)"):
            ergebnisse = scrape_marktguru(suchbegriff)
        
        if ergebnisse:
            st.success(f"✅ {len(ergebnisse)} Angebote gefunden!")
            
            for angebot in ergebnisse:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if angebot['bild']:
                            st.image(angebot['bild'], width=100)
                    
                    with col2:
                        st.markdown(f"**🏪 {angebot['store']}**")
                        st.markdown(f"📦 {angebot['produkt']}")
                        st.markdown(f"💰 **{angebot['preis']}**")
                        if angebot['alter_preis']:
                            st.markdown(f"~~{angebot['alter_preis']}~~")
                        st.markdown(f"📅 {angebot['gueltigkeit']}")
                        st.markdown(f"[🔗 Zum Angebot]({angebot['link']})")
                    
                    st.divider()
        else:
            st.warning("😕 Keine Angebote gefunden. Versuch's mit einem anderen Suchbegriff!")
    else:
        st.warning("⚠️ Bitte gib einen Suchbegriff ein!")
