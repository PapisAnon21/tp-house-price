import streamlit as st

st.title("Calculatrice simple")

a = st.number_input("Entrer un nombre A", value=0)
b = st.number_input("Entrer un nombre B", value=0)

if st.button("Additionner"):
    st.write(f"Résultat : {a + b}")
