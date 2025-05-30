import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


#Load data from S&P 500 Index and stock into dataframes
def load_data(ticker_name):
    sp500 = yf.Ticker("^GSPC").history(period="1y")["Close"]
    stock = yf.Ticker(ticker_name).history(period="1y")["Close"]

    df_sp500 = pd.DataFrame(sp500)
    df_stock = pd.DataFrame(stock)

    #Calculate the market for the S&P return for a 3 day
 
    df_sp500["Return"] = df_sp500["Close"].pct_change(periods=3)
    df_stock["Return"] = df_stock["Close"].pct_change(periods=3)

    merged_df = pd.merge(df_sp500, df_stock, left_index=True, right_index=True)

    return merged_df

def calculate_ar(merged_df, trade_date):
    merged_df["Abnormal Return"] = merged_df["Return_x"] - merged_df["Return_y"]

    if trade_date in merged_df.index:
        return merged_df.loc[trade_date, "Abnormal Return"]
    else:
        return None 

def determine_suspicion(transaction, ar):
    ABNORMAL_RETURN_THRESHOLD = 0.05
    if transaction == "PURCHASE":
        return ar > ABNORMAL_RETURN_THRESHOLD
    else:
        return ar < -ABNORMAL_RETURN_THRESHOLD


def calculate_insidertrader(merged_df, trade_date, ticker_name):
    fig, ax = plt.subplots(figsize=(15, 7))
    #Plot the lines of the SP500 and stock respectively
    ax.plot(merged_df.index, merged_df["Return_x"], label="Stock Return")
    ax.plot(merged_df.index, merged_df["Return_y"], label="S&P 500 Return")
    ax.set_title(f"3-Day Returns: {ticker_name} vs. S&P 500")
    ax.legend()

    #Marks when the politician bousght
    try: 
        converted_date= pd.to_datetime(trade_date)
        ax.axvline(converted_date, color='red', linestyle='--', label="Trade Date")
    except Exception as e:
        print(f"Ran into the error {e}")
    
    return fig

