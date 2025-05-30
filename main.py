import streamlit as st
import sqlite3
import re
from yf_scrapper import load_data, calculate_ar, calculate_insidertrader, determine_suspicion
from datetime import datetime

#Connect to SQL database
connection = sqlite3.connect("congressional_trades.db")
cursor = connection.cursor()


#Get distinct politician names, removing duplicates
cursor.execute("SELECT DISTINCT politician_name FROM trades")

    
st.title("Recent Congressional Market Movers")

st.subheader("Please select a politician from the dropdown menu:")

option = st.selectbox(
    label = "Choose a politician",
    options = [row[0] for row in cursor.fetchall()]
)

cursor.execute(f"SELECT * FROM trades WHERE politician_name = ?", (option,))
politician_trades = cursor.fetchall()
try:
    for trade in politician_trades:
        stock_name = trade[0]
        date = trade[3]

        data = load_data(stock_name)
        ar = calculate_ar(data, date)
        figure = calculate_insidertrader(data, date, stock_name)
        transaction = "SALE" if trade[1].startswith("S") else "PURCHASE"

        st.pyplot(figure)
        if determine_suspicion(transaction, ar):
            st.write(f"The return was {ar:.2%} and is potentially made with insider trading.")
        else:
            st.write(f"The return was {ar:.2%} and is potentially made with no insider trading.")
        
        date_object = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%m/%d/%Y")
        

        st.write(f"{option} made a {transaction} of {stock_name} on {formatted_date}")
        st.markdown("---")
except TypeError as e:
    st.write("This stock data is currently unavaliable")


connection.commit()
