import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import requests
from bs4 import BeautifulSoup
import re
# import talib
import os
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
moving_averages = {}
excel_data = {}
def Institutional_net_buy(stock_symbol):
    # 定义目标网页链接
    url = f"https://tw.stock.yahoo.com/quote/{stock_symbol}/broker-trading"
    print(url)
    response = requests.get(url, headers=headers)


    # 发送HTTP请求并获取页面内容
    html_content = response.content

    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(html_content, "html.parser")
    # 查找具有特定类名的元素
    target_elements = soup.select("div.Fz\(24px\).Fz\(18px\)--mobile.Fw\(600\).H\(28px\).H\(a\)--mobile.Mt\(4px\)[class*='c-trend']")
    print("target_elements", target_elements)
    if target_elements:
        content = target_elements[0].get_text()
        moving_averages['日主力'] = content
    else:
        moving_averages['日主力'] = "未找到目标元素"

def Foreign_institutional_net_BuySell(stock_symbol):
    URL = f"https://tw.stock.yahoo.com/quote/{stock_symbol}/institutional-trading"
    print (URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  # 設置一個User-Agent，避免被網站阻擋

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        target_divs = soup.find_all('div', class_='Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc')
        
        if target_divs:
            count = 0
            for target_div in target_divs:
                count += 1
                span_data = target_div.find('span', class_='Jc(fe)')
                if span_data:
                    if count == 28:
                        WeeklyForeignInstitutionalInvestors = span_data.text
    else:
        print(f"網頁回應錯誤，HTTP 狀態碼: {response.status_code}")

    moving_averages['周外資'] = WeeklyForeignInstitutionalInvestors

def seventyTwoDay_moving_average(stock_symbol):
    symbol_before_dot = stock_symbol.split(".")[0]
    URL = f"https://fubon-ebrokerdj.fbs.com.tw/Z/ZC/ZCW/ZCWG/ZCWG_{symbol_before_dot}_72.djhtm"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # 從所有的<script>標籤中搜尋GetBcdData的呼叫
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string:
            matches = re.search(r'GetBcdData\(\'(.*?)\'\)', script.string)
            if matches:
                data = matches.group(1)
                # 使用空格分割數據
                part1, part2 = data.split(' ')

    numbers_part2 = [int(n) for n in part2.split(",")]

    # 使用sum函數計算總和
    total = sum(numbers_part2)
    tenp = total * 0.1
    # 从第一个数开始减去temp
    for i, num in enumerate(numbers_part2):
        tenp -= num
        if tenp <= 0:  # 当temp小于或等于0时，记录索引并退出循环
            index = i
            break
    numbers_part1 = [float(n) for n in part1.split(",")]
    lower = numbers_part1[index]
    moving_averages['72分下'] = lower
    numbers_part2_reversed = numbers_part2[::-1]  # 反转数列
    tenp = total * 0.1

    # 从最后一个数开始减去temp
    for i, num in enumerate(numbers_part2_reversed):
        tenp -= num
        if tenp <= 0:
            index_reversed = i
            break

    numbers_part1_reversed = numbers_part1[::-1]
    upper = numbers_part1_reversed[index_reversed]
    moving_averages['72分上'] = upper


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

def calculate_weekly_macd(stock_symbol):
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


def calculate_weekly_RSI14(stock_symbol):
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

def trend_line(moving_averages):
    def get_trend(value):
        # Try to convert the value to float, if fails, return '-'
        if value == '-':
            return '-'
        elif value == '+':
            return '+'
        try:
            print("value", value)
            float_val = float(value.replace(',', '').split(' ')[0])
            print("float_val", float_val)
            return '+' if float_val > 0 else '-'
        except:
            return '-'

    columns_to_check = ['日主力', '周外資','月線>現價', '季線>現價', '年線>現價', '量MA5>20', '連3日>MA5', 'daily_MACD', 'daily_RSI14', 'weekly_MACD', 'weekly_RSI14']

    combined_trend = ''.join([get_trend(moving_averages[col]) for col in columns_to_check])
    print("combined_trend", combined_trend)
    ##寫到這裡******* 'daily_MACD', 'daily_RSI14', 'weekly_MACD', 'weekly_RSI14' 要看正負，把趨勢寫入excel 
    moving_averages['趨勢'] = combined_trend
    positive_count = combined_trend.count('+')
    negative_count = combined_trend.count('-')
    moving_averages['正加總'] = positive_count
    moving_averages['負加總'] = negative_count

def save_to_excel(excel_data):
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(excel_data).T
    
    # Desired column order
    desired_order = ['日主力', '周外資', '72分上', '72分下', '月線', '季線', '年線', '量MA5>20', '連3日>MA5', 'daily_MACD', 'daily_RSI14', 'weekly_MACD', 'weekly_RSI14','趨勢','正加總','負加總']
    
    # Rearrange columns based on desired order
    df = df[desired_order]
    
    # Get the current directory of the .exe or script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the absolute path
    file_path = os.path.join(current_dir, "output.xlsx")
    
    # Save to Excel
    df.to_excel(file_path, engine='openpyxl')
    print(f"Saved to {file_path}")

def run_func(stock_symbols):
    # 獲取並顯示0056.TW的股票資訊
    print("print",stock_symbols)
    for stock_symbol in stock_symbols:
        moving_averages.clear()
    # 使用 yf.download 函式獲取歷史股價數據
        stock_symbol = stock_symbol + ".TW"
        print(stock_symbol)
        df = yf.download(stock_symbol)
        get_avg_prices(df)
        calculate_and_get_trade_indicators(df)
        calculate_daily_macd(df)
        print("----------日MACD----------")
        calculate_weekly_macd(stock_symbol)
        print("----------日RSI14----------")
        calculate_RSI14(df)
        print("----------週RSI14----------")
        calculate_weekly_RSI14(stock_symbol)
        Institutional_net_buy(stock_symbol)
        Foreign_institutional_net_BuySell(stock_symbol)
        seventyTwoDay_moving_average(stock_symbol)
        trend_line(moving_averages)
        excel_data[stock_symbol] = moving_averages.copy()
        print("moving_averages", moving_averages)
    save_to_excel(excel_data)