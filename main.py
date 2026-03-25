import requests
from bs4 import BeautifulSoup
import time
import re
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "你的TOKEN"

running = False
last_data = None

# 发送消息
async def send_msg(app, chat_id, msg):
    await app.bot.send_message(chat_id=chat_id, text=msg)

# 抓数据
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

# 分析
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

# 后台监听线程
def worker(app, chat_id):
    global running, last_data

    while running:
        try:
            data = get_data()

            if data and data != last_data:
                last_data = data
                ok, score = analyze(data)

                if ok:
                    msg = f"🔥 云端信号\n数据：{data}\n状态：{score}\n建议：做（重仓）"
                    app.create_task(send_msg(app, chat_id, msg))

        except Exception as e:
            print("错误：", e)

        time.sleep(20)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 V17系统\n\n"
        "发送：\n"
        "开启 - 开始监听\n"
        "停止 - 停止监听"
    )

# 控制
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    text = update.message.text
    chat_id = update.effective_chat.id
    app = context.application

    if text == "开启":
        if not running:
            running = True
            threading.Thread(target=worker, args=(app, chat_id)).start()
            await update.message.reply_text("✅ 已开启监听")
        else:
            await update.message.reply_text("已经在运行了")

    elif text == "停止":
        running = False
        await update.message.reply_text("🛑 已停止")

    else:
        await update.message.reply_text("请输入：开启 或 停止")

# 启动
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

print("🚀 V17系统运行中...")
app.run_polling()
