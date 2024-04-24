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
        pass

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
        st.title('Create Employee Account')
        self.create_logon()
        employee_position = self.create_employee()
        self.create_hotel_selection(employee_position)
        
        if st.button('Create!') and self.entered_username.strip() and self.entered_password.strip() and self.fname.strip() and self.lname.strip():
            response = requests.post(f'{self.mainRoute}user_logon', json=self.login_record)
            check_account_existance = response.json()

            if check_account_existance[1] is True:
                st.error('Invalid username')
                pass

            response = requests.post(f'{self.mainRoute}employee', json=self.employee_record)

            print(response.json())
            

            self.new_account = False
            self.login_success = False
            st.empty()
            st.rerun()
        else:
            st.error('Must fill up all fields')
    
    def create_logon(self):
        self.entered_username = st.text_input('Create Username')
        self.entered_password = st.text_input('Create Password', type='password')

        self.login_record = {
            'username': self.entered_username,
            'password': self.entered_password
        }

    def create_employee(self):
        self.fname = st.text_input('First Name')
        self.lname = st.text_input('Last Name')
        age = st.number_input('Age', min_value=18, step=1)
        position = st.selectbox('Job Position', ['Regular', 'Supervisor', 'Administrator'])

        if position == 'Supervisor':
            min_salary = 50000
            max_salary = 79999
        elif position == 'Administrator':
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
            'position': position,
            'salary': salary
        }

        return position

    def create_hotel_selection(self, employee_position):
        response = requests.get(f'{self.mainRoute}hotel')
        self.allHotels = response.json()

        available_hotels = []
        for hotel in self.allHotels:
            if hotel['hname'] != 'Administrative':
                available_hotels.append(hotel['hname'])
        
        if employee_position != 'Administrator':
            selected_option = st.selectbox('Select an Hotel from the chain above', available_hotels)
        else:
            selected_option = st.selectbox('Select an Hotel from the chain above', ['Administrative'])

        for hotel in self.allHotels:
            if hotel['hname'] == selected_option:
                self.employee_record['hid'] = hotel['hid']
                break
        
        
