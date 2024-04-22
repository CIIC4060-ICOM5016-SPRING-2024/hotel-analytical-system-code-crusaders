import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
import plotly as px

SERVER = "heroku"

class FApplication:

    # User credentials
    userLogged = None
    userPassword = None

    # Employee info
    chainID = None
    position = None
    employeeID = None

    # Flask route
    mainRoute = None

    signInSession_loggedin = False

    def __init__(self):
        if SERVER == "heroku":
            self.mainRoute = 'https://pdb-frontend-6b009c60f251.herokuapp.com/'
        else:
            self.mainRoute = 'http://localhost:5000/'
        pass

    def sign_in(self):
        st.title('Sign-in')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        user_signed_in = st.button('Sign-in')

        if user_signed_in:
            response = requests.post(f'{self.mainRoute}login', json = {'username': username, 'password': password})

            print(response)

            if response.status_code == 200:
                user_details = response.json()
                print(user_details)
                # st.success(f'Welcome, {user_details["username"]}!')
                # Redirect to main app or show other content...
            else:
                st.error('Invalid credentials')
        pass

# check if data is received
# def checkstatus(tocheck):
#     if tocheck.status_code == 200:
#         return True
#     else:
#         return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")


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
    frontendApplication = FApplication()

    frontendApplication.sign_in()