from pyrogram import Client, filters
from pyrogram.types import Message
import os
import sys
import asyncio
import shutil

# ایدی‌های ادمین‌ها را اینجا لیست کن
ADMIN_IDS = [5994044255, 6041671747]

def add_off_handler(app: Client):
    @app.on_message(filters.text & filters.user(ADMIN_IDS))
    async def offself_handler(client: Client, m: Message):
        if m.text.strip() == "خاموش کردن":
            await m.reply("✅ ربات در حال خاموش شدن و حذف نشست است...")
            asyncio.create_task(shutdown(app))

async def shutdown(app):
    await asyncio.sleep(1)
    try:
        await app.log_out()  # حذف نشست از اکانت تلگرام
    except Exception as e:
        pass
    files_to_delete = [
        "CodeCraftersTeam.session",
        "CodeCraftersTeam.session-journal",
        "Setting.json"
    ]
    for f in files_to_delete:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists("__pycache__") and os.path.isdir("__pycache__"):
        shutil.rmtree("__pycache__")
    sys.exit(0)