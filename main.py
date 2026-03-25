import requests
from bs4 import BeautifulSoup
import time
import re
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

last_data = None

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def get_data():
    try:
        url = "https://zl288.app/jnd28.html"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        text = r.text
        match = re.search(r'(\d)\+(\d)\+(\d)=', text)

        if match:
            return tuple(map(int, match.groups()))
    except:
        return None

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

print("系统启动成功")

while True:
    try:
        data = get_data()

        if data and data != last_data:
            last_data = data

            ok, score = analyze(data)

            if ok:
                send(f"🔥信号\n数据:{data}\n评分:{score}")

        time.sleep(15)

    except:
        time.sleep(5)
print("🚀 V17系统运行中...")
app.run_polling()
