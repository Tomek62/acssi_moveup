import streamlit as st


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
    <div style="display: flex; justify-content: center; align-items: center;margin: 20px;">
        <button style="background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
            🔒 Connectez-vous
        </button>
    </div>
    """
    if st.sidebar.markdown(button_html, unsafe_allow_html=True) and username and password:
        st.session_state.token = "1234567890"
        st.rerun()

    if st.sidebar.button("Vous n'avez pas de compte? [Inscrivez-vous](https://www.acssi.com)"):
        subscribe()

@st.dialog("Inscrivez-vous",width='large')
def subscribe():
    username = st.text_input("Entrez votre Username")
    password = st.text_input("Entrez votre Password", type="password")
    confirmed_password = st.text_input("Confirm Password", type="password")
    if st.button("Submit") and password == confirmed_password:
        st.session_state.vote = {"username": username, "password": password}
        st.session_state.token = "1234567890"
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