import streamlit as st
import requests

def login_frontend():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    login_button = st.button('Login')

    # if login_button:
    #     response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
    #     if response.status_code == 200:
    #         user_details = response.json()
    #         print(user_details)
    #         # st.success(f'Welcome, {user_details["username"]}!')
    #         # Redirect to main app or show other content...
    #     else:
    #         st.error('Invalid credentials')

login_frontend()