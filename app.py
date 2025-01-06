import streamlit as st
from menu import menu

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


# Selectbox to choose role
st.title("Bienvenue sur ACSSI MOVEUP :arrow_up:")
# Introduction to the application
st.header("Challenge Sportif ACSSI")
st.write("""
Bienvenue sur l'application Challenge Sportif ACSSI! 
Notre objectif est de vous encourager à rester actif et en bonne santé grâce à des défis sportifs hebdomadaires et mensuels.
Choisissez votre rôle pour commencer et découvrez les défis qui vous attendent!
""")
menu() # Render the dynamic menu!