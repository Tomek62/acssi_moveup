import streamlit as st
import requests
import time
from components.subscribe_modal import subscribe


API_URL = "http://127.0.0.1:5000"
STRAVA_API_URL = "https://www.strava.com/api/v3"

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/mes-performances.py", label="Mes performances", icon="🎯")
    st.sidebar.page_link("pages/mon-classement.py", label="Mon classement", icon="🥇")
    st.sidebar.page_link("pages/challenges.py", label="Mes challenges", icon=":material/sports_score:")
    st.sidebar.page_link("pages/mon-profil.py", label="Mon profil", icon="👤")
    logout_button = st.sidebar.button("Logout", use_container_width=True, icon=":material/logout:")
    
    # Fonctionnalité de déconnexion
    if logout_button:
        st.session_state.token = None
        st.rerun()

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    username = st.sidebar.text_input(label="Username")
    password =st.sidebar.text_input(label="Password", type="password")
    auth_url = f"{API_URL}/strava/auth"
    button =st.sidebar.button("🔒 Connectez-vous",use_container_width=True)
    button_strava= f"""
    <div style="display: flex;margin-bottom: 10px;background-color: #FC5200;border: none; padding: 10px 20px;border-radius: 5px;">
        <a href="{auth_url}" style=" color: white;  width:100%; cursor: pointer; text-decoration: none; text-align: center;">
            Connectez-vous avec Strava
        </a>
    </div>
    """
    if st.sidebar.markdown(button_strava, unsafe_allow_html=True):
        query_params = st.query_params
        if "access_token" in query_params:
            print(query_params)
            st.session_state.token = query_params["access_token"]
            print(st.session_state.token)
            st.query_params = {}  # Clear the token from the URL
                # 2️⃣ Faire une requête pour récupérer les infos de l'utilisateur
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                response = requests.get(f"{API_URL}/get_user", headers=headers,json={"token": st.session_state.token})
                print(response)
                if response.status_code == 200:
                    st.session_state.user = response.json().get("user")
                    st.query_params.clear()
                    st.switch_page("pages/mes-performances.py")
            
                else:
                    st.sidebar.error("Impossible de récupérer les informations utilisateur.")
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Erreur de connexion au serveur : {e}")

            
    if button:
        try:
            response = requests.post(f"{API_URL}/login", json={"email": username, "password": password})
            
            if response.status_code == 401:
                st.sidebar.error("Email ou mot de passe invalides")
            elif response.status_code == 200:
                with st.sidebar:
                    with st.spinner("Connexion en cours..."):
                        time.sleep(2)
                st.sidebar.success("Connexion réussie")
                time.sleep(2)
                st.session_state.token = response.json().get("token")
                st.session_state.user = response.json().get("user")
                st.switch_page("pages/mes-performances.py")
            else:
                st.sidebar.error(f"Erreur inattendue ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as e:
            # Catch and display errors related to the HTTP request
            st.sidebar.error(f"Erreur de connexion au serveur : {e}")
        except Exception as e:
            # Catch any other unexpected exceptions
            st.sidebar.error(f"Une erreur inattendue s'est produite : {e}")

    if st.sidebar.button("💪🏼 S'inscrire",use_container_width=True):
        subscribe()

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