import streamlit as st
import pandas as pd
from data.database import Database
from data.project import Project
from data.milestones import Milestone

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

st.title("Search for Projects:")

if "search_submitted" not in st.session_state:
    st.session_state.search_submitted = False

if "new_milestone" not in st.session_state:
    st.session_state.new_milestone = False

with st.form(key="search_form"):
    project_name = st.text_input("Enter Project Name:")
    search_button = st.form_submit_button("Search")

    if search_button:
        st.session_state.search_submitted = True

if st.session_state.search_submitted:
    query = {"project_name": {"$regex": project_name, "$options": "i"}}
    results = db.fetch_projects(query)

    if results:
        df = pd.DataFrame(results)
        st.subheader("Search Results")
        for _, row in df.iterrows():
            with st.expander(f"Project: {row['project_name']}"):
                st.title(f"Project: {row['project_name']}")
                project_id = row["_id"]
                project_name = st.text_input("Name", row["project_name"], key=f"name_{project_id}")
                project_customer = st.text_input("Customer", row["project_customer"], key=f"cust_{project_id}")
                project_status = st.selectbox("Status", ["Open", "In Progress", "Completed"], index=["Open", "In Progress", "Completed"].index(row["project_status"]), key=f"status_{project_id}")
                updated_project = Project(project_name, project_customer, project_status, project_id=project_id)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update", key=f"update_{project_id}"):
                        # Validate fields
                        if not project_name:
                            st.warning("Please enter the project name.")
                        elif not project_customer:
                            st.warning("Please enter the project customer.")
                        elif not project_status:
                            st.warning("Please select the project status.")
                        else:
                            db.update_project(project_id, updated_project)
                            st.success("Project updated successfully!")
                
                with col2:
                    if st.button("Delete", key=f"delete_{project_id}"):
                        db.delete_project(project_id)
                        st.warning("Project deleted successfully!")
                        st.rerun()
                
                st.title("Milestones")
                milestones = db.fetch_project_milestones(project_id)
                col1, col2 = st.columns(2)
                with col1:
                    new_milestone_name = st.text_input("New Milestone Name", key=f"new_milestone_name_{project_id}_h1")
                with col2: 
                    st.text("")
                    if st.button("Add New Milestone", key=f"new_milestone_{project_id}"):
                        if new_milestone_name:
                            milestone = Milestone(new_milestone_name, "Open")
                            if not milestone.contains_num():
                                milestones.append(milestone.to_dict())
                                db.update_milestones(project_id, milestones)
                                st.success("New milestone added successfully!")
                                st.rerun()
                            else:
                                st.error("Milestone name cannot contain numbers.")
   
                milestone_selection = st.selectbox("Select Milestone", [m.get("milestone_name") for m in milestones], index=len(milestones)-1, placeholder="Select Milestone", key=f"milestone_selection_{project_id}")
                if milestone_selection:
                    selected_milestone = next((m for m in milestones if m.get("milestone_name") == milestone_selection), None)
                    if selected_milestone:
                        with st.form(key=f"milestone_form_{project_id}"):
                            milestone_name = st.text_input("Milestone Name", selected_milestone["milestone_name"])
                            milestone_status = st.selectbox("Milestone Status", ["Open", "In Progress", "Completed"], index=["Open", "In Progress", "Completed"].index(selected_milestone["milestone_status"]))
                            col1, col2 = st.columns(2)
                            with col1:
                                submit_milestone = st.form_submit_button("Update Milestone")
                                if submit_milestone:
                                    selected_milestone["milestone_name"] = milestone_name
                                    selected_milestone["milestone_status"] = milestone_status
                                    db.update_milestones(project_id, milestones)
                                    st.success("Milestone updated successfully!")
                                    milestone_selection = None
                                    st.rerun()  
                            with col2:
                                delete_milestone = st.form_submit_button("Delete Milestone")
                                if delete_milestone:
                                    milestones.remove(selected_milestone)
                                    db.update_milestones(project_id, milestones)
                                    st.warning("Milestone deleted successfully!")
                                    milestone_selection = None
                                    st.rerun()

if st.button("Clear Search"):
    st.session_state.search_submitted = False
    st.rerun()

if st.button("Back to Dashboard"):
    st.switch_page("pages/landing.py")