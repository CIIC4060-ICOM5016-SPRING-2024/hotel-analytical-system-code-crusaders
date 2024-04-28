import requests
import streamlit as st

class Login:

    username = None
    password = None

    chainID = None
    hotelID = None
    employeeID = None

    position = 'Regular'

    new_account = False
    login_success = False

    def __init__(self, mainRoute):
        self.mainRoute = mainRoute

    def getLoginJson(self):
        return {'username': self.username, 'password': self.password}
    
    def getHotels(self, hotel_list_json):
        available_hotels = []
        for hotel in hotel_list_json:
            if hotel['hname'] != 'Administrative':
                available_hotels.append(hotel['hname'])
        return available_hotels
    
    def getHotelID(self, target_hotel, hotel_list_json):
        for hotel in hotel_list_json:
            if hotel['hname'] == target_hotel:
                return hotel['hid']
        return -1
    
    def getChains(self, chain_list_json):
        available_chains = []
        for chain in chain_list_json:
            if chain['cname'] != 'Administrative':
                available_chains.append(chain['cname'])
        return available_chains
    
    def getChainID(self, target_chain, chain_list_json):
        for chain in chain_list_json:
            if chain['cname'] == target_chain:
                return chain['chid']
        return -1
    
    def getChainData(self, target_chain, chain_list_json):
        for chain in chain_list_json:
            if chain['chid'] == target_chain:
                return chain
        return None
    
    def getHotelData(self, target_hotel, hotel_list_json):
        for hotel in hotel_list_json:
            if hotel['hid'] == target_hotel:
                return hotel
        return None

    def getHotelFromChain(self, target_chain, hotel_list_json):
        for hotel in hotel_list_json:
            if hotel['chid'] == target_chain:
                return hotel['hid']
        return -1
    
    def getAllHotelsFromChain(self, target_chain, hotel_list_json):
        hotel_list = []
        for hotel in hotel_list_json:
            if hotel['chid'] == target_chain:
                hotel_list.append(hotel)
        return hotel_list

    def login_user(self):
        # Login user
        st.title('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        user_logged_in_button = st.button('login')
        
        # Create account prompt
        st.write("Don't have an account?")
        user_create_account_button = st.button("Sign up")

        if user_logged_in_button:
            response = requests.post(f'{self.mainRoute}user_logon', json = {'username': username, 'password': password})

            user_details = response.json()
            if user_details[1] is not False:
                self.username = username
                self.password = password

                self.chainID  = user_details[0]['chid']
                self.hotelID  = user_details[0]['hid']
                self.position = user_details[0]['position']
                
                self.new_account = False
                self.login_success = True
                st.empty()
                st.rerun()
            else:
                st.error('Invalid credentials')

        if user_create_account_button:
            self.new_account = True
            self.login_success = False
            st.empty()
            st.rerun()

    def create_account(self):
        # Create account
        st.write('# Create a new Employee Account')
        
        self.create_logon()
        self.create_employee()
        self.create_hotel_selection()
        
        # Check if is valid to create when button is pressed
        if st.button('Create!') and self.entered_username.strip() and self.entered_password.strip() and self.fname.strip() and self.lname.strip():
            response = requests.post(f'{self.mainRoute}user_logon', json=self.login_record)
            check_account_existance = response.json()

            if check_account_existance[1] is True:
                st.error('Invalid username')
                pass

            response = requests.post(f'{self.mainRoute}employee', json=self.employee_record)
            employee_id = response.json()
            self.login_record['eid'] = employee_id
            response = requests.post(f'{self.mainRoute}login', json=self.login_record)
    
            self.new_account = False
            self.login_success = False
            st.empty()
            st.rerun()
        else:
            st.warning('Must fill up all fields')
    
    def create_logon(self):
        st.write('### Provide Login Credentials')
        self.entered_username = st.text_input('Create Username')
        self.entered_password = st.text_input('Create Password', type='password')

        self.login_record = {
            'username': self.entered_username,
            'password': self.entered_password
        }

    def create_employee(self):
        st.write('### Provide Employee Details')
        self.fname = st.text_input('First Name')
        self.lname = st.text_input('Last Name')
        age = st.number_input('Age', min_value=18, step=1)
        self.created_position = st.selectbox('Job Position', ['Regular', 'Supervisor', 'Administrator'])

        if self.created_position == 'Supervisor':
            min_salary = 50000
            max_salary = 79999
        elif self.created_position == 'Administrator':
            min_salary = 80000
            max_salary = 120000
        else:
            min_salary = 18000
            max_salary = 49999

        salary = st.number_input('Salary', min_value=min_salary, max_value=max_salary, step=1000)

        self.employee_record = {
            'fname': self.fname,
            'lname': self.lname,
            'age': age,
            'position': self.created_position,
            'salary': salary
        }

    def create_hotel_selection(self):

        if self.created_position == 'Regular':
            # if employee is regular, then just obtain the
            # ID of the hotel that the employee will work on
            response = requests.get(f'{self.mainRoute}hotel')
            all_hotels = response.json()
            selected_option = st.selectbox('Select an Hotel to work as regular employee', self.getHotels(all_hotels))
            
            self.employee_record['hid'] = self.getHotelID(selected_option, all_hotels)

        elif self.created_position == 'Supervisor':
            # if employee is supervisor, select a chain to
            # work on, and from that chain.. look the first
            # hotel that is related to such chainID just for reference
            response = requests.get(f'{self.mainRoute}chains')
            selected_option = st.selectbox('Select an Chain to supervise', self.getChains(response.json()))

            hotel_response = requests.get(f'{self.mainRoute}hotel')
            self.employee_record['hid'] = self.getHotelFromChain(self.getChainID(selected_option, response.json()), hotel_response.json())

        elif self.created_position == 'Administrator':
            # if the employee is administrator, just set the hotel to -1 since its administrator
            selected_option = st.selectbox('Select an Hotel from the chain above', ['Administrative'])
            self.employee_record['hid'] = -1
        else:
            st.error(f'Position {self.created_position} is not valid to work as')