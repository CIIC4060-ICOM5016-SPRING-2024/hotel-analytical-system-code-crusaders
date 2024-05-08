import requests
import pandas as pd
import streamlit as st

class AdminDataBaseAccess:

    access_type = [
        "View Records",
        "Search Records",
    ]
    
    available_entities = [
        "login",
        "employee",
        "hotel",
        "chains",
        "room",
        "roomdescription",
        "roomunavailable",
        "reserve",
        "client",
    ]

    searchable_content = [
        "login",
        "employee",
        "hotel",
        "chains",
        "room information",
        "client information",
    ]

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute

    def create(self):

        st.write("# Admin Database Access")
        # Always choose the first choice
        selected_tab = st.selectbox("Select database access choice", self.access_type, index=0)

        # Define the content for each tab
        if selected_tab == "View Records":
            self.view_record()
        elif selected_tab == "Search Records":
            self.search_record()

    def view_record(self):
        st.write("# View Records")

        # Obtain the chosen entity to work with
        entity_selected = self.choose_entity()
        if not entity_selected:
            st.number_input("Enter page number", min_value=1, max_value=1, value=1, disabled=True)
            return

        response = requests.get(f'{self.mainRoute}{entity_selected}')
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


    def search_record(self):
        st.write("# Search Record")

        entity_selected = st.selectbox("Select what to search", self.searchable_content, index=None, disabled=False)
        if not entity_selected:
            return

        if entity_selected == "login":
            entered_username = st.text_input("Enter Username to look up", '')
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
            
            st.table(user_logger_data)

        elif entity_selected == "employee":
            entered_firstname = st.text_input("Enter Employee's First Name to look up", "")
            entered_lastname = st.text_input("Enter Employee's Last Name to look up", "")

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
            
            st.table(found_employee_data)

        elif entity_selected == "hotel":
            response = requests.get(f'{self.mainRoute}hotel')

            entered_hotel = st.selectbox('Select a Hotel to look up', self.login.getHotels(response.json()), index=None)

            if not entered_hotel:
                return
            
            found_hotel_data = {}
            for hotel_data in response.json():
                if hotel_data['hname'] == entered_hotel:
                    found_hotel_data = hotel_data
                    break
            
            st.table(found_hotel_data)

        elif entity_selected == "chains":

            response = requests.get(f'{self.mainRoute}chains')
            entered_chain = st.selectbox('Enter a Chain to look up', self.login.getChains(response.json()), index=None)

            if not entered_chain:
                return
            
            found_chain_data = {}
            for chain_data in response.json():
                if chain_data['cname'] == entered_chain:
                    found_chain_data = chain_data
                    break
            
            st.table(found_chain_data)

        elif entity_selected == "room information":
            # This will display a table with all the room information
            hotel_response = requests.get(f'{self.mainRoute}hotel')
            entered_hotel = st.selectbox('Select a Hotel name', self.login.getHotels(hotel_response.json()), index=None)
            
            roomdescription_response = requests.get(f'{self.mainRoute}roomdescription')

            roomdescription_names = set([])
            for roomdescription_data in roomdescription_response.json():
                roomdescription_names.add(roomdescription_data['rname'])

            entered_room = st.selectbox('Enter the Room Name to look up', roomdescription_names, index=None)
            
            room_response = requests.get(f'{self.mainRoute}room')
            
            if not entered_hotel or not entered_room:
                return

            found_roomdescription = False
            found_roomdescription_data = {}
            for roomdescription_data in roomdescription_response.json():
                if roomdescription_data['rname'] == entered_room:
                    found_roomdescription = True
                    found_roomdescription_data = roomdescription_data
                    break

            if not found_roomdescription:
                st.warning('No room found in Database')
                return

            # show room details
            st.write(f"### Information related to {entered_room} room")
            st.table(found_roomdescription_data)

            # show the room count
            room_count = 0
            avg_room_price = 0
            room_prices = {}
            for room_data in room_response.json():
                if room_data['rdid'] == found_roomdescription_data['rdid']:
                    room_id = room_data['rid']
                    room_count += 1
                    avg_room_price += room_data['rprice']
                    room_prices.update({f'room id: {room_id}': str(room_data['rprice']) + '$'})
            
            avg_room_price /= room_count

            st.write(f"### Room count and average price related to {entered_room}")
            st.table({'room count': int(room_count), 'rooms average price': str(float(avg_room_price)) + '$'})

            room_type = found_roomdescription_data['rtype']
            st.write(f"### Avaliable prices for {room_type}")
            st.table(room_prices)


        elif entity_selected == "client information":
            client_fname = st.text_input("Enter the Client's first name to look up", "")
            client_lname = st.text_input("Enter the Client's last name to look up", "")
            
            client_response = requests.get(f'{self.mainRoute}client')
            reserve_response = requests.get(f'{self.mainRoute}reserve')

            found_client = False
            found_client_data = {}
            for client_data in client_response.json():
                if client_data['fname'] == client_fname and client_data['lname'] == client_lname:
                    found_client = True
                    found_client_data = client_data
                    break

            if not found_client:
                st.warning('No matching client found in database')
                return

            # show member year
            member_year = found_client_data['memberyear']

            st.write(f"### Client Information")

            client_info = {
                'Client First Name': found_client_data['fname'],
                'Client Last Name': found_client_data['lname'],
                'Client Age': found_client_data['age'],
                'Client member year': member_year,
            }
            st.table(client_info)

            # Find reservations related to the cliend provided
            found_reserve = False
            found_reserve_data = []
            for reserve_data in reserve_response.json():
                if reserve_data['clid'] == found_client_data['clid']:
                    found_reserve = True
                    found_reserve_data.append(reserve_data)
            
            if not found_reserve:
                st.warning(f"{client_fname} {client_lname} doesn't have any reservations")
                return
            
            # show reservation for this client
            st.write(f"### All reservations that {client_fname} has")
            st.table(found_reserve_data)

    def choose_entity(self):
        return st.selectbox("Select Entity", self.available_entities, index=None, disabled=False)