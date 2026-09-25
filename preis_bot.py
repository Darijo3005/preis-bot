
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🛒 Preis-Bot", page_icon="🛒", layout="wide")

sample_data = {
    "Nutella 450g": {
        "Kaufland": {"preis": 3.49, "alt_preis": 3.99, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.kaufland.de/angebote"},
        "Penny": {"preis": 3.99, "alt_preis": 3.99, "trend": "➖", "gueltig_bis": "Sa., 11.11.", "link": "https://www.penny.de/angebote"},
        "Rewe": {"preis": 3.79, "alt_preis": 3.69, "trend": "🔺", "gueltig_bis": "So., 12.11.", "link": "https://www.rewe.de/angebote"},
        "Netto": {"preis": 3.59, "alt_preis": 3.79, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.netto-online.de/angebote"},
        "Aldi": {"preis": 3.89, "alt_preis": 3.89, "trend": "➖", "gueltig_bis": "Mi., 15.11.", "link": "https://www.aldi-sued.de/angebote"},
        "Lidl": {"preis": 3.65, "alt_preis": 3.75, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.lidl.de/angebote"},
    },
    "Jacobs Krönung Kaffee 500g": {
        "Kaufland": {"preis": 5.99, "alt_preis": 6.49, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.kaufland.de/angebote"},
        "Penny": {"preis": 6.29, "alt_preis": 6.29, "trend": "➖", "gueltig_bis": "Sa., 11.11.", "link": "https://www.penny.de/angebote"},
        "Rewe": {"preis": 5.79, "alt_preis": 5.99, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.rewe.de/angebote"},
        "Netto": {"preis": 6.49, "alt_preis": 6.29, "trend": "🔺", "gueltig_bis": "Sa., 11.11.", "link": "https://www.netto-online.de/angebote"},
        "Aldi": {"preis": 5.49, "alt_preis": 5.49, "trend": "➖", "gueltig_bis": "Mi., 15.11.", "link": "https://www.aldi-sued.de/angebote"},
        "Lidl": {"preis": 5.69, "alt_preis": 5.89, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.lidl.de/angebote"},
    },
    "Persil Waschmittel": {
        "Kaufland": {"preis": 8.99, "alt_preis": 9.49, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.kaufland.de/angebote"},
        "Penny": {"preis": 9.49, "alt_preis": 9.49, "trend": "➖", "gueltig_bis": "Sa., 11.11.", "link": "https://www.penny.de/angebote"},
        "Rewe": {"preis": 8.79, "alt_preis": 8.99, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.rewe.de/angebote"},
        "Netto": {"preis": 9.29, "alt_preis": 8.99, "trend": "🔺", "gueltig_bis": "Sa., 11.11.", "link": "https://www.netto-online.de/angebote"},
        "Aldi": {"preis": 7.99, "alt_preis": 7.99, "trend": "➖", "gueltig_bis": "Mi., 15.11.", "link": "https://www.aldi-sued.de/angebote"},
        "Lidl": {"preis": 8.49, "alt_preis": 8.69, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.lidl.de/angebote"},
    },
    "Toilettenpapier (8 Rollen)": {
        "Kaufland": {"preis": 4.49, "alt_preis": 4.99, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.kaufland.de/angebote"},
        "Penny": {"preis": 4.99, "alt_preis": 4.99, "trend": "➖", "gueltig_bis": "Sa., 11.11.", "link": "https://www.penny.de/angebote"},
        "Rewe": {"preis": 4.79, "alt_preis": 4.69, "trend": "🔺", "gueltig_bis": "So., 12.11.", "link": "https://www.rewe.de/angebote"},
        "Netto": {"preis": 4.59, "alt_preis": 4.79, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.netto-online.de/angebote"},
        "Aldi": {"preis": 3.99, "alt_preis": 3.99, "trend": "➖", "gueltig_bis": "Mi., 15.11.", "link": "https://www.aldi-sued.de/angebote"},
        "Lidl": {"preis": 4.29, "alt_preis": 4.49, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.lidl.de/angebote"},
    },
    "Milch 1L": {
        "Kaufland": {"preis": 1.19, "alt_preis": 1.29, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.kaufland.de/angebote"},
        "Penny": {"preis": 1.29, "alt_preis": 1.29, "trend": "➖", "gueltig_bis": "Sa., 11.11.", "link": "https://www.penny.de/angebote"},
        "Rewe": {"preis": 1.15, "alt_preis": 1.19, "trend": "🔻", "gueltig_bis": "So., 12.11.", "link": "https://www.rewe.de/angebote"},
        "Netto": {"preis": 1.25, "alt_preis": 1.15, "trend": "🔺", "gueltig_bis": "Sa., 11.11.", "link": "https://www.netto-online.de/angebote"},
        "Aldi": {"preis": 1.09, "alt_preis": 1.09, "trend": "➖", "gueltig_bis": "Mi., 15.11.", "link": "https://www.aldi-sued.de/angebote"},
        "Lidl": {"preis": 1.19, "alt_preis": 1.25, "trend": "🔻", "gueltig_bis": "Sa., 11.11.", "link": "https://www.lidl.de/angebote"},
    },
}

RETAILER_COLORS = {
    "Kaufland": "#E30613", "Penny": "#CC0000", "Rewe": "#CC071E",
    "Netto": "#FFD500", "Aldi": "#00549F", "Lidl": "#0050AA",
}

st.title("🛒 Preis-Bot – Finde den besten Preis!")
st.markdown("### Vergleiche Preise verschiedener Supermärkte auf einen Blick 😊")
st.markdown("## 🔍 Was möchtest du kaufen?")

col1, col2 = st.columns([3, 1])
with col1:
    suche = st.text_input("Produktname eingeben:", placeholder="z. B. Nutella, Kaffee, Milch...")

with col2:
    st.markdown("**💡 Beispiele:**")
    for produkt in sample_data.keys():
        if st.button(produkt, key=produkt):
            suche = produkt

if suche:
    gefunden = None
    for produkt in sample_data.keys():
        if suche.lower() in produkt.lower():
            gefunden = produkt
            break

    if gefunden:
        daten = sample_data[gefunden]
        preise = {h: v["preis"] for h, v in daten.items()}
        bester_haendler = min(preise, key=preise.get)
        bester_preis = preise[bester_haendler]

        st.markdown("---")
        st.markdown(f"## 📦 Ergebnisse für: **{gefunden}**")

        st.markdown(
            f"""
            <div style="background-color:#DFF6DD; padding:25px; border-radius:15px; border: 3px solid #4CAF50;">
                <h2 style="color:#2E7D32; margin:0;">🏆 Bester Preis!</h2>
                <h1 style="color:#1B5E20; margin:10px 0;">{bester_preis:.2f} € bei {bester_haendler}</h1>
                <p style="font-size:18px;">📅 Gültig bis: {daten[bester_haendler]['gueltig_bis']}</p>
                <a href="{daten[bester_haendler]['link']}" target="_blank">
                    <button style="background-color:#4CAF50; color:white; padding:12px 24px; border:none; border-radius:8px; font-size:16px; cursor:pointer;">
                        🔗 Zum Angebot
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📊 Alle Angebote im Vergleich:")

        sortierte_haendler = sorted(daten.items(), key=lambda x: x[1]["preis"])
        cols = st.columns(3)
        for idx, (haendler, info) in enumerate(sortierte_haendler):
            farbe = RETAILER_COLORS.get(haendler, "#CCCCCC")
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div style="background-color:white; border-left: 8px solid {farbe}; 
                                padding:15px; border-radius:10px; margin-bottom:15px; 
                                box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h3 style="margin:0;">{haendler} {info['trend']}</h3>
                        <h2 style="color:{farbe}; margin:5px 0;">{info['preis']:.2f} €</h2>
                        <p style="color:gray; font-size:14px;">
                            Vorher: {info['alt_preis']:.2f} €<br>
                            📅 Gültig bis: {info['gueltig_bis']}
                        </p>
                        <a href="{info['link']}" target="_blank">🔗 Zum Angebot</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown("### 📈 Preis-Trend Erklärung:")
        st.markdown("🔻 = Preis gesunken | 🔺 = Preis gestiegen | ➖ = Preis gleich geblieben")
    else:
        st.warning(f"😕 Kein Produkt gefunden für '{suche}'. Probier es mit: Nutella, Kaffee, Waschmittel, Toilettenpapier oder Milch!")
else:
    st.info("👆 Gib oben ein Produkt ein oder klicke auf einen der Beispiel-Buttons!")

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:12px;">
        ℹ️ Dies ist eine Demo-Version mit Beispieldaten. 
        Echte Preise können abweichen. Bitte prüfe die Angebote direkt beim Händler.
    </div>
    """,
    unsafe_allow_html=True
</details>
