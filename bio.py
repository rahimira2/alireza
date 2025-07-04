import aiohttp
from pyrogram.enums import ParseMode

BIO_API_URL = "https://api.majidapi.ir/fun/bio"
BIO_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_bio(message):
    """
    هندلر دریافت بیو با دستور: بیو
    پیام کاربر را ویرایش و یک بیو زیبا جایگزین می‌کند.
    """
    if not message.text or not message.text.strip().startswith("بیو"):
        return

    params = {
        "token": BIO_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BIO_API_URL, params=params) as resp:
                data = await resp.json()

        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and data.get("result")
        ):
            bio = data["result"]
            msg = (
                "📝 <b>بیو پیشنهادی:</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"<i>{bio}</i>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "<i>برای دریافت بیو جدید دوباره بنویس: بیو</i>"
            )
            await message.edit_text(msg, parse_mode=ParseMode.HTML)
        else:
            await message.edit_text("❌ دریافت بیو موفق نبود.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.edit_text(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )