from nsepy import get_history
from datetime import date
import pandas as pd
import talib



stocks = ['ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
          'ICICIBANK', 'INDUSINDBK', 'INFY', 'IOC', 'ITC', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SHREECEM', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'ULTRACEMCO', 'UPL', 'WIPRO']
start_date = date(2022, 1, 1)
end_date = date.today()


def Importdata():
    for stock in stocks:
        rawdata = get_history(symbol=stock, start=start_date, end=end_date)
        file_name = 'Data/{}.csv'.format(stock)
        df = pd.DataFrame(rawdata)
        df.to_csv(file_name, encoding='utf-8') 
        print(stock)



def squeeze(data):

    return data['ubb'] < data['uk'] and data['lbb'] > data['lk']


def Loaddata():
    for stock in stocks:
        try:
            data = pd.read_csv('Data/{}.csv'.format(stock))
            # print(stock)
            # print(data)
            data['ubb'], data['mbb'], data['lbb'] = talib.BBANDS(data["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            data['atr'] = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=20)
            data['uk'] = talib.EMA(data['Close'], timeperiod=20) + 1.5*data['atr']
            data['lk'] = talib.EMA(data['Close'], timeperiod=20) - 1.5*data['atr']

            data['squeeze'] = data.apply(squeeze, axis=1)

            if data.iloc[-1]['squeeze']:
                print("The stocks which are in squeeze are : ",stock)
                
        except:
            pass


Loaddata()

# Importdata()
