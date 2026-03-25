import requests
from bs4 import BeautifulSoup
import time
import re

BOT_TOKEN = "填你的token"
CHAT_ID = "填你的chat_id"

last_data = None

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_data():
    url = "https://zl288.app/jnd28.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    match = re.search(r'(\d)\+(\d)\+(\d)=', text)
    if match:
        return tuple(map(int, match.groups()))
    return None

def analyze(arr):
    count43 = sum(1 for x in arr if x in [3,4])
    count89 = sum(1 for x in arr if x in [8,9])
    wave = max(arr) - min(arr)

    score = 0
    if count89 >= 2: score += 4
    if count43 >= 2: score += 3
    if wave <= 5: score += 2

    if count89 >= 2 and score >= 8:
        return True, score
    return False, score

while True:
    data = get_data()

    if data and data != last_data:
        last_data = data

        ok, score = analyze(data)

        if ok:
            send(f"🔥 云端信号\n数据：{data}\n状态：{score}\n建议：做（重仓）")

    time.sleep(20)

print("🚀 V17系统运行中...")
app.run_polling()
