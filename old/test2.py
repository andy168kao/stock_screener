import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 定义目标网页链接
url = "https://tw.stock.yahoo.com/quote/0056.TW/broker-trading"
response = requests.get(url, headers=headers)


# 发送HTTP请求并获取页面内容
html_content = response.content

# 使用Beautiful Soup解析页面内容
soup = BeautifulSoup(html_content, "html.parser")
# 查找具有特定类名的元素
target_element = soup.find("div", class_="Fz(24px) Fz(18px)--mobile Fw(600) H(28px) H(a)--mobile Mt(4px) C($c-trend-down)")

if target_element:
    content = target_element.get_text()
    print("抓取的内容:", content)
else:
    print("未找到目标元素")

# print("抓取的内容:", content)
