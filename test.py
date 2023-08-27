import yfinance as yf
import pandas as pd
import numpy as np
import datetime
# import talib
moving_averages = {}

def get_avg_prices(df):
    # 計算當下的均線（月線、季線、年線）
    # 計算當下的月線
# 假設 df 是您的 DataFrame，並已經包含了 'Close' 這一列

    df['月線'] = df['Close'].rolling(window=20).mean()
    moving_averages['月線'] = "{:.2f}".format(df.at[df.index[-1], '月線'])  # 格式化為小數點後兩位

    df['季線'] = df['Close'].rolling(window=60).mean()
    moving_averages['季線'] = "{:.2f}".format(df.at[df.index[-1], '季線'])  # 格式化為小數點後兩位

    df['年線'] = df['Close'].rolling(window=240).mean()
    moving_averages['年線'] = "{:.2f}".format(df.at[df.index[-1], '年線'])  # 格式化為小數點後兩位
    # 取得當天的最新 Close 價格
    current_price = df.at[df.index[-1], 'Close']

    # 格式化現價為小數點後兩位
    formatted_current_price = "{:.2f}".format(current_price)

    moving_averages['現價'] = formatted_current_price

    if (moving_averages['月線'] > moving_averages['現價']):
        moving_averages['月線>現價'] = "+"
        moving_averages['月線'] = moving_averages['月線'] + "+"
    else:    
        moving_averages['月線>現價'] = "-"
        moving_averages['月線'] = moving_averages['月線'] + "-"

    if (moving_averages['季線'] > moving_averages['現價']):
        moving_averages['季線>現價'] = "+"
        moving_averages['季線'] = moving_averages['季線'] + "+"
    else:    
        moving_averages['季線>現價'] = "-"
        moving_averages['季線'] = moving_averages['季線'] + "-"

    if (moving_averages['年線'] > moving_averages['現價']):
        moving_averages['年線>現價'] = "+"
        moving_averages['年線'] = moving_averages['年線'] + "+"
    else:    
        moving_averages['年線>現價'] = "-"
        moving_averages['年線'] = moving_averages['年線'] + "-"


def calculate_and_get_trade_indicators(df):
    # 計算前五日的平均交易量和前 20 日的平均交易量
    df['前五日均量'] = df['Volume'].rolling(window=5).mean()
    df['前20日均量'] = df['Volume'].rolling(window=20).mean()
    
    # 判斷前五日的平均交易量是否大於前 20 日交易量，並將結果轉換為符號
    moving_averages['量MA5>20'] = f"{'+ ' if df.at[df.index[-1], '前五日均量'] > df.at[df.index[-1], '前20日均量'] else '- '}" \
                                  f"({abs(df.at[df.index[-1], '前五日均量'] - df.at[df.index[-1], '前20日均量']):.2f})"

    # 判斷連續三日的每日交易數量是否大於前五天的平均交易數量
    df['交易數量均值'] = df['Volume'].rolling(window=5).mean()
    df['連續三日交易大於均值'] = (df['Volume'].shift(1) > df['交易數量均值'].shift(1)) & \
                               (df['Volume'].shift(2) > df['交易數量均值'].shift(2)) & \
                               (df['Volume'] > df['交易數量均值']) 
    # 將布林列轉換為符號 "+" 或 "-"
    df['連續三日交易大於均值'] = df['連續三日交易大於均值'].apply(lambda x: '+' if x else '-')
    moving_averages['連3日>MA5'] = df['連續三日交易大於均值'].iloc[-1]

