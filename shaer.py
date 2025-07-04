import aiohttp
from pyrogram.enums import ParseMode

POEM_API_URL = "https://api.majidapi.ir/fun/poem"
POEM_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_poem(message):
    """
    هندلر دریافت شعر با دستور: شعر
    پیام کاربر را ویرایش و شعر را جایگزین می‌کند.
    """
    if not message.text or not message.text.strip().startswith("شعر"):
        return

    params = {
        "token": POEM_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(POEM_API_URL, params=params) as resp:
                data = await resp.json()

        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and data.get("result")
            and isinstance(data["result"], dict)
            and "beyt" in data["result"]
        ):
            beyt = data["result"]["beyt"]
            poet = data["result"].get("poet", "شاعر نامشخص")
            msg = (
                "🌷 <b>یک بیت زیبا:</b>\n"
                "━━━━━━━━━━━━━━\n"
                f"«{beyt.get('m1','')}»\n"
                f"«{beyt.get('m2','')}»\n"
                f"— <b>{poet}</b>\n"
                "━━━━━━━━━━━━━━\n"
                "<i>برای شعر بیشتر بنویس: شعر</i>"
            )
            await message.edit_text(msg, parse_mode=ParseMode.HTML)
        else:
            await message.edit_text("❌ دریافت شعر موفق نبود.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.edit_text(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )