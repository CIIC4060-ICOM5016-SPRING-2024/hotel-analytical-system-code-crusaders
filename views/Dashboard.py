import streamlit as st

from views.LocalStats import LocalStats
from views.GlobalStats import GlobalStats

class Dashboard:

    admin_tabs = [
        "Local Statistics",
        "Global Statistics",
        "Create Reservation"
    ]
    normal_tabs = [
        "Local Statistics",
    ]

    def __init__(self, position):
        self.position = position
        self.local_stat = LocalStats()
        self.global_stat = GlobalStats()

        st.sidebar.title('Hotel-Application Selection')
        
        if position == 'Administrator':
            self.create_Administrator()
        elif position == 'Supervisor':
            self.create_Supervisor()
        elif position == 'Regular':
            self.create_Regular()
        pass
    def create_Administrator(self):
        self.tab = st.sidebar.radio("Navigation", self.admin_tabs)

        if self.tab == "Local Statistics":
            self.local_stat.create_stats_Admin()
        elif self.tab == "Global Statistics":
            self.global_stat.create_stats()

    def create_Supervisor(self):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_stats_Supervisor()

    def create_Regular(self):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_stats_Regular()