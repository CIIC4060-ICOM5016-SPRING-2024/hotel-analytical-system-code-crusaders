import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
import plotly.express as px

from views.Login import Login

class LocalStats:

    option_stats = (
        "Top 5 handicap rooms that were reserve the most",
        "Top 3 rooms that were the least time unavailable",
        "Top 5 clients under 30 that made the most reservation with a credit",
        "Top 3 highest paid regular employees.",
        "Top 5 clients that received the most discounts",
        "Total reservation by room type.",
        "Top 3 rooms that were reserved that had the least guest-to-capacity ratio."
    )

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute
    def checkstatus(self, tocheck):
        if tocheck.status_code == 200:
            return True
        else:
            return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")
    def create_stats(self,hid):
        select = st.selectbox("Choose Local Statistic", self.option_stats, index=None)

        if select == self.option_stats[0]:
            self.stat_Handicaproom(hid)
        elif select == self.option_stats[1]:
            self.stat_LeastReserve(hid)
        elif select == self.option_stats[2]:
            self.stat_MostCreditCard(hid)
        elif select == self.option_stats[3]:
            self.stat_HighestPaid(hid)
        elif select == self.option_stats[4]:
            self.stat_MostDiscount(hid)
        elif select == self.option_stats[5]:
            self.stat_RoomType(hid)
        elif select == self.option_stats[6]:
            self.stat_LeastGuests(hid)

    def isValidResponse(self, response):
        if response.status_code == 200:
            return True
        else:
            return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")

    #Top 5 handicap rooms that were reserve the most
    def stat_Handicaproom(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/handicaproom"
        response = requests.post(route, json=self.login.getLoginJson())

        if not self.checkstatus(response):
            return
        df = pd.DataFrame(response.json())
        chart = alt.Chart(df).mark_bar().encode(
            x='rname',
            y='reservation_count',
            color='rtype'
        ).properties(
            width=600,
            height=400,
            title='Reservation Count by Hotel'
        ).interactive()
        st.write(chart)

    #Top 3 rooms that were the least time unavailable
    def stat_LeastReserve(self,hid):
            route = self.mainRoute + "hotel/" + str(hid) + "/leastreserve"
            response = requests.post(route, json=self.login.getLoginJson())
            
            if not self.checkstatus(response):
                return
            df = pd.DataFrame.from_dict(response.json())
            st.table(df)
            bar_chart = alt.Chart(df).mark_bar().encode(
                y='datediff',
                x='rid',
                color='rid'
            )
            st.altair_chart(bar_chart, use_container_width=True)

    #Top 5 clients under 30 that made the most reservation with a credit
    def stat_MostCreditCard(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/mostcreditcard"
        response = requests.post(route, json=self.login.getLoginJson())

        if not self.checkstatus(response):
            return
        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            y='count_reservation',
            x='full_name',
            color='full_name'
        )
        st.altair_chart(bar_chart, use_container_width=True)

        #Top 3 highest paid regular employees.
    def stat_HighestPaid(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/highestpaid"
        response = requests.post(route, json=self.login.getLoginJson())

        if not self.isValidResponse(response):
            return

        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            y='salary',
            x='full_name',
            color ='full_name'
        )
        st.altair_chart(bar_chart, use_container_width=True)

    #Top 5 clients that received the most discounts
    def stat_MostDiscount(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/mostdiscount"
        response = requests.post(route, json=self.login.getLoginJson())

        if not self.isValidResponse(response):
            return

        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            y='discount',
            x='full_name',
            color='full_name'
        )
        st.altair_chart(bar_chart, use_container_width=True)

    #Total reservation by room type.
    def stat_RoomType(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/roomtype"
        response = requests.post(route, json=self.login.getLoginJson())

        if not self.isValidResponse(response):
            return

        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        bar_chart = alt.Chart(df).mark_bar().encode(
            y='reservations_total',
            x='rtype',
            color='rtype'
        )
        st.altair_chart(bar_chart, use_container_width=True)

    #Top 3 rooms that were reserved that had the least guest-to-capacity ratio.
    def stat_LeastGuests(self,hid):
        route = self.mainRoute + "hotel/" + str(hid) + "/leastguests"
        response = requests.post(route, json=self.login.getLoginJson())
        if not self.checkstatus(response):
            return
        df = pd.DataFrame.from_dict(response.json())
        st.table(df)
        scatter_plot = alt.Chart(df).mark_circle().encode(
            x='rid',
            y='ratio',
            color='rid'
        ).properties(
            width=600,
            height=400,
            title='Scatter Plot of ratio vs rid'
        ).interactive()
        st.altair_chart(scatter_plot, use_container_width=True)