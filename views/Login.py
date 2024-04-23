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

    def __init__(self):
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
            response = requests.post(f'{self.mainRoute}login', json = {'username': username, 'password': password})

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
        st.title('Create Account')
        username = st.text_input('Create Username')
        password = st.text_input('Create Password', type='password')
        user_created_account = st.button('Create!')

        if user_created_account:
            # response = requests.post(f'{self.mainRoute}login', json = {'username': username, 'password': password})
            self.new_account = False
            self.login_success = False
            st.empty()
            st.rerun()

            print(username, password)