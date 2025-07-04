import aiohttp
import re
from pyrogram.enums import ParseMode

SPOTIFY_API_URL = "https://api.majidapi.ir/music/spotify/download"
SPOTIFY_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_spotify_download(m):
    """
    هندلر دانلود موزیک اسپاتیفای
    دستور: اسپاتیفای <لینک اسپاتیفای>
    """
    match = re.match(r"^اسپاتیفای\s+(https?://[^\s]+)", m.text.strip(), re.IGNORECASE)
    if not match:
        return

    spotify_url = match.group(1)
    waiting = await m.reply("⏳ در حال دریافت لینک دانلود موزیک از اسپاتیفای ...")
    params = {
        "url": spotify_url,
        "token": SPOTIFY_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(SPOTIFY_API_URL, params=params) as resp:
                data = await resp.json()
        if (
            isinstance(data, dict)
            and data.get("status") == 200
            and data.get("result")
        ):
            music_link = data["result"]
            msg = (
                "🎵 <b>دانلود موزیک اسپاتیفای</b>\n"
                "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
                "📥 <b>لینک دانلود:</b>\n"
                f'<a href="{music_link}">⬇️ دانلود مستقیم موزیک</a>\n\n'
               
            )
            await waiting.edit(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=False)
        else:
            await waiting.edit("❌ دریافت لینک از اسپاتیفای موفق نبود یا لینک معتبر نیست.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await waiting.edit(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )