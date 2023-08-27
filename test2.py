import requests
from bs4 import BeautifulSoup 

response = requests.get("https://www.cmoney.tw/finance/0056/technicalanalysis") #將此頁面的HTML GET下來
soup = BeautifulSoup(response.content, "html.parser")
# 查找包含MACD数据的元素
macd_element = soup.find("span", class_="fa fa-minus linelegend")
result = soup.find_all(["i", "p"], limit=2,string="fa")
print(result)

if macd_element:
    macd_data = macd_element.text.strip()
    print("MACD数据:", macd_data)
else:
    print("未找到MACD数据")

# 提取MACD数据
macd_data = macd_element.text.strip()

# 打印MACD数据
print("MACD数据:", macd_data)