import bcrypt
from pymongo import MongoClient
import streamlit as st

class Authentication:
    def __init__(self):
        connection_string = st.secrets["mongodb"]["connection_string"]
        self.client = MongoClient(connection_string)
        self.db = self.client["auth"]
        self.collection = self.db['auth']

    def verify_password(self, username, password):
        user = self.collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user.get("password").encode('utf-8')):
            return True
        return False