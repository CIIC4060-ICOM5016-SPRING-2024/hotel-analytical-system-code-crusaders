import requests
import pandas as pd
import streamlit as st

class ManageRecords:

    admin_manage = [
        "Create Record", 
        "Update Record", 
        "Delete Record", 
        "Create Roomunavailable", 
        "Create Reservation", 
    ]

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute

    def create_as_admin(self):
        st.write("# Manage Records")
        # Always choose the first choice
        selected_tab = st.selectbox("Select to manage records", self.admin_manage, index=0)

        # Define the content for each tab
        if selected_tab == "Create Record":
            self.create_records()
        elif selected_tab == "Update Record":
            self.update_records()
        elif selected_tab == "Delete Record":
            self.delete_records()
        elif selected_tab == "Create Roomunavailable":
            self.create_roomunavailable()
        elif selected_tab == "Create Reservation":
            self.create_reservation()
    
    def create_as_supervisor(self):
        st.write("# Manage Records")
        st.write("## Create Roomunavailable")

        self.create_roomunavailable()
    
    def create_as_regular(self):
        st.write("# Manage Records")
        st.write("## Create reservation")

        self.create_reservation()

    def create_records(self):
        st.write("# Create Records")	
        pass
    
    def update_records(self):
        st.write("# Update Records")
        pass
    
    def delete_records(self):
        st.write("# Delete Records")
        pass

    def create_reservation(self):
        pass

    def create_roomunavailable(self):
        pass