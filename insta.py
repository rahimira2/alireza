import aiohttp
import re
from pyrogram.enums import ParseMode

INSTAGRAM_API_URL = "https://api.majidapi.ir/instagram/download"
INSTAGRAM_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_instagram_download(m):
    match = re.match(r"^اینستا\s+(https?://[^\s]+)", m.text.strip(), re.IGNORECASE)
    if not match:
        return

    insta_url = match.group(1)
    waiting = await m.reply("⏳ در حال دریافت اطلاعات ویدیو ...")
    params = {
        "url": insta_url,
        "token": INSTAGRAM_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(INSTAGRAM_API_URL, params=params) as resp:
                data = await resp.json()
        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and "result" in data
        ):
            res = data["result"]
            video_url = res.get("video")
            caption = res.get("caption", "")
            likes = res.get("likes", 0)
            if video_url:
                msg = (
    "🎬 <b>ویدیوی اینستاگرام آماده دانلود است!</b>\n"
    "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
    "📥 <b>لینک دانلود:</b>\n"
    f'<a href="{video_url}">⬇️ دانلود و مشاهده ویدیو</a>\n\n'
    "📝 <b>کپشن:</b>\n"
    f"{caption}\n\n"
    f"❤️ <b>تعداد لایک:</b> <code>{likes:,}</code>"
)
                await waiting.edit(msg, parse_mode=ParseMode.HTML)
            else:
                await waiting.edit("❌ ویدیو پیدا نشد.", parse_mode=ParseMode.HTML)
        else:
            await waiting.edit("❌ دریافت اطلاعات از اینستاگرام موفق نبود یا پست معتبر نیست.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await waiting.edit(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )