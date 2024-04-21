import streamlit as st
import requests
import json
import pandas as pd
import altair as alt
# check if data is received


def checkstatus(tocheck):
    if tocheck.status_code == 200:
        return True
    else:
        return st.error(f"Failed to retrieve data. Status code: {tocheck.status_code}")


def main():

    select = st.selectbox("Choose Statistic", ("Top 3 highest paid regular employee", "Top 5 hotel with the most client capacity", "Top 3 month with the most reservation by chain"), index=None)
    hotel = st.text_input("hotel id")
    if select == "Top 3 highest paid regular employee":
        route = 'http://localhost:5000/codecrusaders/hotel/'+hotel+'/highestpaid'
        data = '{"username": "fmays2", "password": "mP6+bo"}'
        json_object = json.loads(data)
        response = requests.post(route, json=json_object)
        if checkstatus(response):
            df = pd.DataFrame.from_dict(response.json())
            st.table(df)
            bar_chart = alt.Chart(df).mark_bar().encode(
                y='salary',
                x='full_name',
                color ='full_name'
            )
            st.altair_chart(bar_chart, use_container_width=True)
    elif select == "Top 5 hotel with the most client capacity":
        data = '{"username": "fmays2", "password": "mP6+bo"}'
        json_object = json.loads(data)
        response = requests.post('http://localhost:5000/codecrusaders/most/capacity', json=json_object)
        if checkstatus(response):
            df = pd.DataFrame.from_dict(response.json())
            st.table(df)
            bar_chart = alt.Chart(df).mark_bar().encode(
                y='total_capacity',
                x='hname',
                color = 'hname'
            )
            st.altair_chart(bar_chart, use_container_width=True)
    elif select == "Top 3 month with the most reservation by chain":
        data = '{"username": "fmays2", "password": "mP6+bo"}'
        json_object = json.loads(data)
        response = requests.post('http://localhost:5000/codecrusaders/most/profitmonth', json=json_object)
        if checkstatus(response):
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

# Run the main function to start the Streamlit app
if __name__ == "__main__":
    main()