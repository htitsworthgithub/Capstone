from pymongo import MongoClient
import streamlit as st

class Database:
    def __init__(self):
        connection_string = st.secrets["mongodb"]["connection_string"]
        self.client = MongoClient(connection_string)
        self.db = self.client["test"]
        self.collection = self.db["projects"]

    def insert_project(self, project):
        self.collection.insert_one(project.__dict__)

    def update_project(self, project_id, updated_project):
        self.collection.update_one({"_id": project_id}, {"$set": updated_project.__dict__})

    def delete_project(self, project_id):
        self.collection.delete_one({"_id": project_id})

    def fetch_projects(self, query):
        return list(self.collection.find(query).sort("_id", -1))
    
    def fetch_project_milestones(self, project_id):
        project = self.collection.find_one({"_id": project_id}, {"project_milestones": 1})
        return project.get("project_milestones", []) if project else []
    
    def update_milestones(self, project_id, milestones):
        self.collection.update_one({"_id": project_id}, {"$set": {"project_milestones": milestones}})