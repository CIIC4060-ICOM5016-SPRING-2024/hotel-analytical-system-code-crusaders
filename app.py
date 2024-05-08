import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
import plotly.express as px

from views.Login import Login
from views.Dashboard import Dashboard

SERVER = "heroku"

class FApplication:

    # Flask route
    mainRoute = None

    @staticmethod
    def init():
        if "fapp_singleton" not in st.session_state:
            st.session_state.fapp_singleton = FApplication()

        login = st.session_state.fapp_singleton.loginHandle
        
        if login.new_account is True:
            login.create_account()
        elif not login.login_success:
            login.login_user()
        else:
            dashboard = Dashboard(login.position)
        pass

    def __init__(self):
        if SERVER == "heroku":
            self.mainRoute = 'https://pdb-f386d9f3feff.herokuapp.com/codecrusaders/'
        else:
            self.mainRoute = 'http://127.0.0.1:5000/'

        # Create new login object
        self.loginHandle = Login(self.mainRoute)
        pass

    def createDashboard(self):
        self.dashboard = Dashboard(st.session_state.position)

# # Run the main function to start the Streamlit app
if __name__ == "__main__":
    FApplication.init()