def calculate_daily_macd(df):
    # 计算12日EMA
    print("----------日MACD----------")
    df['12日EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
    print("12日EMA", "{:.2f}".format(df['12日EMA'].iloc[-1]))
    # 计算26日EMA
    df['26日EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
    print("26日EMA", "{:.2f}".format(df['26日EMA'].iloc[-1]))
    # 计算DIF（差异）
    df['DIF'] = df['12日EMA'] - df['26日EMA']
    print("DIF", "{:.2f}".format(df['DIF'].iloc[-1]))
    # 计算9日DIF的EMA，即MACD
    df['MACD'] = df['DIF'].ewm(span=9, adjust=False).mean()
    print("MACD", "{:.2f}".format(df['MACD'].iloc[-1]))

    df['OSC'] = df['DIF'] - df['MACD']
    print("OSC", "{:.2f}".format(df['OSC'].iloc[-1]))

    daily_MACD = df['MACD'].iloc[-1]
    moving_averages['daily_MACD'] = "{:.2f}".format(daily_MACD)

    daily_OSC = df['OSC'].iloc[-1]
    moving_averages['daily_OSC'] = "{:.2f}".format(daily_OSC)

def calculate_weekly_macd():
    # 使用 yf.download 函式獲取週歷史股價數據

    df = yf.download(stock_symbol, interval='1wk')
    # 計算12週EMA
    print("----------週MACD----------")
    df['12週EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
    print("12週EMA", "{:.2f}".format(df['12週EMA'].iloc[-1]))
    # 計算26週EMA
    df['26週EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
    print("26週EMA", "{:.2f}".format(df['26週EMA'].iloc[-1]))
    # 計算DIF
    df['weekly_DIF'] = df['12週EMA'] - df['26週EMA']
    print("weekly_DIF", "{:.2f}".format(df['weekly_DIF'].iloc[-1]))
    # 計算9週DIF的EMA，即MACD
    df['weekly_MACD'] = df['weekly_DIF'].ewm(span=9, adjust=False).mean()
    print("weekly_MACD", "{:.2f}".format(df['weekly_MACD'].iloc[-1]))
    # 取得最後一筆週MACD數值
    last_weekly_macd = df['weekly_MACD'].iloc[-1]
    moving_averages['weekly_MACD'] = "{:.2f}".format(last_weekly_macd)

    df['weekly_OSC'] = df['weekly_DIF'] - df['weekly_MACD']
    moving_averages['weekly_OSC'] = "{:.2f}".format(df['weekly_OSC'].iloc[-1])

    # weekly_OSC = df['weekly_OSC'].iloc[-1]
    # moving_averages['weekly_OSC'] = "{:.2f}".format(weekly_OSC)

def calculate_RSI14(df):
    # 計算價格變動
    df['Price Change'] = df['Close'].diff()

    # 計算上漲幅度和下跌幅度
    df['Gain'] = np.where(df['Price Change'] > 0, df['Price Change'], 0)
    df['Loss'] = np.where(df['Price Change'] < 0, -df['Price Change'], 0)

    # 計算相對強度（RS）
    window = 14  # RSI14的計算窗口
    avg_gain = df['Gain'].rolling(window=window).mean()
    avg_loss = df['Loss'].rolling(window=window).mean()
    df['RS'] = avg_gain / avg_loss

    df['daily_RSI14'] = 100 - (100 / (1 + df['RS']))

    # 只取最新一筆資料的日 RSI14 值
    latest_rsi = "{:.2f}".format(df['daily_RSI14'].iloc[-1])
    moving_averages['daily_RSI14'] = latest_rsi


def calculate_weekly_RSI14():
    df = yf.download(stock_symbol, interval='1wk')
    # 計算價格變動
    df['Price Change'] = df['Close'].diff()

    # 計算上漲幅度和下跌幅度
    df['Gain'] = np.where(df['Price Change'] > 0, df['Price Change'], 0)
    df['Loss'] = np.where(df['Price Change'] < 0, -df['Price Change'], 0)

    # 計算相對強度（RS）
    window = 14  # RSI14的計算窗口
    avg_gain = df['Gain'].rolling(window=window).mean()
    avg_loss = df['Loss'].rolling(window=window).mean()
    df['RS'] = avg_gain / avg_loss

    df['weekly_RSI14'] = 100 - (100 / (1 + df['RS']))

    # 只取最新一筆資料的週 RSI14 值
    latest_rsi = "{:.2f}".format(df['weekly_RSI14'].iloc[-1])
    print("weekly_RSI14", latest_rsi)
    moving_averages['weekly_RSI14'] = latest_rsi

# 假設你有一個包含股票價格數據的 DataFrame，名稱為 stock_data



# Calculate the RSI
# def calculate_rsi(df, period=14):
#     delta = df['Close'].diff()
#     gain = (delta.where(delta > 0, 0)).fillna(0)
#     loss = (-delta.where(delta < 0, 0)).fillna(0)

#     avg_gain = gain.rolling(window=period).mean()
#     avg_loss = loss.rolling(window=period).mean()

#     relative_strength = avg_gain / avg_loss
#     rsi = 100 - (100 / (1 + relative_strength))
    
#     return rsi



# Calculate the OSC
# def calculate_osc(df, short_period=9, long_period=14):
#     short_rsi = df['RSI'].rolling(window=short_period).mean()
#     long_rsi = df['RSI'].rolling(window=long_period).mean()
    
#     osc = (short_rsi - long_rsi).iloc[-1]
#     print("osc:",osc)
#     return osc

# 獲取並顯示0056.TW的股票資訊
stock_symbol = "0056.TW"
# 使用 yf.download 函式獲取歷史股價數據
df = yf.download(stock_symbol)
get_avg_prices(df)
calculate_and_get_trade_indicators(df)
calculate_daily_macd(df)
calculate_weekly_macd()
calculate_RSI14(df)
calculate_weekly_RSI14()
# df['RSI'] = calculate_rsi(df)
# df['OSC'] = calculate_osc(df)
print(moving_averages)

# 获取0056.TW的股票对象
stock = yf.Ticker("0056.TW")

# 获取历史交易数据
history = stock.history(period="1d")

# 计算买入和卖出数量差
buy_quantity = history['Volume'][history['Close'] > history['Open']].sum()
sell_quantity = history['Volume'][history['Close'] < history['Open']].sum()

difference = buy_quantity - sell_quantity

print(f"买入张数：{buy_quantity}")
print(f"卖出张数：{sell_quantity}")
print(f"买入和卖出张数差：{difference}")