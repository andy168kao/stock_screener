import requests
from bs4 import BeautifulSoup
import re

URL = 'https://fubon-ebrokerdj.fbs.com.tw/Z/ZC/ZCW/ZCWG/ZCWG_2890_72.djhtm'
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
print(tenp)
for i, num in enumerate(numbers_part2):
    tenp -= num
    print (tenp)
    if tenp <= 0:  # 当temp小于或等于0时，记录索引并退出循环
        index = i
        break
print(index)  # 打印索引
numbers_part1 = [float(n) for n in part1.split(",")]
upper = numbers_part1[index]
print(total)

print("--------")

numbers_part2_reversed = numbers_part2[::-1]  # 反转数列
tenp = total * 0.1
print(tenp)

# 从最后一个数开始减去temp
for i, num in enumerate(numbers_part2_reversed):
    tenp -= num
    print(tenp)
    if tenp <= 0:
        index_reversed = i
        break

print(index_reversed)  # 打印索引

numbers_part1_reversed = numbers_part1[::-1]
lower = numbers_part1_reversed[index_reversed]
print(lower)