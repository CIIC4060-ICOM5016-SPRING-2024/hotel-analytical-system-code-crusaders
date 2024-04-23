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

    fapplication_singleton = None

    # Flask route
    mainRoute = None

    loginHandle = None

    @staticmethod
    def create():
        if FApplication.fapplication_singleton is None:
            FApplication.fapplication_singleton = FApplication()
    
    @staticmethod
    def instance():
        return FApplication.fapplication_singleton

    @staticmethod
    def init():
        login = FApplication.fapplication_singleton.loginHandle
        
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
            self.mainRoute = 'http://localhost:5000/'

        # Create new login object
        self.loginHandle = Login()
        pass

    # check if data is received
    def checkstatus(self, tocheck):
        if tocheck.status_code == 200:
            return True
        else:
            return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")


    def createDashboard(self):
        self.dashboard = Dashboard(st.session_state.position)

        # select = st.selectbox("Choose Statistic", ("Top 3 highest paid regular employee",
        # "Top 5 hotel with the most client capacity", "Top 3 month with the most reservation by chain",
        # "Top 10% of the hotels that had the most reservations", "Top 3 rooms that were the least time unavailable",
        # "Total reservation percentage by payment method", "Top 3 rooms that had the least guest-to-capacity ratio"), index=None)
        # hotel = st.text_input("hotel id")
        # if select == "Top 3 highest paid regular employee":
        #     route = f'{self.mainRoute}hotel/{hotel}/highestpaid'
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(route, json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame.from_dict(response.json())
        #         st.table(df)
        #         bar_chart = alt.Chart(df).mark_bar().encode(
        #             y='salary',
        #             x='full_name',
        #             color ='full_name'
        #         )
        #         st.altair_chart(bar_chart, use_container_width=True)
        # elif select == "Top 5 hotel with the most client capacity":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}most/capacity', json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame.from_dict(response.json())
        #         st.table(df)
        #         bar_chart = alt.Chart(df).mark_bar().encode(
        #             y='total_capacity',
        #             x='hname',
        #             color = 'hname'
        #         )
        #         st.altair_chart(bar_chart, use_container_width=True)
        # elif select == "Top 3 month with the most reservation by chain":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}most/profitmonth', json=json_object)
        #     if self.checkstatus(response):
        #         #st.table(response.json())
        #         #st.bar_chart(response.json())
        #         df = pd.DataFrame.from_dict(response.json())
        #         st.table(df)
        #         bar_chart = alt.Chart(df).mark_bar().encode(
        #             x = 'year',
        #             y = 'total_reservations',
        #             column = 'name',
        #             color = 'month',
        #         )
        #         st.altair_chart(bar_chart, use_container_width=False)
        # elif select == "Top 3 rooms that were the least time unavailable":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}hotel/{hotel}/leastreserve', json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame(response.json(), columns=['datediff', 'rid'])
        #         st.write("Query Results:", df)
        #         st.bar_chart(df,x="rid",y="datediff")
        # elif select == "Top 10% of the hotels that had the most reservations":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}most/reservation', json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame(response.json(), columns=['hname', 'reservations'])
        #         st.write("Query Results:", df)
        #         st.bar_chart(df,x="hname",y="reservations")
        # elif select == "Total reservation percentage by payment method":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}paymentmethod', json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame(response.json(), columns=['payment', 'percentage'])
        #         fig = px.pie(df, values='percentage', names='payment')
        #         st.plotly_chart(fig)
        # elif select == "Top 3 rooms that had the least guest-to-capacity ratio":
        #     data = '{"username": "fmays2", "password": "mP6+bo"}'
        #     json_object = json.loads(data)
        #     response = requests.post(f'{self.mainRoute}hotel/{hotel}/leastguests', json=json_object)
        #     if self.checkstatus(response):
        #         df = pd.DataFrame(response.json(), columns=['rid', 'ratio'])
        #         st.write("Query Results:", df)
        #         st.bar_chart(df,x="rid",y="ratio")
   

# def main():

#     select = st.selectbox("Choose Statistic", ("Top 3 highest paid regular employee",
#     "Top 5 hotel with the most client capacity", "Top 3 month with the most reservation by chain",
#      "Top 10% of the hotels that had the most reservations", "Top 3 rooms that were the least time unavailable",
#      "Total reservation percentage by payment method", "Top 3 rooms that had the least guest-to-capacity ratio"), index=None)
#     hotel = st.text_input("hotel id")
#     if select == "Top 3 highest paid regular employee":
#         route = 'http://localhost:5000/codecrusaders/hotel/'+hotel+'/highestpaid'
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post(route, json=json_object)
#         if checkstatus(response):
#             df = pd.DataFrame.from_dict(response.json())
#             st.table(df)
#             bar_chart = alt.Chart(df).mark_bar().encode(
#                 y='salary',
#                 x='full_name',
#                 color ='full_name'
#             )
#             st.altair_chart(bar_chart, use_container_width=True)
#     elif select == "Top 5 hotel with the most client capacity":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('http://localhost:5000/codecrusaders/most/capacity', json=json_object)
#         if checkstatus(response):
#             df = pd.DataFrame.from_dict(response.json())
#             st.table(df)
#             bar_chart = alt.Chart(df).mark_bar().encode(
#                 y='total_capacity',
#                 x='hname',
#                 color = 'hname'
#             )
#             st.altair_chart(bar_chart, use_container_width=True)
#     elif select == "Top 3 month with the most reservation by chain":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('http://localhost:5000/codecrusaders/most/profitmonth', json=json_object)
#         if checkstatus(response):
#             #st.table(response.json())
#             #st.bar_chart(response.json())
#             df = pd.DataFrame.from_dict(response.json())
#             st.table(df)
#             bar_chart = alt.Chart(df).mark_bar().encode(
#                 x = 'year',
#                 y = 'total_reservations',
#                 column = 'name',
#                 color = 'month',
#             )
#             st.altair_chart(bar_chart, use_container_width=False)
#     elif select == "Top 3 rooms that were the least time unavailable":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('https://pdb-f386d9f3feff.herokuapp.com/codecrusaders/hotel/+hotel+/leastreserve', json=json_object)
#         if checkstatus(response):
#           df = pd.DataFrame(query_results, columns=['datediff', 'rid'])
#           st.write("Query Results:", df)
#           st.bar_chart(df,x="rid",y="datediff")
#     elif select == "Top 10% of the hotels that had the most reservations":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('https://pdb-f386d9f3feff.herokuapp.com/codecrusaders/most/reservation', json=json_object)
#         if checkstatus(response):
#           df = pd.DataFrame(query_results, columns=['hname', 'reservation'])
#           st.write("Query Results:", df)
#           st.bar_chart(df,x="hname",y="reservation")
#     elif select == "Total reservation percentage by payment method":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('https://pdb-f386d9f3feff.herokuapp.com/codecrusaders/paymentmethod', json=json_object)
#         if checkstatus(response):
#           df = pd.DataFrame(query_results, columns=['payment', 'percentage'])
#            fig = px.pie(df, values='percentage', names='payment')
#            st.plotly_chart(fig)
#     elif select == "Top 3 rooms that had the least guest-to-capacity ratio":
#         data = '{"username": "fmays2", "password": "mP6+bo"}'
#         json_object = json.loads(data)
#         response = requests.post('https://pdb-f386d9f3feff.herokuapp.com/codecrusaders/hotel/+hotel+/leastguests', json=json_object)
#         if checkstatus(response):
#               df = pd.DataFrame(query_results, columns=['rid', 'ratio'])
#               st.write("Query Results:", df)
#               st.scatter_chart(df,x="rid",y="ratio")
#
#
#
#
#
#
#
#


         

# # Run the main function to start the Streamlit app
if __name__ == "__main__":
    FApplication.create()
    FApplication.init()


    # frontendApplication = FApplication()

    # # Check if user is logged in
    # if "logged_in" not in st.session_state:
    #     st.session_state.logged_in = False

    # if "create_account" not in st.session_state:
    #     st.session_state.create_account = False

    # if st.session_state.create_account is True:
    #     frontendApplication.create_account()
    # elif not st.session_state.logged_in:
    # # Display login page if user is not logged in
    #     frontendApplication.login()
    # else:
    # # Display dashboard if user is logged in
    #     frontendApplication.createDashboard()