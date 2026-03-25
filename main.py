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
        print("准备发送:", msg)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })
        print("返回:", res.text)
    except Exception as e:
        print("发送失败:", e)

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

print("✅ 程序启动成功（云端运行中）")

last_data = None

last_data = None

while True:
    data = get_data()
    
    print("当前数据:", data)

    if data and data != last_data:
        msg = f"🔥新数据: {data}"
        send(msg)
        print("已发送:", msg)
        last_data = data

    time.sleep(10)

    except Exception as e:
        print("主循环错误:", e)
        time.sleep(5)
send("🔥我活了🔥")
print("BOT:", BOT_TOKEN)
print("CHAT:", CHAT_ID)
send("🔥启动成功🔥")
print("已发送测试")
