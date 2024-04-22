import streamlit as st

class Dashboard:

    def __init__(self, position):
        self.position = position

        self.tabs = st.sidebar.radio("Navigation", ["Tab 1", "Tab 2", "Tab 3"])

        if position == 'Administrator':
            self.create_Administrator()
        elif position == 'Supervisor':
            self.create_Supervisor()
        elif position == 'Regular':
            self.create_Regular()
        pass

    def create_Administrator(self):
        if self.tabs == "Tab 1":
            st.write("This is Tab 1 Administrator")
        elif self.tabs == "Tab 2":
            st.write("This is Tab 2 Administrator")
        elif self.tabs == "Tab 3":
            st.write("This is Tab 3 Administrator")
        pass

    def create_Supervisor(self):
        if self.tabs == "Tab 1":
            st.write("This is Tab 1 Supervisor")
        elif self.tabs == "Tab 3":
            st.write("This is Tab 3 Supervisor")
        pass

    def create_Regular(self):
        if self.tabs == "Tab 1":
            st.write("This is Tab 1 Regular")
        pass