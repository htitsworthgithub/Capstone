from datetime import datetime
import pandas as pd
import streamlit as st

from data.database import Database
from data.milestones import Milestone, Milestones

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

projects = db.fetch_projects({})
customers = list(set([project['project_customer'] for project in projects]))

st.title("Customer Project Status Report")
selected_customer = st.selectbox("Select Customer:", customers)

if st.button("Generate Report"):
    query = {"project_customer": selected_customer}
    results = db.fetch_projects(query)

    if results:
        st.subheader(f"Projects for {selected_customer}")
        data = []
        for project in results:
            dbmilestones = db.fetch_project_milestones(project["_id"])
            milestones = Milestones()
            for milestone in dbmilestones:
                milestone = Milestone(milestone["milestone_name"], milestone["milestone_status"])
                milestones.add_milestone(milestone.out_string())
            data.append({
                "Project Name": project["project_name"],
                "Status": project["project_status"],
                "Milestones": milestones.value()
            })
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write(f"No projects found for {selected_customer}")
    
    now = datetime.now()

    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    st.text(f"Report Generated at {formatted_date_time}")

if st.button("Back to Dashboard"):
    st.switch_page("pages/landing.py")  # Redirect to another page
