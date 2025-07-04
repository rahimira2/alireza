import aiohttp
from pyrogram.enums import ParseMode

GPT_API_URL = "https://api.majidapi.ir/gpt/35"
GPT_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_gpt(message):
    """
    هندلر دریافت پاسخ از GPT-3.5 با دستور .gpt
    """
    if not message.text or not message.text.strip().startswith(".gpt"):
        return

    # گرفتن پارامتر q بعد از .gpt
    parts = message.text.strip().split(" ", 1)
    if len(parts) < 2 or not parts[1].strip():
        await message.edit_text(
            "❗ بعد از دستور <b>.gpt</b> سوال یا متن خود را وارد کنید.\nمثال:\n<code>.gpt بهترین خواننده ایران</code>",
            parse_mode=ParseMode.HTML
        )
        return

    q = parts[1].strip()
    params = {
        "q": q,
        "token": GPT_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GPT_API_URL, params=params) as resp:
                data = await resp.json()
        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and data.get("result")
        ):
            result = data["result"]
            msg = (
                "🤖 <b>پاسخ هوش مصنوعی:</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"{result}\n"
                "━━━━━━━━━━━━━━━━━━"
            )
            await message.edit_text(msg, parse_mode=ParseMode.HTML)
        else:
            await message.edit_text("❌ دریافت پاسخ موفق نبود.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.edit_text(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )