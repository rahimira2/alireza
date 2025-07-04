import aiohttp
from pyrogram.enums import ParseMode

JOKE_API_URL = "https://api.majidapi.ir/fun/joke"
JOKE_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_joke(message):
    """
    هندلر دریافت و ارسال جوک با ویرایش پیام کاربر
    """
    if not message.text or not message.text.strip().startswith("جوک"):
        return

    params = {
        "token": JOKE_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(JOKE_API_URL, params=params) as resp:
                data = await resp.json()
        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and data.get("result")
        ):
            joke = data["result"]
            msg = (
                "🤣 <b>جوک خنده‌دار برات پیدا کردم:</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"<i>{joke}</i>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🔄 برای دریافت جوک جدید دوباره بنویس: <b>جوک</b>"
            )
            await message.edit_text(msg, parse_mode=ParseMode.HTML)
        else:
            await message.edit_text("❌ دریافت جوک موفق نبود.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.edit_text(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )