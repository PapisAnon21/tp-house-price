import streamlit as st
import pandas as pd
import requests

# ------------------------- Configuration -------------------------
st.set_page_config(page_title="Prédicteur de Prix Immobilier", layout="centered")
st.title("🏠 Prédicteur de Prix de Maison")

mode = st.radio("📌 Choisir le mode d'entrée :", ["Formulaire manuel", "Upload CSV"])

# ------------------------- Mode Manuel -------------------------
if mode == "Formulaire manuel":
    st.subheader("📝 Saisie manuelle des caractéristiques")

    # Champs numériques obligatoires
    gr_liv_area = st.number_input("GrLivArea (surface habitable au-dessus du sol)", min_value=0, value=1710)
    overall_qual = st.slider("OverallQual (qualité globale)", 1, 10, value=7)
    year_built = st.number_input("YearBuilt (année de construction)", min_value=1800, max_value=2025, value=2003)
    total_bsmt_sf = st.number_input("TotalBsmtSF (surface sous-sol)", min_value=0, value=856)
    garage_area = st.number_input("GarageArea (surface garage)", min_value=0, value=548)

    # Champs catégoriels obligatoires
    neighborhood = st.selectbox("Neighborhood (quartier)", [
        "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel", "Somerst", 
        "NWAmes", "OldTown", "BrkSide", "Sawyer", "NridgHt", "NAmes", 
        "SawyerW", "IDOTRR", "MeadowV", "Edwards", "Timber", "Gilbert", 
        "StoneBr", "ClearCr", "NPkVill", "Blmngtn", "BrDale", "SWISU", 
        "Blueste"
    ])
    ms_zoning = st.selectbox("MSZoning (zone résidentielle)", ["RL", "RM", "C (all)", "FV", "RH"])

    # Autres champs optionnels
    garage_cars = st.slider("GarageCars (places garage)", 0, 5, value=2)
    year_remod_add = st.number_input("YearRemodAdd (année rénovation)", min_value=1800, max_value=2025, value=2003)
    first_flr_sf = st.number_input("FirstFlrSF (surface RDC)", min_value=0, value=856)
    second_flr_sf = st.number_input("SecondFlrSF (surface étage)", min_value=0, value=854)
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

    # Préparation des données
    input_data = {
        "GrLivArea": gr_liv_area,
        "OverallQual": overall_qual,
        "OverallCond": 5,  # valeur par défaut
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
        "SaleCondition": sale_condition,
        "Neighborhood": neighborhood,
        "MSZoning": ms_zoning
    }

    # Validation des champs obligatoires
    required_values = [gr_liv_area, overall_qual, year_built, total_bsmt_sf, garage_area, neighborhood, ms_zoning]
    if st.button("🔍 Prédire le prix"):
        if any(v in [None, "", 0] for v in required_values):
            st.error("❗ Tous les champs obligatoires doivent être remplis.")
        else:
            try:
                response = requests.post("http://localhost:8000", json=input_data)
                if response.status_code == 200:
                    prediction = response.json().get("prediction", "Non défini")
                    st.success(f"💰 Prix estimé : **{prediction}**")
                else:
                    st.error(f"Erreur {response.status_code} : {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Impossible de se connecter à l'API (localhost:8000)")

# ------------------------- Mode CSV -------------------------
else:
    st.subheader("📂 Prédiction en lot par fichier CSV")

    uploaded_file = st.file_uploader("Uploader un fichier CSV avec les caractéristiques des maisons", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        # Vérifier colonnes obligatoires
        required_columns = [
            "GrLivArea", "OverallQual", "YearBuilt", "TotalBsmtSF", "GarageArea",
            "Neighborhood", "MSZoning"
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"❌ Colonnes manquantes dans le fichier CSV : {', '.join(missing)}")
        else:
            if st.button("🔄 Envoyer au serveur pour prédiction"):
                try:
                    payload = {"instances": df.to_dict(orient="records")}
                    response = requests.post("http://localhost:8000/batch", json=payload)

                    if response.status_code == 200:
                        preds = response.json().get("predictions", [])
                        df["PredictedPrice"] = preds
                        st.success("✅ Prédictions obtenues")
                        st.dataframe(df)
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button("💾 Télécharger les résultats", data=csv, file_name="predictions.csv", mime="text/csv")
                    else:
                        st.error(f"Erreur {response.status_code} : {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de se connecter à l'API (localhost:8000)")
