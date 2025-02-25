import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:5000"

@st.dialog("Inscrivez-vous",width='large')
def subscribe():
    st.subheader("Plus que quelques étapes pour devenir le boss du sport 😎")
    email = st.text_input("Entrez votre email")
    username = st.text_input("Entrez votre nom d'utilisateur")
    password = st.text_input("Entrez votre Password", type="password")
    confirmed_password = st.text_input("Confirm Password", type="password")
    if not email or not password or not confirmed_password:
        st.warning("Veuillez remplir tous les champs")


    if st.button("Submit"):
        try:
            response = requests.post(f"{API_URL}/register", json={"email": email,"username":username, "password": password,"confirmed_password": confirmed_password})
            if response.status_code == 400:
                st.error(response.json().get("message"))
            elif response.status_code == 201:
                st.success(response.json().get("message"))
                time.sleep(2)
                st.session_state.token = response.json().get("access_token")


        except Exception as e:
            # Catch any other unexpected exceptions
            st.sidebar.error(f"Une erreur inattendue s'est produite : {e}")