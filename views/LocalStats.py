import streamlit as st
import requests
import pandas as pd
import altair as alt
import plotly.express as px

from views.Login import Login

class LocalStats:

    option_stats = [
        "Top 5 handicap rooms that were reserve the most",
        "Top 3 rooms that were the least time unavailable",
        "Top 5 clients under 30 that made the most reservation with a credit",
        "Top 3 highest paid regular employees.",
        "Top 5 clients that received the most discounts",
        "Total reservation by room type.",
        "Top 3 rooms that were reserved that had the least guest-to-capacity ratio."
    ]

    def __init__(self):
        self.login = st.session_state.fapp_singleton.loginHandle
        self.mainRoute = st.session_state.fapp_singleton.mainRoute
    
    def create_as_admin(self):

        st.write(f'# Local Statistics for Hotel')

        response = requests.get(f'{self.mainRoute}hotel')
        self.allHotels = response.json()

        self.hotelID = -1
        hotel_selected = st.selectbox('Select Hotel', self.login.getHotels(self.allHotels), index=None)
        self.hotelID = self.login.getHotelID(hotel_selected, self.allHotels)

        self.create()

    def create_as_supervisor(self):

        chain_response = requests.get(f'{self.mainRoute}chains')
        chain_data = self.login.getChainData(self.login.chainID, chain_response.json())

        response = requests.get(f'{self.mainRoute}hotel')
        hotel_list_json = self.login.getAllHotelsFromChain(self.login.chainID, response.json())
        hotel_list = self.login.getHotels(hotel_list_json)
        
        st.write(f'# Local Statistics for Hotel')
        if chain_data is not None:
            chain_name = chain_data['cname']
            st.write(f'## under chain {chain_name}')
             
        hotel_selected = st.selectbox(f'Select Hotel', hotel_list, index=None)

        self.hotelID = -1
        self.hotelID = self.login.getHotelID(hotel_selected, hotel_list_json)

        self.create()

    def create_as_regular(self):
        response = requests.get(f'{self.mainRoute}hotel')
        self.hotelID = self.login.hotelID
        hotel_data = self.login.getHotelData(self.hotelID, response.json())['hname']

        st.write(f'# Local Statistics for Hotel')
        st.write(f'## Working on {hotel_data}')

        self.create()

    def create(self):
        response = requests.get(f'{self.mainRoute}hotel/{self.hotelID}')
        if response.status_code != 200:
            stat_selected = st.selectbox("Choose Local Statistic", self.option_stats, index=None, disabled=True)
            return
        else:
            stat_selected = st.selectbox("Choose Local Statistic", self.option_stats, index=None)

        if stat_selected == self.option_stats[0]:
            self.stat_Handicaproom()
        elif stat_selected == self.option_stats[1]:
            self.stat_LeastReserve()
        elif stat_selected == self.option_stats[2]:
            self.stat_MostCreditCard()
        elif stat_selected == self.option_stats[3]:
            self.stat_HighestPaid()
        elif stat_selected == self.option_stats[4]:
            self.stat_MostDiscount()
        elif stat_selected == self.option_stats[5]:
            self.stat_RoomType()
        elif stat_selected == self.option_stats[6]:
            self.stat_LeastGuests()

    def isValidResponse(self, response):
        if response.status_code == 200:
            return True
        else:
            return st.error(f"Failed to retrieve data. Status code: {response.status_code}")

    #Top 5 handicap rooms that were reserve the most
    def stat_Handicaproom(self):
        response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/handicaproom', json=self.login.getLoginJson())
        if not self.isValidResponse(response):
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
    def stat_LeastReserve(self):
            response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/leastreserve', json=self.login.getLoginJson())
            if not self.isValidResponse(response):
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
    def stat_MostCreditCard(self):
        response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/mostcreditcard', json=self.login.getLoginJson())
        if not self.isValidResponse(response):
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
    def stat_HighestPaid(self):
        response = requests.post(f'{self.mainRoute}/hotel/{self.hotelID}/highestpaid', json=self.login.getLoginJson())
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
    def stat_MostDiscount(self):
        response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/mostdiscount', json=self.login.getLoginJson())
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
    def stat_RoomType(self):
        response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/roomtype', json=self.login.getLoginJson())
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
    def stat_LeastGuests(self):
        response = requests.post(f'{self.mainRoute}hotel/{self.hotelID}/leastguests', json=self.login.getLoginJson())
        if not self.isValidResponse(response):
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