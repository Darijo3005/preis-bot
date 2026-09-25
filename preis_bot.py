import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Preis-Bot",
    page_icon="🛒",
    layout="wide"
)

PRODUKTE = {
    "Nutella 450g": {
        "Kaufland": {"preis": 3.49, "alt_preis": 3.99, "gueltig_bis": "27.09.2025"},
        "Penny": {"preis": 3.29, "alt_preis": 3.79, "gueltig_bis": "27.09.2025"},
        "Rewe": {"preis": 3.99, "alt_preis": 3.99, "gueltig_bis": "27.09.2025"},
        "Netto": {"preis": 3.59, "alt_preis": 3.99, "gueltig_bis": "27.09.2025"},
        "Aldi": {"preis": 3.19, "alt_preis": 3.19, "gueltig_bis": "27.09.2025"},
        "Lidl": {"preis": 3.39, "alt_preis": 3.89, "gueltig_bis": "27.09.2025"},
    },
    "Kaffee (500g)": {
        "Kaufland": {"preis": 4.99, "alt_preis": 5.99, "gueltig_bis": "27.09.2025"},
        "Penny": {"preis": 4.49, "alt_preis": 5.49, "gueltig_bis": "27.09.2025"},
        "Rewe": {"preis": 5.29, "alt_preis": 5.29, "gueltig_bis": "27.09.2025"},
        "Netto": {"preis": 4.79, "alt_preis": 5.79, "gueltig_bis": "27.09.2025"},
        "Aldi": {"preis": 4.29, "alt_preis": 4.29, "gueltig_bis": "27.09.2025"},
        "Lidl": {"preis": 4.59, "alt_preis": 5.19, "gueltig_bis": "27.09.2025"},
    },
    "Waschmittel": {
        "Kaufland": {"preis": 7.99, "alt_preis": 9.99, "gueltig_bis": "27.09.2025"},
        "Penny": {"preis": 6.99, "alt_preis": 8.99, "gueltig_bis": "27.09.2025"},
        "Rewe": {"preis": 8.49, "alt_preis": 8.49, "gueltig_bis": "27.09.2025"},
        "Netto": {"preis": 7.49, "alt_preis": 9.49, "gueltig_bis": "27.09.2025"},
        "Aldi": {"preis": 6.49, "alt_preis": 6.49, "gueltig_bis": "27.09.2025"},
        "Lidl": {"preis": 6.79, "alt_preis": 8.79, "gueltig_bis": "27.09.2025"},
    },
    "Toilettenpapier": {
        "Kaufland": {"preis": 5.99, "alt_preis": 6.99, "gueltig_bis": "27.09.2025"},
        "Penny": {"preis": 5.49, "alt_preis": 6.49, "gueltig_bis": "27.09.2025"},
        "Rewe": {"preis": 6.29, "alt_preis": 6.29, "gueltig_bis": "27.09.2025"},
        "Netto": {"preis": 5.79, "alt_preis": 6.79, "gueltig_bis": "27.09.2025"},
        "Aldi": {"preis": 4.99, "alt_preis": 4.99, "gueltig_bis": "27.09.2025"},
        "Lidl": {"preis": 5.29, "alt_preis": 6.29, "gueltig_bis": "27.09.2025"},
    },
    "Milch (1L)": {
        "Kaufland": {"preis": 1.19, "alt_preis": 1.29, "gueltig_bis": "27.09.2025"},
        "Penny": {"preis": 1.09, "alt_preis": 1.19, "gueltig_bis": "27.09.2025"},
        "Rewe": {"preis": 1.29, "alt_preis": 1.29, "gueltig_bis": "27.09.2025"},
        "Netto": {"preis": 1.15, "alt_preis": 1.25, "gueltig_bis": "27.09.2025"},
        "Aldi": {"preis": 0.99, "alt_preis": 0.99, "gueltig_bis": "27.09.2025"},
        "Lidl": {"preis": 1.05, "alt_preis": 1.15, "gueltig_bis": "27.09.2025"},
    },
}

FARBEN = {
    "Kaufland": "#E30613",
    "Penny": "#CC0000",
    "Rewe": "#CC071E",
    "Netto": "#FFD500",
    "Aldi": "#00549F",
    "Lidl": "#0050AA",
}

st.markdown("""
    <style>
    .big-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #2E7D32;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .best-price-box {
        background-color: #E8F5E9;
        border: 3px solid #4CAF50;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
    }
    .best-price-label {
        font-size: 18px;
        color: #2E7D32;
        font-weight: bold;
    }
    .best-price-value {
        font-size: 42px;
        color: #1B5E20;
        font-weight: bold;
    }
    .store-card {
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🛒 Preis-Bot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Finde den besten Preis für deine Lieblingsprodukte!</p>', unsafe_allow_html=True)

st.markdown("### 🔍 Was möchtest du kaufen?")

produkt_liste = list(PRODUKTE.keys())
ausgewaehlt = st.selectbox(
    "Wähle ein Produkt aus der Liste:",
    ["-- Bitte wählen --"] + produkt_liste,
    label_visibility="collapsed"
)

if ausgewaehlt != "-- Bitte wählen --":
    daten = PRODUKTE[ausgewaehlt]
    
    preise_liste = [(laden, info["preis"]) for laden, info in daten.items()]
    preise_liste.sort(key=lambda x: x[1])
    
    bester_laden, bester_preis = preise_liste[0]
    
    st.markdown(f"""
        <div class="best-price-box">
            <p class="best-price-label">🏆 BESTER PREIS bei {bester_laden}</p>
            <p class="best-price-value">{bester_preis:.2f} €</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Alle Preise im Vergleich")
    
    for laden, preis in preise_liste:
        info = daten[laden]
        alt_preis = info["alt_preis"]
        gueltig = info["gueltig_bis"]
        farbe = FARBEN.get(laden, "#666666")
        
        if preis < alt_preis:
            trend = "🔻"
            trend_text = f"Reduziert von {alt_preis:.2f} €"
        elif preis > alt_preis:
            trend = "🔺"
            trend_text = "Preis gestiegen"
        else:
            trend = "➖"
            trend_text = "Regulärer Preis"
        
        st.markdown(f"""
            <div class="store-card" style="background-color: {farbe};">
                {laden}: {preis:.2f} € {trend} 
                <span style="font-size: 14px; opacity: 0.9;">
                    ({trend_text} · gültig bis {gueltig})
                </span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 **Hinweis:** Dies sind Beispieldaten. Echte Preise können abweichen.")

else:
    st.markdown("### 💡 Beliebte Produkte zum Ausprobieren:")
    cols = st.columns(len(produkt_liste))
    for i, produkt in enumerate(produkt_liste):
        with cols[i]:
            st.markdown(f"**{produkt}**")

st.markdown("---")
st.caption("🛒 Preis-Bot Prototyp · Beispieldaten · Stand: September 2025")
