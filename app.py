
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# =======================
# Données temps réel via yfinance
# =======================
tickers = {
    "Ørsted": "ORSTED.CO",
    "Vestas": "VWS.CO",
    "Schneider Electric": "SU.PA",
    "Microsoft": "MSFT",
    "AXA": "CS.PA"
}

data = yf.download(list(tickers.values()), period="1d", interval="1d")["Close"].iloc[-1]
actions = pd.DataFrame({
    "Entreprise": list(tickers.keys()),
    "Ticker": list(tickers.values()),
    "Prix (€)": [round(p, 2) for p in data],
})
actions["Quantité"] = (10000 // actions["Prix (€)"]).astype(int)
actions["Investi (€)"] = actions["Quantité"] * actions["Prix (€)"]

# Obligations (valeur estimée à 100€)
obligations = pd.DataFrame({
    "Titre": [
        "OAT Verte 2039",
        "BEI CAB",
        "Banque Mondiale GB",
        "Apple Green Bond",
        "Iberdrola Green Bond"
    ],
    "Prix (€)": [100] * 5,
    "Quantité": [100] * 5
})
obligations["Investi (€)"] = obligations["Prix (€)"] * obligations["Quantité"]

# =======================
# Interface Streamlit
# =======================
st.set_page_config(page_title="Portefeuille ESG", layout="wide")
st.title("🌱 Portefeuille Durable (Actions + Obligations Vertes)")

# Résumé portefeuille
st.header("📊 Répartition du portefeuille")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Actions durables")
    st.dataframe(actions)
    total_actions = actions["Investi (€)"].sum()
    st.metric("Montant total en actions", f"{total_actions:,.2f} €")

with col2:
    st.subheader("Obligations vertes")
    st.dataframe(obligations)
    total_oblig = obligations["Investi (€)"].sum()
    st.metric("Montant total en obligations", f"{total_oblig:,.2f} €")

# Camembert
fig, ax = plt.subplots()
ax.pie([total_actions, total_oblig], labels=["Actions", "Obligations"], autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# =======================
# Fiches ESG (extraites du rapport)
# =======================
st.header("📌 Fiches ESG des actifs")
with st.expander("📈 Ørsted (énergie renouvelable)"):
    st.write("Best-in-class, notée AAA MSCI. Production éolienne offshore. Impact direct sur le climat.")

with st.expander("⚙️ Schneider Electric (industrie durable)"):
    st.write("Entreprise la plus durable 2025. Automatisation & efficacité énergétique. MSCI AAA.")

with st.expander("💻 Microsoft (technologie verte)"):
    st.write("Cloud 100% renouvelable d'ici 2025. Objectif 'Carbon Negative'. Inclusivité forte.")

with st.expander("🌍 OAT Verte France"):
    st.write("Obligation souveraine verte. Financement de projets publics (transports, bâtiments verts).")

with st.expander("🏛️ BEI / Banque Mondiale"):
    st.write("Obligations vertes d'institutions AAA. Financement global de projets verts dans les pays en développement.")

st.info("💡 Ce portefeuille est réparti à parts égales entre 5 actions best-in-class et 5 obligations vertes labellisées.")
