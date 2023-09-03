import requests
from bs4 import BeautifulSoup

URL = 'https://tw.stock.yahoo.com/quote/00878.TW/institutional-trading'
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

print (WeeklyForeignInstitutionalInvestors)


