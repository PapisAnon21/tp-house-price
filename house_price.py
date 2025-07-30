import streamlit as st
import requests
import json

st.set_page_config(page_title="Prédicteur de Prix de Maison", layout="centered")
st.title("🏠 Prédicteur de Prix Immobilier")

st.markdown("Veuillez remplir les caractéristiques de la maison ci-dessous :")

# --- Champs numériques ---
gr_liv_area = st.number_input("GrLivArea (surface habitable)", value=1710)
overall_qual = st.slider("OverallQual (qualité globale)", 1, 10, value=7)
overall_cond = st.slider("OverallCond (état global)", 1, 10, value=5)
year_built = st.number_input("YearBuilt (année de construction)", value=2003)
year_remod_add = st.number_input("YearRemodAdd (année rénovation)", value=2003)
total_bsmt_sf = st.number_input("TotalBsmtSF (surface sous-sol)", value=856)
first_flr_sf = st.number_input("FirstFlrSF (surface RDC)", value=856)
second_flr_sf = st.number_input("SecondFlrSF (surface étage)", value=854)
garage_area = st.number_input("GarageArea (surface garage)", value=548)
garage_cars = st.slider("GarageCars (places garage)", 0, 5, value=2)


# --- Champs catégoriels ---
heating_qc = st.selectbox("HeatingQC (qualité chauffage)", ["Ex", "Gd", "TA", "Fa", "Po"])
central_air = st.selectbox("CentralAir (climatisation)", ["Y", "N"])
kitchen_qual = st.selectbox("KitchenQual (qualité cuisine)", ["Ex", "Gd", "TA", "Fa"])
functional = st.selectbox("Functional (fonctionnalité)", ["Typ", "Min1", "Min2", "Mod", "Maj1", "Maj2", "Sev", "Sal"])
fireplace_qu = st.selectbox("FireplaceQu (qualité cheminée)", ["Ex", "Gd", "TA", "Fa", "Po", None])
garage_type = st.selectbox("GarageType", ["Attchd", "Detchd", "BuiltIn", "Basment", "CarPort", "2Types", None])
garage_finish = st.selectbox("GarageFinish", ["Fin", "RFn", "Unf", None])
garage_qual = st.selectbox("GarageQual", ["Ex", "Gd", "TA", "Fa", "Po", None])
paved_drive = st.selectbox("PavedDrive (allée pavée)", ["Y", "N", "P"])
sale_condition = st.selectbox("SaleCondition", ["Normal", "Abnorml", "AdjLand", "Alloca", "Family", "Partial"])

# --- Regroupement des données ---
data = {
    "GrLivArea": gr_liv_area,
    "OverallQual": overall_qual,
    "OverallCond": overall_cond,
    "YearBuilt": year_built,
    "YearRemodAdd": year_remod_add,
    "TotalBsmtSF": total_bsmt_sf,
    "FirstFlrSF": first_flr_sf,
    "SecondFlrSF": second_flr_sf,
    "GarageArea": garage_area,
    "GarageCars": garage_cars,
    "HeatingQC": heating_qc,
    "CentralAir": central_air,
    "KitchenQual": kitchen_qual,
    "Functional": functional,
    "FireplaceQu": fireplace_qu,
    "GarageType": garage_type,
    "GarageFinish": garage_finish,
    "GarageQual": garage_qual,
    "PavedDrive": paved_drive,
    "SaleCondition": sale_condition
}

# --- Envoi vers le backend ---
if st.button("🔍 Prédire le prix"):
    try:
        response = requests.post("http://localhost:8000", json=data)
        if response.status_code == 200:
            prediction = response.json().get("prediction", "Valeur non retournée")
            st.success(f"💰 Prix estimé : **{prediction}**")
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Erreur : impossible de se connecter à l'API (localhost:8000)")