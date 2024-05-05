import streamlit as st

from views.LocalStats import LocalStats
from views.GlobalStats import GlobalStats
from views.AdminDataBaseAccess import AdminDataBaseAccess

class Dashboard:

    admin_tabs = [
        "Local Statistics",
        "Global Statistics",
        "Create Reservation",
        "Access Database"
    ]
    normal_tabs = [
        "Local Statistics",
    ]

    def __init__(self, position):
        self.position = position
        self.local_stat = LocalStats()
        self.global_stat = GlobalStats()
        self.admin_database_access = AdminDataBaseAccess()

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
            self.local_stat.create_as_admin()
        elif self.tab == "Global Statistics":
            self.global_stat.create_stats()
        elif self.tab == "Access Database":
            self.admin_database_access.create()

    def create_Supervisor(self):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_as_supervisor()

    def create_Regular(self):
        self.tab = st.sidebar.radio("Navigation", self.normal_tabs)
        self.local_stat.create_as_regular()