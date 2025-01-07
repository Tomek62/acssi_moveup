import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/mon-classement.py", label="My ranking")
    st.sidebar.page_link("pages/mes-performances.py", label="My performances")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    username = st.sidebar.text_input(label="Username")
    password =st.sidebar.text_input(label="Password", type="password")
    button_html = """
    <div style="display: flex; justify-content: center; align-items: center;margin: 20px; ">
        <button style="background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
            🔒 Connectez-vous
        </button>
    </div>
    """
    if st.sidebar.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"email": username, "password": password})
        st.session_state.token = response.json().get("access_token")
        st.rerun()

    if st.sidebar.button("Vous n'avez pas de compte? [Inscrivez-vous](https://www.acssi.com)"):
        subscribe()

@st.dialog("Inscrivez-vous",width='large')
def subscribe():
    email = st.text_input("Entrez votre email")
    password = st.text_input("Entrez votre Password", type="password")
    confirmed_password = st.text_input("Confirm Password", type="password")
    if not email or not password or not confirmed_password:
        st.warning("Veuillez remplir tous les champs")
    if not "@" in email:
        st.warning("Veuillez entrer une adresse email valide")
    if not password == confirmed_password:
        st.warning("Les mots de passe ne correspondent pas")

    if st.button("Submit"):
        response = requests.post(f"{API_URL}/register", json={"email": email, "password": password})
        st.write(response.json())
        if response.status_code == 201:
            st.session_state.token = response.json().get("access_token")
            st.rerun()

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    st.sidebar.image("public/acssi.png", use_container_width=True)
    if "token" not in st.session_state or st.session_state.token is None:
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "token" not in st.session_state or st.session_state.token is None:
        st.switch_page("app.py")
    menu()