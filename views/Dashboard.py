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

    def __init__(self, position, hid):
        self.position = position
        self.local_stat = LocalStats()
        self.global_stat = GlobalStats()

        st.sidebar.title('Hotel Selection')
        
        #self.tabs = st.sidebar.radio("Navigation", self.accessible_tabs)
        if position == 'Administrator':
            self.tab = st.sidebar.radio("Navigation", self.admin_tabs)
            self.create_Administrator(hid)
        elif position == 'Supervisor':
            self.create_Supervisor(hid)
        elif position == 'Regular':
            self.create_Regular(hid)
        pass
    def create_Administrator(self, hid):
        #self.tab = st.sidebar.radio("Navigation", self.admin_tabs)
        #self.local_stat.create_stats()
        #self.global_stat.create_stats()
        if self.tab == "Local Statistics":
            self.local_stat.create_stats(hid)
            st.write("This is Tab 1 Administrator")
        elif self.tab == "Global Statistics":
            self.global_stat.create_stats()
            st.write("This is Tab 2 Administrator")
        pass

    def create_Supervisor(self,hid):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_stats(hid)
        st.write("This is Tab 1 Administrator")
        # if self.tabs == "Tab 1":
        #     st.write("This is Tab 1 Supervisor")
        # elif self.tabs == "Tab 3":
        #     st.write("This is Tab 3 Supervisor")
        # pass

    def create_Regular(self,hid):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_stats(hid)
        st.write("This is Tab 1 Administrator")
        # if self.tabs == "Tab 1":
        #     st.write("This is Tab 1 Regular")
        # pass