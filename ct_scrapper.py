from bs4 import BeautifulSoup
import requests
import sqlite3
import re

#Connect to SQL database
connection = sqlite3.connect("congressional_trades.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    ticker_name TEXT,
    transaction_type TEXT,
    politician_name TEXT,
    traded_date TEXT
)""")
connection.commit() 


headers = {'User-Agent': 'Mozilla/5.0' }
all_trades = []
month_map = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

#Get a response from the Quiverquant server
url = f"https://www.quiverquant.com/congresstrading/"
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, features="lxml")


try: 
#Extract the stock name, transaction, politician, traded times 
    rows = soup.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 5:
            ticker = columns[0].get_text().split(' ')[0].strip()
            transaction = columns[1].get_text(strip=True)
            politician =re.sub("(House|Senate)", "", columns[2].get_text(strip=True))[:-3].strip()
            traded_date = columns[4].get_text(strip=True)

            #Filter trade components and append the trade to all trades
            if ticker and transaction and traded_date:
                try:
                    date_parts = traded_date.replace(".","").replace(",", "").split()
                    year = date_parts[2]
                    month = month_map[date_parts[0]]
                    day = date_parts[1].zfill(2)

                    date = f"{year}-{month}-{day}"

                except (KeyError, IndexError) as e:
                    print(f"An error has occured with the date parsing: {e}")
                #Add trade to SQL db
                cursor.execute("INSERT INTO trades (ticker_name, transaction_type, politician_name, traded_date) VALUES (?, ?, ?, ?)",
                               (ticker, transaction, politician, date))
                connection.commit()            
    
    
except Exception as e:
    print(f"Something has gone wrong! {e}")





                


