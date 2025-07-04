import aiohttp
import re
from pyrogram.enums import ParseMode

YOUTUBE_API_URL = "https://api.majidapi.ir/youtube/download"
YOUTUBE_TOKEN = "rm2jvmq1ohjkbyg:r6WBwXgljYwB2d6gZ075"

async def handle_youtube_download(m):
    match = re.match(r"^یوتوب\s+(https?://[^\s]+)", m.text.strip(), re.IGNORECASE)
    if not match:
        await m.reply("لطفاً دستور را به‌صورت صحیح وارد کن:\nیوتوب <لینک یوتیوب>")
        return
    yt_url = match.group(1)
    waiting = await m.reply("⏳ در حال دریافت لینک 720p mp4 ...")
    params = {
        "url": yt_url,
        "token": YOUTUBE_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(YOUTUBE_API_URL, params=params) as resp:
                data = await resp.json()
        formats = []
        if (
            isinstance(data, dict) and
            "result" in data and
            "res_data" in data["result"] and
            "formats" in data["result"]["res_data"]
        ):
            formats = data["result"]["res_data"]["formats"]

        mp4_720_link = None
        for fmt in formats:
            if (
                fmt.get("quality") == "720p"
                and fmt.get("ext") == "mp4"
                and fmt.get("vcodec") != "none"
            ):
                mp4_720_link = fmt.get("url")
                break

        if mp4_720_link:
            await waiting.edit(
                f"🎬 <b>لینک دانلود مستقیم 720p mp4:</b>\n"
                f"<a href=\"{mp4_720_link}\">⬇️ دانلود 720p MP4</a>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
        else:
            await waiting.edit("❌ کیفیت 720p mp4 پیدا نشد.", parse_mode=ParseMode.HTML)
    except Exception as e:
        await waiting.edit(
            f"❌ خطا در دریافت یا اتصال به API:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )