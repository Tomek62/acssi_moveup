import streamlit as st
import requests
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:5000"

@st.dialog("Ajoutez une performance",width='large')
def add_performance():
    name = st.text_input("Nom de l'activité")
    type = st.selectbox("Type d'activité", ["Course à pied", "Vélo", "Marche", "Natation","Autre"])
    if type == "Autre":
        type = st.text_input("Précisez le type d'activité")
    start_time = st.date_input("Date de l'activité")
    duration = st.time_input("Durée de l'activité",step=60)
    distance = st.number_input("Distance parcourue (km)", min_value=0.0)
    elevation_gain = st.number_input("Dénivelé positif (m)", min_value=0.0)
    average_speed = st.number_input("Vitesse moyenne (km/h)", min_value=0.0)
    max_speed = st.number_input("Vitesse maximale (km/h)", min_value=0.0)
    calories = st.number_input("Calories brûlées", min_value=0)
    user_id = st.session_state.user.get("user_id")
    created_at = datetime.now()
    updated_at = datetime.now()
    if st.button("Ajouter"):
        try:
        # Convert duration from time object to timedelta
            duration_timedelta = timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
        
        # Prepare payload
            payload = {
            "name": name,
            "type": type,
            "start_time": start_time.isoformat(),  # Convert date to string
            "duration": str(duration_timedelta),  # Send duration as a string
            "distance": distance,
            "elevation_gain": elevation_gain,
            "average_speed": average_speed,
            "max_speed": max_speed,
            "calories": calories,
            "user_id": user_id,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
            }

        # Make API request
            response = requests.post(f"{API_URL}/add_performance", json=payload, headers={"Authorization": f"Bearer {st.session_state.token}"})
            st.write(response)
            if response.status_code == 400:
                st.error(response.json().get("message"))
            elif response.status_code == 201:
                st.success(response.json().get("message"))
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {e}")
