import requests
import pandas as pd
import streamlit as st

class ManageRecords:

    manage_type = [
        "Create Record", 
        "Update Record", 
        "Delete Record", 
    ]

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute

    def create(self):
        st.write("# Manage Records")
        # Always choose the first choice
        selected_tab = st.selectbox("Select to manage records", self.manage_type, index=0)

        # Define the content for each tab
        if selected_tab == "Create Record":
            st.write("# Create Records")
        elif selected_tab == "Update Record":
            st.write("# Update Records")
        elif selected_tab == "Delete Record":
            st.write("# Delete Records")

    def create_records(self):
        pass
    
    def update_records(self):
        pass
    
    def delete_records(self):
        pass

