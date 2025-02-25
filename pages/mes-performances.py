import streamlit as st
from menu import menu_with_redirect
from components.add_performance_modal import add_performance
import requests

STRAVA_API_URL = "https://www.strava.com/api/v3"
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

col1, col2 = st.columns([0.6, 0.4], gap="large",vertical_alignment="bottom")
with col1:
    st.title("Mes performances")
with col2:
    add_performance_button = st.button("Ajouter une performance", key="add_performance",icon=":material/add_circle:")

st.text("bonjour " + str(st.session_state.user.get("username")))
if add_performance_button:
    add_performance()


st.subheader("Overview")
st.write("Here is a quick overview of your performances:")
col_dist, col_duration, col_activities = st.columns(3)

with col_dist:
    st.metric("Total distance 🏃🏼", "100 km",border=True)

with col_duration:
    st.metric("Total time ⏱️", "10 h",border=True)

with col_activities:
    st.metric("Nombre d'activités 🔢", "10",border=True)

st.subheader("Dernières performances")
st.write(str(st.session_state.user))