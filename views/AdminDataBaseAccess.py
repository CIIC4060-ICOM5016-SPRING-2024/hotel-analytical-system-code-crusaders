import requests
import pandas as pd
import streamlit as st

class AdminDataBaseAccess:

    access_type = [
        "View Records",
        "Search Records",
        "Create Record", 
        "Edit Record", 
        "Delete Record", 
    ]
    
    available_entities = [
        "Login",
        "Employee",
        "Hotel",
        "Chains",
        "Room",
        "RoomDescription",
        "RoomUnavailable",
        "Reserve",
        "Client",
    ]

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute

    def create(self):

        st.write("# Admin Database Access")
        selected_tab = st.selectbox("Select database access choice", self.access_type, index=0)

        # Define the content for each tab
        if selected_tab == "View Records":
            self.view_record()
        elif selected_tab == "Search Records":
            st.write("# Search Records")
        elif selected_tab == "Create Record":
            st.write("# Create Records")
        elif selected_tab == "Edit Record":
            st.write("# Edit Records")
        elif selected_tab == "Delete Record":
            st.write("# Delete Records")

    def view_record(self):
        st.write("# View Records")

        entity_selected = self.choose_entity()

        response = requests.get(f'{self.mainRoute}roomdescription')

        df = pd.DataFrame(response.json())

        # Define pagination parameters
        page_size = 10  # Number of records per page
        total_records = len(df)
        total_pages = (total_records + page_size - 1) // page_size

        # Get the page number from the user
        page_number = st.number_input("Enter page number", min_value=1, max_value=total_pages, value=1)

        # Calculate the start and end indices for the current page
        start_idx = (page_number - 1) * page_size
        end_idx = min(start_idx + page_size, total_records)

        # Display the records for the current page
        if start_idx < end_idx:
            st.table(df[start_idx:end_idx])
        else:
            st.write("No records to display for this page.")
        pass

    def choose_entity(self):
        return st.selectbox("Select Entity", self.available_entities, index=None, disabled=False)

    def display_table(self):
        pass