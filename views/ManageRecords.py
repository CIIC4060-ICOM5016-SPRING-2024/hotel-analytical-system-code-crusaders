import datetime
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

    tables = {
        'login': [
            ('employee', str),
            ('username', str),   
            ('password', str)
        ],
        
        'employee': [
            ('fname', str), 
            ('lname', str),   
            ('age', int), 
            ('position', ['Administrator', 'Supervisor', 'regular']), 
            ('salary', float)
        ],
        
        'chains': [
            ('cname',      str), 
            ('springmkup', float), 
            ('fallmkup',   float), 
            ('wintermkup', float)
        ],
        
        'hotel': [
            ('chains', 'search', 'chid', 'cname', None), 
            ('hname', str), 
            ('hcity', str)
        ],
        
        'room': [
            ('hotel', 'search', 'hid', 'hname', None),
            ('roomdescription', 'search', 'rdid', 'rname', None),
            ('rprice', float)
        ],
        
        'roomunavailable': [
            ('room', 'search', 'rid', 'rid', None), 
            ('startdate', 'date'), 
            ('enddate',   'date')
        ],

        'roomdescription': [
            ('rname', str), 
            ('rtype', str), 
            ('capacity',   int), 
            ('ishandicap', bool)
        ],

        'client': [
            ('fname', str), 
            ('lname', str), 
            ('age',   int), 
            ('memberyear', int)
        ],
        
        'reserve': [
            ('roomunavailable', str),
            ('client', 'search', 'clid', 'fname', 'match'), 
            ('total_cost', float), 
            ('payment', float), 
            ('guests', int)
        ],
    }

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
        self.create_roomunavailable()
    
    def create_as_regular(self):
        self.create_reservation()

    def create_records(self):
        st.write("# Create Records")

        table_selected = st.selectbox("Select which table to create a new record", self.tables.keys(), index=None, disabled=False)

        if table_selected is None:
            return

        result = self.create_widgets(table_selected)
        fields = result[1]
        valid_to_create = result[0]

        print(fields)

        if st.button('create', disabled=not valid_to_create) and valid_to_create:
            response = requests.post(f'{self.mainRoute}{table_selected}', json=fields)

            if response.status_code == 200:
                st.success('Operation completed successfully!')
            else:
                st.error('Operation failed, check the fields you provided')
        else:
            st.warning('All fields must be filled up to create')
    
    def update_records(self):
        st.write("# Update Records")
        pass
    
    def delete_records(self):
        st.write("# Delete Records")
        pass

    def create_reservation(self):
        st.write("# Create Reservation")	
        pass

    def create_roomunavailable(self):
        st.write("# Create Roomunavailable")	
        pass

    def create_widgets(self, table_selected):

        valid_to_create = True
        fields = {}
        for column in self.tables[table_selected]:
            column_name = column[0]

            if column_name in self.tables:
                if column[1] == 'search' and column[4] is None:
                    response = requests.get(f'{self.mainRoute}{column_name}')
                    display_names = {}
                    for record in response.json():
                        display_names.update({record[column[3]] : record[column[2]]})
                    id = display_names[st.selectbox(f"Select {column_name}", display_names.keys(), index=0)]
                    fields.update({column[2]: id})
                
                elif column[1] == 'search' and column[4] == 'match':
                    to_search = st.text_input(f"Search for {column_name}", '')

                    response = requests.get(f'{self.mainRoute}{column_name}')
                    id_found = -2
                    for record in response.json():
                        if record[column[3]] == to_search:
                            id_found = record[column[2]]
                            break
                    
                    if id_found == -2:
                        st.warning('Such record doesnt exist in database')
                        valid_to_create = False
                    else:
                        fields.update({column[2]: id_found})
                else:
                    result = self.create_widgets(column_name)
                    fields.update(result[1])
                    valid_to_create = result[0]

            elif column[1] == 'date':
                fields.update({column[0]: st.date_input(f"Select a date {column_name}")})

            elif type(column[1]) is list:
                selected_content = st.selectbox(f"Select {column_name}", column[1], index=0)
                fields.update({column[0]: selected_content})

            elif column[1] is int:
                fields.update({column_name : st.number_input(f"provide {column_name}", min_value=1)})
            elif column[1] is str:
                string_value = st.text_input(f"provide {column_name}", "")
                if not string_value:
                    valid_to_create = False
                fields.update({column_name : string_value})
            elif column[1] is float:
                fields.update({column_name : st.number_input(f"set value for {column_name}")})
            elif column[1] is bool:
                fields.update({column_name : st.checkbox(f"check if {column_name}")})

        return (valid_to_create, fields)