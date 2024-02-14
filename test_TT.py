import yfinance as yf
from datetime import datetime, timedelta

# 獲取今天的日期
today = datetime.today()

# 格式化今天的日期作為結束日期
end_date = today.strftime('%Y-%m-%d')

# 假設想要往回推的時間為過去5年
start_date = (today - timedelta(days=5*365)).strftime('%Y-%m-%d')

# 下載台灣加權指數的月線資料
monthly_data = yf.download("^TWII", start=start_date, end=end_date, interval="1mo")

# 下載台灣加權指數的季線資料
quarterly_data = yf.download("^TWII", start=start_date, end=end_date, interval="3mo")

# 下載台灣加權指數的年線資料
annual_data = yf.download("^TWII", start=start_date, end=end_date, interval="1y")

# 顯示月線資料
print("Monthly Data:")
print(monthly_data)

# 顯示季線資料
print("\nQuarterly Data:")
print(quarterly_data)

# 顯示年線資料
print("\nAnnual Data:")
print(annual_data)

