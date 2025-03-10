import time
import streamlit as st
import pandas as pd
from data.database import Database
from data.project import Project


##Style, and Authentication Template##
st.set_page_config(initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state or st.session_state["authenticated"] == False:
    st.error("Authentication required.")
    if st.button("Return to Login"):
        st.switch_page("app.py")
    st.stop()

##################################################

db = Database()


st.title("UPMS Dashboard")

      
if "new_project" not in st.session_state:
    st.session_state.new_project = False

if st.button("New Project"):
    st.session_state.new_project = not st.session_state.new_project

if 'new_project' in st.session_state and st.session_state.new_project:
    st.subheader("New Project Form")
    project_name = st.text_input("Project Name")
    project_customer = st.text_input("Project Customer")
    project_status = st.selectbox("Project Status", ["Open", "In Progress", "Completed"])

    if st.button("Submit Project"):
        new_project = Project(project_name, project_customer, project_status)
        if new_project.is_valid():
            db.insert_project(new_project)
            st.success("New project added successfully!")
            st.session_state.new_project = False
            time.sleep(1)
            st.rerun()

        else:
            st.error("Please ensure customer name and project name are greater than 3 characters, and is not named 'project'.")

else:
    if st.button("Generate Report"):
        st.switch_page("pages/report.py")

    if st.button("Search Projects"):
        st.switch_page("pages/search.py")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.clear()
        st.switch_page("app.py")



