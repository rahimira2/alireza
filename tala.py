import aiohttp
from pyrogram.enums import ParseMode

API_URL = "https://api.majidapi.ir/price/gold"
API_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_tala_command(m):
    try:
        msg = await m.reply("⏳ در حال دریافت اطلاعات قیمت طلا ...")
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params={"token": API_TOKEN}) as resp:
                data = await resp.json()
        # بررسی ساختار داده
        if not data or "result" not in data:
            await msg.edit("❌ دریافت اطلاعات ناموفق بود.", parse_mode=ParseMode.HTML)
            return
        result = data["result"]
        text = "<b>🏅 قیمت لحظه‌ای طلا:</b>\n"
        # طلای گرمی
        if result.get("tala"):
            text += "\n<b>• طلای گرمی:</b>\n"
            for i in result["tala"]:
                text += (f"▫️ <b>{i['title']}</b>\n"
                         f"  💵 قیمت: <b>{i['price']}</b>\n"
                         f"  🔻 تغییر: <code>{i['change']}</code>\n"
                         f"  📉 کمترین: <code>{i['lowest']}</code> | 📈 بیشترین: <code>{i['highest']}</code>\n"
                         f"  🕒 {i['time']}\n"
                         "━━━\n")
        # مثقال
        if result.get("mesghal"):
            text += "\n<b>• مثقال:</b>\n"
            for i in result["mesghal"]:
                text += (f"▫️ <b>{i['title']}</b>\n"
                         f"  💵 قیمت: <b>{i['price']}</b>\n"
                         f"  🔻 تغییر: <code>{i['change']}</code>\n"
                         f"  📉 کمترین: <code>{i['lowest']}</code> | 📈 بیشترین: <code>{i['highest']}</code>\n"
                         f"  🕒 {i['time']}\n"
                         "━━━\n")
        # آبشده
        if result.get("abshode"):
            text += "\n<b>• آبشده:</b>\n"
            for i in result["abshode"]:
                text += (f"▫️ <b>{i['title']}</b>\n"
                         f"  💵 قیمت: <b>{i['price']}</b>\n"
                         f"  🔻 تغییر: <code>{i['change']}</code>\n"
                         f"  📉 کمترین: <code>{i['lowest']}</code> | 📈 بیشترین: <code>{i['highest']}</code>\n"
                         f"  🕒 {i['time']}\n"
                         "━━━\n")
        if len(text) > 4000:
            for i in range(0, len(text), 4000):
                await m.reply(text[i:i+4000], parse_mode=ParseMode.HTML)
            await msg.delete()
        else:
            await msg.edit(text, parse_mode=ParseMode.HTML)
    except Exception as e:
        await m.reply(f"❌ خطا: {e}")