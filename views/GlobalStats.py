import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
import plotly.express as px

class GlobalStats:

    option_stats = (
        "Top 3 chains with the highest total revenue.",
        "Total reservation percentage by payment method",
        "Top 3 chain with the least rooms.",
        "Top 5 hotels with the most capacity.",
        "Top 10% hotels that had the most reservations.",
        "Top 3 month with the most reservation by chain"
    )

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute

    def create_stats(self):
        select = st.selectbox("Choose Global Statistic", self.option_stats, index=None)

        if select == self.option_stats[0]:
            self.gstat_MostRevenue()
        elif select == self.option_stats[1]:
            self.gstat_PaymentMethod()
        elif select == self.option_stats[2]:
            self.gstat_LeastRooms()
        elif select == self.option_stats[3]:
            self.gstat_MostCapacity()
        elif select == self.option_stats[4]:
            self.gstat_MostReservation()
        elif select == self.option_stats[5]:
            self.gstat_MostProfitMonth()

    def isValidResponse(self, response):
        if response.status_code == 200:
            return True
        else:
            return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")

    #Top 3 chains with the highest total revenue.
    def gstat_MostRevenue(self):
        pass

    #Total reservation percentage by payment method
    def gstat_PaymentMethod(self):
        response = requests.post(f'{self.mainRoute}paymentmethod', json=self.login.getLoginJson())
        if self.checkstatus(response):
            df = pd.DataFrame(response.json(), columns=['payment', 'percentage'])
            fig = px.pie(df, values='percentage', names='payment')
            st.plotly_chart(fig)

    #Top 3 chain with the least rooms.
    def gstat_LeastRooms(self):
        pass
    
    #Top 5 hotels with the most capacity.
    def gstat_MostCapacity(self):
        response = requests.post(f'{self.mainRoute}most/capacity', json=self.login.getLoginJson())
        if not self.isValidResponse(response):
            return

        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            y='total_capacity',
            x='hname',
            color = 'hname'
        )
        st.altair_chart(bar_chart, use_container_width=True) 

    #Top 10% hotels that had the most reservations.
    def gstat_MostReservation(self):
        response = requests.post(f'{self.mainRoute}most/reservation', json=self.login.getLoginJson())
        if not self.checkstatus(response):
            return
        df = pd.DataFrame(response.json(), columns=['hname', 'reservations'])
        st.write("Query Results:", df)
        st.bar_chart(df,x="hname",y="reservations")

    #Top 3 month with the most reservation by chain
    def gstat_MostProfitMonth(self):
        response = requests.post(f'{self.mainRoute}most/profitmonth', json=self.login.getLoginJson())
        if not self.checkstatus(response):
            return

        #st.table(response.json())
        #st.bar_chart(response.json())
        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            x = 'year',
            y = 'total_reservations',
            column = 'name',
            color = 'month',
        )
        st.altair_chart(bar_chart, use_container_width=False)