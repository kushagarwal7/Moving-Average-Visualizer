from flask import Flask, render_template, request
import pandas as pd
import quandl

quandl.ApiConfig.api_key = 'zC992yeEkw5VTye5PFJY'
application = Flask(__name__)

#global variables 
ticker_names = ["AAPL", "GOOG", "MSFT", "TSLA", "FB"]
window_size_1 = 20
window_size_2 = 40
window_size_3 = 60

@application.route("/", methods=['GET'])
def renderChart():
    current_ticker = request.args.get("ticker_name")
    if current_ticker == None:
        current_ticker = "AAPL"
    df = getStockData(current_ticker)
    dates = []
    values = []

    for date in df['Date']:
        dates.append(date.date())
    for price in df['Adj. Close']:
        values.append(price)

    # Moving Average computations    
    moving_ave_20 = df['Adj. Close'].rolling(window=window_size_1).mean()
    moving_ave_40 = df['Adj. Close'].rolling(window=window_size_2).mean()
    moving_ave_60 = df['Adj. Close'].rolling(window=window_size_3).mean()

    return render_template('index.html', values = values, labels = dates, current_ticker = current_ticker, ticker_names = ticker_names, moving_ave_20 = moving_ave_20, moving_ave_40 = moving_ave_40, moving_ave_60 = moving_ave_60, window_size_1= window_size_1, window_size_2= window_size_2, window_size_3= window_size_3)


def getStockData (ticker):
    df = quandl.get('WIKI/' + ticker +'.11', start_date="2016-12-31", end_date="2018-03-27")
    df.reset_index(level=0, inplace=True)
    return df


if __name__ == "__main__":
    application.run()