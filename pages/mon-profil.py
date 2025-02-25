import streamlit as st
from menu import menu_with_redirect
import requests


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
st.title("Mon profil")


# API endpoint pour récupérer et mettre à jour les paramètres utilisateur
API_BASE_URL = "http://localhost:5000/api/users"  # Remplacez par l'URL de votre API



# Fonction pour mettre à jour les paramètres utilisateur
def update_user_settings(user_id, updated_data):
    response = requests.put(f"{API_BASE_URL}/{user_id}", json=updated_data)
    if response.status_code == 200:
        st.success("Paramètres mis à jour avec succès.")
        return response.json()
    else:
        st.error("Erreur lors de la mise à jour des paramètres.")
        return None

# Interface utilisateur avec Streamlit
st.title("Paramètres de l'utilisateur")

# Récupération des données utilisateur
user_data = st.session_state.user
# Ajouter une checkbox pour activer la modification
edit_mode = st.checkbox("Activer la modification")

# if edit_mode:
#     email = st.text_input("Email", user_data.get("email", ""), key="email_edit")
#     username = st.text_input("Nom d'utilisateur", user_data.get("username", ""), key="username_edit")
#     password = st.text_input("Mot de passe (laisser vide pour ne pas changer)", type="password", key="password_edit")
# else:
#     st.text_input("Email", user_data.get("email", ""), disabled=True)
#     st.text_input("Nom d'utilisateur", user_data.get("username", ""), disabled=True)
#     st.text_input("Mot de passe (laisser vide pour ne pas changer)", type="password", disabled=True)
if user_data:
    with st.form("user_settings_form"):
        st.subheader("Modifier vos informations")

        # Champs modifiables
        email = st.text_input("Email", user_data.get("email", ""), help="Votre adresse email")
        username = st.text_input("Nom d'utilisateur", user_data.get("username", ""))
        password = st.text_input("Mot de passe (laisser vide pour ne pas changer)", type="password")

        # Bouton pour soumettre les modifications
        submitted = st.form_submit_button("Mettre à jour")

        if submitted:
            updated_data = {
                "email": email,
                "username": username,
            }

            # Ajouter le mot de passe uniquement s'il a été modifié
            if password:
                updated_data["password"] = password


                updated_data["password"] = password

            # Appeler l'API pour mettre à jour les paramètres
            # update_user_settings(USER_ID, updated_data)

    st.subheader("Données actuelles")
    st.json(user_data)