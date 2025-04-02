import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# ======================
# Simulations de données ESG & Actifs durables
# ======================
actifs = pd.DataFrame({
    "Nom": [
        "Ørsted", "Vestas", "Schneider Electric", "Microsoft", "AXA",
        "Fonds ISR A", "ETF Green Equity", "Green Bond Apple", "Obligation OAT Verte", "Fonds ISR B"
    ],
    "Type": [
        "Action", "Action", "Action", "Action", "Action",
        "Fonds", "ETF", "Obligation", "Obligation", "Fonds"
    ],
    "Secteur": [
        "Énergie", "Énergie", "Industrie", "Technologie", "Finance",
        "Mixte", "Technologie", "Technologie", "Public", "Mixte"
    ],
    "Région": [
        "Europe", "Europe", "Europe", "Amérique", "Europe",
        "Global", "Global", "Amérique", "Europe", "Global"
    ],
    "Score ESG": [
        9.2, 8.5, 9.5, 8.7, 7.1,
        8.8, 8.9, 8.6, 8.3, 9.0
    ],
    "ISIN": [
        "ORSTED.CO", "VWS.CO", "SU.PA", "MSFT", "CS.PA",
        "ISR001", "ETF001", "OBL001", "OBL002", "ISR002"
    ]
})

# Récupération des prix pour les actions/ETF avec yfinance
tickers = actifs[actifs["Type"].isin(["Action", "ETF"])]
data = yf.download(list(tickers["ISIN"]), period="5y", interval="1d")["Close"]

# Simule un portefeuille égalitaire pour tous les actifs
actifs["Poids"] = 1 / len(actifs)

# ======================
# Interface utilisateur Streamlit
# ======================
st.set_page_config(page_title="Portefeuille ESG Avancé", layout="wide")
st.title("🌱 Portefeuille Durable (Actions, Fonds, Obligations, ETF)")

# Filtres ESG
st.sidebar.header("🔍 Filtres ESG")
types = st.sidebar.multiselect("Type d’actif", actifs["Type"].unique(), default=actifs["Type"].unique())
secteurs = st.sidebar.multiselect("Secteur", actifs["Secteur"].unique(), default=actifs["Secteur"].unique())
scores = st.sidebar.slider("Score ESG minimum", 0.0, 10.0, 7.0, 0.1)

actifs_filtrés = actifs[(actifs["Type"].isin(types)) &
                        (actifs["Secteur"].isin(secteurs)) &
                        (actifs["Score ESG"] >= scores)]

# ======================
# Affichage portefeuille filtré
# ======================
st.header("📋 Portefeuille filtré")
st.dataframe(actifs_filtrés)

# ======================
# Reporting ESG
# ======================
st.header("📊 Reporting ESG")

col1, col2, col3 = st.columns(3)

# Répartition par secteur
with col1:
    secteur_data = actifs_filtrés.groupby("Secteur")["Poids"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(secteur_data, labels=secteur_data.index, autopct="%1.1f%%")
    ax1.set_title("Répartition par secteur")
    st.pyplot(fig1)

# Score ESG moyen pondéré
with col2:
    esg_moyen = np.average(actifs_filtrés["Score ESG"], weights=actifs_filtrés["Poids"])
    st.metric("Score ESG moyen pondéré", f"{esg_moyen:.2f}/10")

# Répartition géographique
with col3:
    region_data = actifs_filtrés.groupby("Région")["Poids"].sum()
    fig2, ax2 = plt.subplots()
    ax2.bar(region_data.index, region_data.values)
    ax2.set_title("Répartition géographique")
    st.pyplot(fig2)

# ======================
# Performance passée (actions + ETF)
# ======================
st.header("📈 Performance passée des actifs sélectionnés")
if not data.empty:
    selected_isins = actifs_filtrés[actifs_filtrés["Type"].isin(["Action", "ETF"])]
    perf_data = data[selected_isins["ISIN"]].dropna()

    if not perf_data.empty:
        perf_norm = perf_data / perf_data.iloc[0] * 100
        st.line_chart(perf_norm)
    else:
        st.warning("Aucune donnée de performance disponible pour les actifs sélectionnés.")
else:
    st.warning("Les données de performance ne sont pas disponibles actuellement.")
