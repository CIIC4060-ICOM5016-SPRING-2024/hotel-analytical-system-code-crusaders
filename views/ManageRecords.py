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

        table_selected = st.selectbox("Select what to update", self.searchable_content, index=None, disabled=False)
        if not table_selected:
            return

        update_data = {}

        if table_selected == "login":

            entered_lid = st.number_input("enter user ID", min_value=1)
            entered_username = st.text_input("Enter Username", '')

            if not entered_username and not entered_lid:
                return

            response = requests.get(f'{self.mainRoute}login/{entered_lid}')
            record = response.json()

            record_found = False
            if record['username'] == entered_username:
                record_found = True
                st.table(record)
            else:
                st.warning("User is not in Database")

            if record_found:
                eid = st.number_input("Change employee ID", min_value=1)
                user = st.text_input("Change username", '')
                password = st.text_input("Change password", '')
                if not user == "" and not password == "" and not eid == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'eid': int(eid), 'username': user, 'password': password})
                       # final_update = requests.put(f'{self.mainRoute}login/{entered_lid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "employee":

            entered_eid = st.number_input("Enter employee id", min_value=1)
            entered_name = st.text_input("Enter employee first name", '')

            if not entered_name and not entered_eid:
                return

            response = requests.get(f'{self.mainRoute}employee/{entered_eid}')
            record = response.json()
            
            if response.status_code != 200:
                return

            record_found = False
            if record['fname'] == entered_name:
                record_found = True
                st.table(record)
            else:
                st.warning("Employee is not in Database")

            if record_found:
                hid = st.number_input("Change hotel ID", min_value=1)
                firstname = st.text_input("Change first name", '')
                lastname = st.text_input("Change last name", '')
                age = st.number_input("Change age", min_value=18)
                position = st.selectbox("Change position", ['Administrator', 'Regular', 'Supervisor'], index=0)
                salary = st.number_input("Change salary", step=0.01)
                if not firstname == "" and not lastname == "" and not age == "" and not position == "" and not salary == "" and not hid == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'hid': int(hid), 'fname': firstname, 'lname': lastname, 'age': int(age), 'position': position, 'salary': float(salary)})
                       # final_update = requests.put(f'{self.mainRoute}employee/{entered_eid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "hotel":
            entered_hid = st.number_input("Enter hotel id", min_value=1)
            entered_hname = st.text_input("Enter hotel name", '')

            if not entered_hid and not entered_hname:
                return

            response = requests.get(f'{self.mainRoute}hotel/{entered_hid}')
            record = response.json()
            record_found = False
            if record['hname'] == entered_hname:
                record_found = True
                st.table(record)
            else:
                st.warning("Hotel is not in Database")

            if record_found:
                chid = st.number_input("Change chain ID", min_value=1)
                hotelname = st.text_input("Change hotel name", '')
                hcity = st.text_input("Change hotel city", '')
                if not hotelname == "" and not hcity == "" and not chid == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'chid': int(chid), 'hname': hotelname, 'hcity': hcity})
                       # final_update = requests.put(f'{self.mainRoute}hotel/{entered_hid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "chains":
            entered_chid = st.number_input("Enter chain id", min_value=1)
            entered_cname = st.text_input("Enter chain name", '')

            if not entered_chid and not entered_cname:
                return

            response = requests.get(f'{self.mainRoute}chains/{entered_chid}')
            record = response.json()
            record_found = False
            if record['cname'] == entered_cname:
                record_found = True
                st.table(record)
            else:
                st.warning("Chain is not in Database")

            if record_found:
                cname = st.text_input("Change cname", '')
                fallmkup   = st.number_input("Change fallmgkup",   step=0.01)
                springmkup = st.number_input("Change springmgkup", step=0.01)
                summermkup = st.number_input("Change summermgkup", step=0.01)
                wintermkup = st.number_input("Change wintermgkup", step=0.01)
                if not cname == "" or not springmkup == "" or not summermkup == "" or not fallmkup == "" or not wintermkup == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'cname': cname, 'springmkup': float(springmkup), 'summermkup': float(summermkup), 'fallmkup': float(fallmkup), 'wintermkup': float(wintermkup)})
                       # final_update = requests.put(f'{self.mainRoute}chains/{entered_chid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "room":
            entered_rid = st.number_input("enter room ID", min_value=1)
            if not entered_rid:
                return

            response = requests.get(f'{self.mainRoute}room/{entered_rid}')
            record = response.json()
            record_found = False
            if record[0]['rid'] == float(entered_rid):
                record_found = True
                st.table(record)
            else:
                st.warning("Room is not in Database")

            if record_found:
                hotel_id = st.number_input("Change Hotel ID", min_value=1)
                room_desc_id = st.number_input("Change Room Description ID", min_value=1)
                rprice = st.number_input("Change room price", step=0.01)
                if not rprice == "" and not hotel_id == "" and not room_desc_id == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'hid': int(hotel_id), 'rdid': int(room_desc_id), 'rprice': float(rprice)})
                       # final_update = requests.put(f'{self.mainRoute}room/{entered_rid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "client":
            entered_clid = st.number_input("enter client ID", min_value=1)
            entered_fname = st.text_input("enter client First name", '')

            if not entered_clid and not entered_fname:
                return

            response = requests.get(f'{self.mainRoute}client/{entered_clid}')
            record = response.json()
            record_found = False
            if record[0]['fname'] == entered_fname:
                record_found = True
                st.table(record)
            else:
                st.warning("Client is not in Database")

            if record_found:
                clientname     = st.text_input("enter client first name")
                clientlastname = st.text_input("enter client Last name")
                clientage      = st.number_input("enter client age", min_value=1)
                memberyear     = st.text_input("enter client memberyear")
                if not clientname == "" or not clientlastname == "" or not clientage == "" or not memberyear == "":
                    if st.button("update"):
                        st.write("success")
                        update_data.update({'fname': clientname, 'lname': clientlastname, 'age': int(clientage), 'memberyear': int(memberyear)})
                        # final_update = requests.put(f'{self.mainRoute}client/{entered_clid}', json=update_data)
                        st.write(update_data)

        elif table_selected == "roomunavailable":
            entered_ruid = st.number_input("enter user room unavailable id", min_value=1)
            if not entered_ruid:
                return

            response = requests.get(f'{self.mainRoute}roomunavailable/{entered_ruid}')
            record = response.json()
            record_found = False
            if record['ruid'] == float(entered_ruid):
                record_found = True
                st.table(record)
            else:
                st.warning("Room unavailable is not in Database")

            if record_found:
                room_id = st.number_input("Change room id", min_value=1)
                stardate = st.date_input("Change startdate",value=None)
                enddate = st.date_input("Change enddate",value=None)
                if not stardate == "" and not enddate == "" and not room_id == "":
                   if st.button("update"):
                       st.write("success")
                       update_data.update({'rid': int(room_id), 'startdate': stardate, 'enddate': enddate})
                       # final_update = requests.put(f'{self.mainRoute}roomunavailable/{entered_ruid}', json=update_data)
                       st.write(update_data)

        elif table_selected == "roomdescription":
            entered_rdid = st.number_input("enter user room description id", min_value=1)
            if not entered_rdid:
                return

            response = requests.get(f'{self.mainRoute}roomdescription/{entered_rdid}')
            record = response.json()
            record_found = False
            if record['rdid'] == float(entered_rdid):
                record_found = True
                st.table(record)
            else:
                st.warning("Room description is not in Database")

            if record_found:
                rname = st.text_input("Change room description name", '')
                rtype = st.text_input("Change room despcription type", '')
                capacity = st.number_input("Change room capacity", min_value=1)
                ishandicap = st.checkbox("Change handicap")
                if not rname == "" and not rtype == "" and not capacity == "" and not ishandicap == "":
                    if st.button("update"):
                        st.write("success")
                        update_data.update({'rname': rname, 'rtype': rtype, 'capacity': int(capacity), 'ishandicap': ishandicap})
                        # final_update = requests.put(f'{self.mainRoute}roomdescription/{entered_rdid}', json=update_data)
                        st.write(update_data)

        elif table_selected == "reserve":
            entered_reid = st.number_input("enter user room reserve id", min_value=1)
            if not entered_reid:
                return

            response = requests.get(f'{self.mainRoute}reserve/{entered_reid}')
            record = response.json()
            record_found = False
            if record[0]['reid'] == float(entered_reid):
                record_found = True
                st.table(record)
            else:
                st.warning("Reserve is not in Database")

            if record_found:
                room_unv_id = st.number_input("Change room unavailable id", min_value=1)
                client_id   = st.number_input("Change client id", min_value=1)
                total_cost  = st.number_input("Change reservation total_cost", step=0.01)
                payment = st.text_input("Change reservation payment", '')
                guests  = st.number_input("Change reservation numbers of guests", min_value=1)
                if not total_cost == "" and not payment == "" and not guests == "" and not room_unv_id == "" and not client_id == "":
                    if st.button("update"):
                        st.write("success")
                        update_data.update({'ruid': int(room_unv_id), 'clid': int(client_id), 'total_cost': float(total_cost), 'payment': payment, 'guests': int(guests)})
                        # final_update = requests.put(f'{self.mainRoute}hotel/{entered_reid}', json=update_data)
                        st.write(update_data)

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