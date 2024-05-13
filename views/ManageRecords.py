import datetime
import requests
import pandas as pd
import streamlit as st

class ManageRecords:

    admin_manage = [
        "Create Record", 
        "Update Record", 
        "Delete Record", 
    ]

    tables = {
        'login': [
            ('employee', str, 'eid'),
            ('username', str),   
            ('password', str)
        ],
        
        'employee': [
            ('hotel', 'search', 'hid', 'hname', None),
            ('fname', str), 
            ('lname', str),   
            ('age', int), 
            ('position', ['Administrator', 'Supervisor', 'regular']), 
            ('salary', float)
        ],
        
        'chains': [
            ('cname',      str), 
            ('springmkup', float), 
            ('summermkup', float), 
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
            ('roomunavailable', str, 'ruid'),
            ('client', 'search', 'clid', 'fname', 'match'), 
            ('total_cost', float), 
            ('payment', ['pear pay', 'credit card', 'check', 'debit card', 'cash']), 
            ('guests', int)
        ],
    }
    searchable_content = [
        "login",
        "employee",
        "hotel",
        "chains",
        "room",
        "client",
        "roomunavailable",
        "roomdescription",
        "reserve",
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
            st.write("# Create Records")
            table_selected = st.selectbox("Select which table to create a new record", self.tables.keys(), index=None, disabled=False)
            self.create_records(table_selected)
        elif selected_tab == "Update Record":
            self.update_records()
        elif selected_tab == "Delete Record":
            self.delete_records()
    
    def create_as_supervisor(self):
        self.create_roomunavailable()
    
    def create_as_regular(self):
        self.create_reservation()

    def create_records(self, table_selected):
        if table_selected is None:
            return

        result = self.create_widgets(table_selected)
        valid_to_create = result[0]
        fields = result[1]
        complementary = result[2]
        complementary_name = result[3]
        complementary_id_name = result[4]

        # print(table_selected, fields)
        # print(complementary_id_name, complementary_name, complementary)

        if st.button('create', disabled=not valid_to_create) and valid_to_create:
            # Check for the complementary table post response
            if complementary_name is not None:
                complementary_response = requests.post(f'{self.mainRoute}{complementary_name}', json=complementary)
                if complementary_response.status_code != 200:
                    st.error('Operation failed on subrecord, check the fields you provided')
                    return
                id_value = complementary_response.json()
                fields.update({complementary_id_name: id_value})
                # print(complementary_id_name, complementary_name, complementary)

            # print(table_selected, fields)
            main_response = requests.post(f'{self.mainRoute}{table_selected}', json=fields)
            if main_response.status_code == 200:
                st.success('Operation completed successfully!')
            else:
                st.error('Operation failed, check the fields you provided')
        elif not valid_to_create:
            st.warning('All fields must be filled up to create')

    def create_reservation(self):
        st.write("# Create Reservation")
        self.create_records('reserve')

    def create_roomunavailable(self):
        st.write("# Create Roomunavailable")
        self.create_records('roomunavailable')
    
    def update_records(self):
        st.write("# Update Records")
        pass
    
    def delete_records(self):
        st.write("# Delete Records")

        entity_selected = st.selectbox("Select what to delete", self.searchable_content, index=None, disabled=False)
        if not entity_selected:
            return

        if entity_selected == "login":
            self.delete_login()
        elif entity_selected == "employee":
            self.delete_employee()
        elif entity_selected == "hotel":
            self.delete_hotel()
        elif entity_selected == "chains":
            self.delete_chains()
        elif entity_selected == "room":
            self.delete_room()
        elif entity_selected == "roomunavailable":
            self.delete_roomunavailable()
        elif entity_selected == "roomdescription":
            self.delete_roomdescription()
        elif entity_selected == "reserve":
            self.delete_reserve()
        elif entity_selected == "client":
            self.delete_client()

    def create_widgets(self, table_selected):

        valid_to_create = True
        main_fields = {}
        complementary_fields = {}
        complementary_table_name = None
        complementary_table_id = None
        widgets_used = []

        for column in self.tables[table_selected]:
            column_name = column[0]

            if column_name in self.tables:
                if column[1] == 'search' and column[4] is None:
                    response = requests.get(f'{self.mainRoute}{column_name}')
                    display_names = {}
                    for record in response.json():
                        display_names.update({record[column[3]] : record[column[2]]})

                    selection = st.selectbox(f"Select {column_name}", display_names.keys(), index=0)
                    id = display_names[selection]
                    main_fields.update({column[2]: id})
                    widgets_used.append(selection)
                
                elif column[1] == 'search' and column[4] == 'match':
                    to_search = st.text_input(f"Search for {column_name}", '')
                    widgets_used.append(to_search)

                    response = requests.get(f'{self.mainRoute}{column_name}')

                    recommended_names = {}
                    for record in response.json():
                        if not to_search:
                            break
                        if to_search.lower() in record[column[3]].lower():
                            recommended_names.update({record[column[3]] : record[column[2]]})

                    if len(recommended_names) != 0:
                        st.table(recommended_names)

                    id_found = -2
                    for record in response.json():
                        if record[column[3]] == to_search:
                            id_found = record[column[2]]
                            break
                    
                    if id_found == -2:
                        st.warning('Such record doesnt exist in database')
                        valid_to_create = False
                    else:
                        main_fields.update({column[2]: id_found})
                else:
                    result = self.create_widgets(column_name)
                    complementary_fields.update(result[1])
                    valid_to_create = result[0]
                    complementary_table_id = column[2]
                    complementary_table_name = column_name
                    widgets_used.append(result[5])

            elif column[1] == 'date':
                selected_date = st.date_input(f"Select a date {column_name}")
                widgets_used.append(selected_date)
                formatted_date = selected_date.strftime('%Y-%m-%d')
                main_fields.update({column[0]: formatted_date})

            elif type(column[1]) is list:
                selected_content = st.selectbox(f"Select {column_name}", column[1], index=0)
                widgets_used.append(selected_content)
                main_fields.update({column[0]: selected_content})

            elif column[1] is int:
                selected_number = st.number_input(f"provide {column_name}", min_value=1)
                widgets_used.append(selected_number)
                main_fields.update({column_name : selected_number})
            elif column[1] is str:
                string_value = st.text_input(f"provide {column_name}", "")
                widgets_used.append(string_value)
                if not string_value:
                    valid_to_create = False
                main_fields.update({column_name : string_value})
            elif column[1] is float:
                selected_number = st.number_input(f"set value for {column_name}")
                widgets_used.append(selected_number)
                main_fields.update({column_name : selected_number})
            elif column[1] is bool:
                check_box = st.checkbox(f"check if {column_name}")
                widgets_used.append(check_box)
                main_fields.update({column_name : check_box})

        return (valid_to_create, main_fields, complementary_fields, complementary_table_name, complementary_table_id, widgets_used)
    
    def handle_delete_button(self, table_name, entity_id):
        if st.button('delete'):
            request = requests.delete(f'{self.mainRoute}{table_name}/{entity_id}')
            if request.status_code == 200:
                st.success('Deleted successfully')
            elif request.status_code == 404:
                st.error('No record was found for the given parameters')
            elif request.status_code == 401:
                st.error('You can only delete the "leafs" first before deleting this record.')

    def delete_login(self):
        entered_username = st.text_input("Enter Username to delete", '')
        if not entered_username:
            return

        response = requests.get(f'{self.mainRoute}login')

        found_user = False
        user_logger_data = {}
        for login_data in response.json():
            if login_data['username'] == entered_username:
                found_user = True
                user_logger_data = login_data
                break

        if not found_user:
            st.warning("User is not in Database")
            return
        id = user_logger_data["lid"]
        st.write(id)
        st.table(user_logger_data)

        self.handle_delete_button('login', id)

    def delete_employee(self):
        entered_firstname = st.text_input("Enter Employee's First Name to delete", "")
        entered_lastname = st.text_input("Enter Employee's Last Name to delete", "")

        if not entered_firstname or not entered_lastname:
            return

        response = requests.get(f'{self.mainRoute}employee')

        found_employee = False
        found_employee_data = {}
        for employee_data in response.json():
            if employee_data['fname'] == entered_firstname and employee_data['lname'] == entered_lastname:
                found_employee = True
                found_employee_data = employee_data
                break

        if not found_employee:
            st.warning("Employee is not in Database")
            return
        id = found_employee_data["eid"]
        st.write(id)
        st.table(found_employee_data)

        self.handle_delete_button('employee', id)

    def delete_hotel(self):
        response = requests.get(f'{self.mainRoute}hotel')

        entered_hotel = st.selectbox('Select a Hotel to delete', self.login.getHotels(response.json()), index=None)

        if not entered_hotel:
            return

        found_hotel_data = {}
        for hotel_data in response.json():
            if hotel_data['hname'] == entered_hotel:
                found_hotel_data = hotel_data
                break
        id = found_hotel_data["hid"]
        st.write(id)
        st.table(found_hotel_data)

        self.handle_delete_button('hotel', id)

    def delete_chains(self):
        response = requests.get(f'{self.mainRoute}chains')
        entered_chain = st.selectbox('Enter a Chain to delete', self.login.getChains(response.json()), index=None)

        if not entered_chain:
            return

        found_chain_data = {}
        for chain_data in response.json():
            if chain_data['cname'] == entered_chain:
                found_chain_data = chain_data
                break
        id = found_chain_data["cid"]
        st.write(id)
        st.table(found_chain_data)

        self.handle_delete_button('chains', id)

    def delete_room(self):
        response = requests.get(f'{self.mainRoute}room')
        entered_room = st.text_input('Enter a Room ID to delete')

        if not entered_room:
            return
        else:
            entered_room = float(entered_room)
        found_room_data = {}
        for room_data in response.json():
            if room_data['rid'] == entered_room:
                found_room_data = room_data
                break
        id = found_room_data["rid"]
        st.write(id)
        st.table(found_room_data)

        self.handle_delete_button('room', id)

    def delete_roomunavailable(self):
        response = requests.get(f'{self.mainRoute}roomunavailable')
        entered_room = st.text_input('Enter a Room Unavailable ID to delete')

        if not entered_room:
            return
        else:
            entered_room = float(entered_room)
        found_room_data = {}
        for room_data in response.json():
            if room_data['ruid'] == entered_room:
                found_room_data = room_data
                break
        id = found_room_data["ruid"]
        st.write(id)
        st.table(found_room_data)

        self.handle_delete_button('roomunavailable', id)

    def delete_roomdescription(self):
        response = requests.get(f'{self.mainRoute}roomdescription')
        entered_room = st.text_input('Enter a Room Description ID to delete')

        if not entered_room:
            return
        else:
            entered_room = float(entered_room)
        found_room_data = {}
        for room_data in response.json():
            if room_data['rdid'] == entered_room:
                found_room_data = room_data
                break
        id = found_room_data["rdid"]
        st.write(id)
        st.table(found_room_data)

        self.handle_delete_button('roomdescription', id)

    def delete_reserve(self):
        response = requests.get(f'{self.mainRoute}reserve')
        entered_reservation = st.text_input('Enter a Reservation ID to delete')

        if not entered_reservation:
            return
        else:
            entered_reservation = float(entered_reservation)
        found_reservation_data = {}
        for reservation_data in response.json():
            if reservation_data['reid'] == entered_reservation:
                found_reservation_data = reservation_data
                break
        id = found_reservation_data["reid"]
        st.write(id)
        st.table(found_reservation_data)

        self.handle_delete_button('reserve', id)

    def delete_client(self):
        entered_firstname = st.text_input("Enter Client's First Name to delete", "")
        entered_lastname = st.text_input("Enter Client's Last Name to delete", "")

        if not entered_firstname or not entered_lastname:
            return

        response = requests.get(f'{self.mainRoute}client')

        found_client = False
        found_client_data = {}
        for client_data in response.json():
            if client_data['fname'] == entered_firstname and client_data['lname'] == entered_lastname:
                found_client = True
                found_client_data = client_data
                break

        if not found_client:
            st.warning("Client is not in Database")
            return
        id = found_client_data["clid"]
        st.write(id)
        st.table(found_client_data)

        self.handle_delete_button('client', id)