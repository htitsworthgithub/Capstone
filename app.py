import streamlit as st
from data.authentication import Authentication

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state.authenticated:
    st.title("Ultimate Project Management System (UPMS)!!!")
    
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        authentication = Authentication()
        if authentication.verify_password(username, password):
            st.session_state.authenticated = True
            st.switch_page("pages/landing.py")
        else:
            st.error("Invalid username or password.")
else:
    st.switch_page("pages/landing.py")
