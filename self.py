import os
import json
import psutil
import random
import re
from hurry.filesize import size
from datetime import datetime
from pytz import timezone
from pyrogram import Client, idle, filters, enums
from pyrogram.types import Message
from pyrogram.raw import functions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from plugins1 import read_json, write_json
from asyncio import sleep
import aiohttp
from bs4 import BeautifulSoup
from pyrogram.enums import ParseMode
from tala import handle_tala_command
from youto import handle_youtube_download
from insta import handle_instagram_download
from spotify import handle_spotify_download
from joke import handle_joke
from shaer import handle_poem
from gpt import handle_gpt
from bio import handle_bio
from privet import handle_privet
from blocked import handle_blocked
from block import handle_block
from delete_CHANEL import handle_delete_CHANEL
from pyrogram.enums import ChatType
from delete_GROP import handle_delete_GROP
from send import handle_send_commands
from tag_admin import handle_tag_admin
from pyrogram.enums import ChatMembersFilter

def debug_print(msg):
    print("[DEBUG]", msg)

if not os.path.isfile("Setting.json"):
    with open("Setting.json", "w", encoding="utf-8") as f:
        json.dump({"timename": "off", "timebio": "off", "online": "off", "playing": "off", "typing": "off"}, f, indent=6, ensure_ascii=False)

api_id = 21144930
api_hash = '48b5db06cda7329621764873f98229a7'

app = Client("CodeCraftersTeam", api_id, api_hash)

from offself import add_off_handler
add_off_handler(app)

LANG_MAP = {
    "انگلیسی": "en", "english": "en", "en": "en",
    "فارسی": "fa", "persian": "fa", "fa": "fa",
    "عربی": "ar", "arabic": "ar", "ar": "ar",
    "ترکی": "tr", "turkish": "tr", "tr": "tr",
    "روسی": "ru", "russian": "ru", "ru": "ru",
    "فرانسوی": "fr", "french": "fr", "fr": "fr",
    "آلمانی": "de", "german": "de", "de": "de",
    "اسپانیایی": "es", "spanish": "es", "es": "es",
}
API_KEY = "5994044255:Pe4ESagfCXx613I@Api_ManagerRoBot"
API_URL = "https://api.fast-creat.ir/translate"

async def translate_text(text, to_lang):
    params = {
        "apikey": API_KEY,
        "text": text,
        "to": to_lang
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("result", {}).get("translate")
    except Exception as e:
        debug_print(f"translate_text error: {e}")
    return None

# --------- هواشناسی و تاریخ زیبای شمسی ---------
WEATHER_API_URL = "https://api.codesazan.ir/Weather/"
WEATHER_API_KEY = "5994044255:bBY3e25heh@CodeSazan_APIManager_Bot"

async def get_weather(city):
    try:
        url = (
            f"{WEATHER_API_URL}"
            f"?key={WEATHER_API_KEY}"
            f"&type=Weather&city={city}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and data.get("status") == 200 and data.get("result"):
                        return data["result"]
    except Exception as e:
        print(f"weather error: {e}")
    return None

def format_weather(result):
    return (
        f"🌤️ <b>وضعیت آب‌وهوا برای:</b> <code>{result.get('address', '')}</code>\n"
        f"کشور: {result.get('flag','')} {result.get('country','')} | استان: {result.get('state','')} | شهر: {result.get('city','')}\n"
        f"مختصات: {result.get('latitude','')} ، {result.get('longitude','')}\n"
        f"تاریخ: {result.get('date','')} | ساعت: {result.get('time','')}\n"
        f"وضعیت: <b>{result.get('weather_conditions','')}</b>\n"
        f"🌡️ دما: <b>{result.get('degree','')}</b>\n"
        f"💧 رطوبت: {result.get('humidity','')} | فشار: {result.get('pressure','')}\n"
        f"💨 سرعت باد: {result.get('speed','')}\n"
        f"🌅 طلوع: {result.get('sunrise',{}).get('time','')}\n"
        f"🌇 غروب: {result.get('sunset',{}).get('time','')}\n"
        f"📍 منطقه زمانی: {result.get('time_zone','')}"
    )

def get_beautiful_date():
    import jdatetime
    tehran = timezone("Asia/Tean")
    now = datetime.now(tehran)
    persian = jdatetime.datetime.fromgregorian(datetime=now)
    weekday_map = {
        "Saturday": "شنبه", "Sunday": "یکشنبه", "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه", "Wednesday": "چهارشنبه",
        "Thursday": "پنجشنبه", "Friday": "جمعه"
    }
    weekday = weekday_map[now.strftime("%A")]
    month_map = {
        1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر", 5: "مرداد",
        6: "شهریور", 7: "مهر", 8: "آبان", 9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
    }
    jalali_str = f"{weekday} {persian.day} {month_map[persian.month]} {persian.year}"
    gregorian_str = now.strftime("%d %B %Y")
    return f"📆 {jalali_str} - {gregorian_str}"

def format_bonbast_table(results):
    best_currencies = [
        "US Dollar", "Euro", "British Pound", "Turkish Lira", "UAE Dirham",
        "Canadian Dollar", "Swiss Franc", "Australian Dollar", "Chinese Yuan",
        "Japanese Yen", "KSA Riyal", "Russian Ruble", "Qatari Riyal"
    ]
    persian_map = {
        "US Dollar": "💵 دلار آمریکا",
        "Euro": "💶 یورو",
        "British Pound": "💷 پوند انگلیس",
        "Turkish Lira": "🇹🇷 لیر ترکیه",
        "UAE Dirham": "🇦🇪 درهم امارات",
        "Canadian Dollar": "🇨🇦 دلار کانادا",
        "Swiss Franc": "🇨🇭 فرانک سوئیس",
        "Australian Dollar": "🇦🇺 دلار استرالیا",
        "Chinese Yuan": "🇨🇳 یوان چین",
        "Japanese Yen": "🇯🇵 ین ژاپن",
        "KSA Riyal": "🇸🇦 ریال عربستان",
        "Russian Ruble": "🇷🇺 روبل روسیه",
        "Qatari Riyal": "🇶🇦 ریال قطر",
    }
    line = "─" * 48
    msg = f"💵 نرخ بهترین ارزهای بن‌بست امروز:\n{line}\n"
    for item in results:
        if item["Currency"] not in best_currencies:
            continue
        name = persian_map.get(item["Currency"], item["Currency"])
        msg += (
            f"خرید: {item['AverageBuy']}   |   فروش: {item['AverageSell']}\n"
            f"⬇️ {item['min_buy']}  ⬆️ {item['max_buy']}   ⬇️ {item['min_sell']}  ⬆️ {item['max_sell']}   {name}\n"
            f"{line}\n"
        )
    return msg

def get_settings():
    return read_json("Setting.json")

def update_profile():
    data = get_settings()
    current_time = datetime.now(timezone("Asia/Tehran")).strftime("%H:%M")
    if not os.path.isfile("time.txt") or open("time.txt").read().strip() != current_time:
        try:
            hey = current_time
            debug_print(f"Update profile: hey={hey}, data={data}")
            if data.get("timebio") == "on":
                app.invoke(functions.account.UpdateProfile(about=f'فضولی شما در تایم {hey} ثبت شد'))
            if data.get("timename") == "on":
                app.invoke(functions.account.UpdateProfile(last_name=hey))
            with open("time.txt", "w", encoding="utf-8") as f:
                f.write(current_time)
        except Exception as e:
            print(f"Error in update_profile: {e}")

def online():
    data = get_settings()
    if data.get('online') == 'on':
        try:
            x = app.send_message("me", "Develop By : @Mahdi_r86\nChannel : @IIII_95_IIII")
            from time import sleep as tsleep
            tsleep(2)
            app.delete_messages("me", x.id)
        except Exception as e:
            print(f"Error in online: {e}")

async def get_hafez_fal_async():
    url = "https://www.hafez.it/tabir/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        poem_div = soup.find("div", class_="faal_poem container")
        poem = []
        if poem_div:
            poem = [p.text.strip() for p in poem_div.find_all("p") if p.text.strip()]
        taabir_divs = soup.find_all("div", class_="col-md-6")
        taabir_text = ""
        for div in taabir_divs:
            h2 = div.find("h2")
            if h2 and "تعبیر فال شما" in h2.text:
                taabir_p = div.find("p")
                if taabir_p:
                    taabir_text = taabir_p.text.strip()
                break
        return {"poem": poem, "taabir": taabir_text}
    except Exception as e:
        return {"poem": [], "taabir": f"خطا در دریافت فال: {e}"}

@app.on_message(~filters.me & ((filters.private & ~filters.bot) | (filters.mentioned & filters.group)))
async def Actions(app, message):
    data = get_settings()
    actions = {
        'playing': enums.ChatAction.PLAYING,
        'typing': enums.ChatAction.TYPING
    }
    for key, action in actions.items():
        if data.get(key) == 'on':
            try:
                await app.send_chat_action(chat_id=message.chat.id, action=action)
            except Exception as e:
                print(f"Error in {key} action: {e}")

@app.on_message(filters.text)
async def handle(client, m: Message):
    text = m.text.strip().lower()
    debug_print(f"User message: {text}")
    if text in ["راهنما", ".help"]:
        await m.edit_text(HELP_TEXT, parse_mode=ParseMode.HTML)
        return
    # دستور یوتوب
    if re.match(r"^یوتوب\s+(https?://[^\s]+)", m.text.strip(), re.IGNORECASE):
        await handle_youtube_download(m)
        return
    # دستور طلا
    if m.text.strip() == "طلا":
        await handle_tala_command(m)
        return
    # اینستا لینک
    if await handle_instagram_download(m):
        return
    # اسپاتیفای
    if await handle_spotify_download(m):
        return
    # جوک
    if await handle_joke(m):
        return
    # شعر
    if await handle_poem(m):
        return
    # چت جی پی تی 
    if await handle_gpt(m):
        return
    # بیو
    if await handle_bio(m):
        return
    # حریم خصوصی
    if await handle_privet(m):
        return
    # لیست بلک‌ها
    if await handle_blocked(m):
        return
    # بلاک
    if await handle_block(m):
        return
    # حذف کانال
    if await handle_delete_CHANEL(client, m):
        return
    # حذف گروه
    if await handle_delete_GROP(client, m):
        return
    # ارسال و فوروارد
    if await handle_send_commands(client, m):
        return
    # تگ ادمین
    if await handle_tag_admin(client, m):
        return
    # هواشناسی و تاریخ
    if await handle_weather_and_date(m): return
    text = m.text.strip().lower()
    debug_print(f"User message: {text}")
    data = get_settings()

    if text == "فال":
        waiting = await m.edit("⏳ در حال گرفتن فال حافظ ...")
        result = await get_hafez_fal_async()
        if result["poem"] or result["taabir"]:
            poem_text = "\n".join([f"    {v}" for v in result["poem"]])
            taabir = result["taabir"]
            msg = (
                "🪶 <b>فال حافظ شما</b> 🪶\n"
                "┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n"
                "<b>شعر:</b>\n"
                f"<code>{poem_text}</code>\n"
                "┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n"
                "<b>تعبیر:</b>\n"
                f"{taabir}\n"
                "┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n"
                "🧿 <i>برای گرفتن فال دوباره، دوباره بنویس: فال</i>"
            )
            await waiting.edit(msg, parse_mode=ParseMode.HTML)
        else:
            await waiting.edit("❌ خطا در دریافت فال حافظ.")
        return
    # --- لوگو اسم ---
    match_logo = re.match(r"^لوگو\s+(.+)", m.text.strip(), re.IGNORECASE)
    if match_logo:
        logo_text = match_logo.group(1)
        logo_id = random.randint(1, 140)
        api_url = (
            "https://api.fast-creat.ir/logo/"
            "?apikey=5994044255:sh3GX1r9Vm4BkI0@Api_ManagerRoBot"
            "&type=logo"
            f"&id={logo_id}"
            f"&text={logo_text}"
        )
        waiting_message = await m.reply("⏳ در حال دریافت لوگو ... لطفاً منتظر بمانید.")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        file_data = await resp.read()
                        temp_file = f"logo_{random.randint(1000,9999)}.png"
                        with open(temp_file, "wb") as f:
                            f.write(file_data)
                        await m.reply_photo(photo=temp_file, caption=f"🔹 لوگو ساخته شد با متن: {logo_text}")
                        os.remove(temp_file)
                        await waiting_message.delete()
                        await m.delete()
                    else:
                        await waiting_message.edit("❌ دریافت لوگو موفق نبود.")
        except Exception as e:
            await waiting_message.edit(f"❌ خطا در دریافت لوگو: {e}")
        return

    # --- دستور اسپم سلام (یا هر متن یا ایموجی) ---
    match_spam_salam = re.match(r"^اسپم(?:\s+(.+))?$", m.text.strip(), re.IGNORECASE)
    if match_spam_salam:
        to_send = match_spam_salam.group(1) if match_spam_salam.group(1) else "سلام"
        count = 10
        try:
            if m.reply_to_message:
                for _ in range(count):
                    await m.reply_to_message.reply(to_send)
                    await sleep(0.6)
            else:
                for _ in range(count):
                    await m.reply(to_send)
                    await sleep(0.6)
            await m.delete()
        except Exception as e:
            await m.reply(f"❌ خطا در اسپم: {e}")
        return
    if text.startswith("هوا ") or text.startswith("هواشناسی "):
        city = text.split(" ", 1)[1].strip() if " " in text else ""
        if not city:
            await m.edit_text("❗ لطفا نام شهر را بعد از 'هوا' بنویسید.\nمثال: هوا تهران")
            return True
        msg = await m.edit_text(f"⏳ دریافت اطلاعات آب‌وهوا برای {city} ...")
        result = await get_weather(city)
        if result and result.get("city"):
            text = format_weather(result)
            await msg.edit(text)
        else:
            await msg.edit(f"❌ اطلاعات آب‌وهوا برای '{city}' یافت نشد.")
            return
    if text == "ارز بن بست":
        await m.edit("🔄 دریافت قیمت ارزهای بن‌بست ...")
        try:
            url = "https://api.fast-creat.ir/bonbast?apikey=5994044255:fORPIT0W6dSpBKq@Api_ManagerRoBot"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data_api = await resp.json()
            if data_api.get("ok") and data_api.get("results"):
                msg = format_bonbast_table(data_api["results"])
                if len(msg) > 4000:
                    part_size = 4000
                    for i in range(0, len(msg), part_size):
                        await m.reply(msg[i:i+part_size])
                    await m.delete()
                else:
                    await m.edit(msg)
            else:
                await m.edit("❌ دریافت قیمت ارزها موفق نبود.")
        except Exception as e:
            await m.edit(f"❌ خطا در دریافت اطلاعات ارز: {e}")
        return

    if text == "تنظیم پروفایل":
        if m.reply_to_message and m.reply_to_message.photo:
            await m.edit("⏳ لطفاً صبر کنید، عکس پروفایل در حال تغییر است...")
            photo_path = await m.reply_to_message.download()
            try:
                await client.set_profile_photo(photo=photo_path)
                await m.edit("✅ عکس پروفایل شما با موفقیت تغییر کرد.")
            except Exception as e:
                await m.edit(f"❌ عکس پروفایل تنظیم نشد!\n{e}")
            finally:
                if os.path.exists(photo_path):
                    os.remove(photo_path)
        else:
            await m.edit("❗ لطفاً روی یک پیام عکس ریپلای کنید و سپس عبارت 'تنظیم پروفایل' را ارسال نمایید.")
        return

    fa_settings = {
        "زمان روشن": ("timename", "on"),
        "زمان خاموش": ("timename", "off"),
        "زمان‌بیو روشن": ("timebio", "on"),
        "زمان‌بیو خاموش": ("timebio", "off"),
        "انلاین": ("online", "on"),
        "افلاین": ("online", "off"),
        "بازی روشن": ("playing", "on"),
        "بازی خاموش": ("playing", "off"),
        "نوشتن روشن": ("typing", "on"),
        "نوشتن خاموش": ("typing", "off"),
    }
    if text in fa_settings:
        key, value = fa_settings[text]
        data[key] = value
        write_json("Setting.json", data)
        await m.edit(f"**• {key.replace('_', ' ').capitalize()} is {value}**")
        debug_print(f"Persian setting: {key} -> {value}")
        return

    if m.from_user and m.from_user.is_self:
        settings = {
            ".timename ": "timename",
            ".timebio ": "timebio",
            ".online ": "online",
            ".playing ": "playing",
            ".typing ": "typing"
        }
        for prefix, setting_key in settings.items():
            if text.startswith(prefix):
                replace = text.replace(prefix, "")
                if replace in ["on", "off"]:
                    data[setting_key] = replace
                    write_json("Setting.json", data)
                    await m.edit(f"**• {setting_key.replace('_', ' ').capitalize()} is {replace}**")
                    debug_print(f"Set {setting_key} = {replace}")
                return

# --------- هواشناسی و تاریخ زیبای شمسی ---------
async def handle_weather_and_date(m):
    text = (m.text or "").strip()
    # تاریخ
    if text in ["تاریخ", "date"]:
        await m.edit_text(get_beautiful_date())
        return True
    # هواشناسی/هوا
    if text.startswith("هوا ") or text.startswith("هواشناسی "):
        city = text.split(" ", 1)[1].strip() if " " in text else ""
        if not city:
            await m.edit_text("❗ لطفا نام شهر را بعد از 'هوا' بنویسید.\nمثال: هوا تهران")
            return True
        msg = await m.edit_text(f"⏳ دریافت اطلاعات آب‌وهوا برای {city} ...")
        result = await get_weather(city)
        if result and result.get("city"):
            text = format_weather(result)
            await msg.edit(text)
        else:
            await msg.edit(f"❌ اطلاعات آب‌وهوا برای '{city}' یافت نشد.")
        return True
    if m.from_user and m.from_user.is_self:
        # ادامه کد برای دستورات خاص کاربر خود
        return False
    return False

@app.on_message(filters.photo, group=200)
async def onphoto(c: Client, m: Message):
    try:
        if m.photo.ttl_seconds:
            rand = random.randint(1, 999)
            local = f"downloads/aks-{rand}.png"
            await app.download_media(message=m, file_name=f"aks-{rand}.png")
            user_id = m.from_user.id if m.from_user else m.chat.id
            username = m.from_user.username if m.from_user and m.from_user.username else f"ID: {user_id}"
            await app.send_photo(
                chat_id="me",
                photo=local,
                caption=f"🔥 New timed image {m.photo.date} | time: {m.photo.ttl_seconds}s | User: @{username}"
            )
            os.remove(local)
    except Exception as e:
        print(f"An error occurred: {e}")

HELP_TEXT = """
╔════════════════════════════════════╗
║    🤖 راهنمای کامل ربات مدیریت پیشرفته    ║
╚════════════════════════════════════╝

🌟 دستورات اصلی:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 راهنما: <code>.help</code>
🟢 پینگ: <code>.ping</code>
🟢 وضعیت تنظیمات: <code>.status</code>
🟢 وضعیت حریم خصوصی: <code>وضعیت حریم</code> یا <code>STATUS PRIVACY</code>
🟢 لیست بلاک‌ها: <code>لیست بلاک</code> یا <code>blocked list</code>
🟢 بلاک کاربر: <code>مسدود</code> یا <code>بلاک</code> (ریپلای )
🗓️ تاریخ امروز: <code>تاریخ</code> یا <code>date</code>
☁️ هواشناسی: <code>هواشناسی <نام شهر></code>
    مثال: <code>هواشناسی تهران</code> یا <code>هواشناسی Mashhad</code>
🎥 دانلود ویدیو اینستاگرام:  
    <code>اینستا <لینک پست اینستاگرام></code>
    مثال:  
    <code>اینستا https://www.instagram.com/reel/DJpAqZyK_tP/?utm_source=ig_web_copy_link</code>
💵 دریافت نرخ ارز بن‌بست:  
    <code>ارز بن بست</code>
⚡ ساخت لوگو اسم یا متن:  
    <code>لوگو <اسم یا متن دلخواه></code>
    مثال: <code>لوگو Mahdi</code>
🪶 گرفتن فال حافظ: <code>فال</code>
🎬 دانلود ویدیو یوتیوب:
    <code>یوتوب <لینک یوتیوب></code>
    مثال: <code>یوتوب https://youtu.be/</code>
🟡 قیمت لحظه‌ای طلا و مثقال: <code>طلا</code>
🎵 دانلود موزیک اسپاتیفای:
    <code>اسپاتیفای <لینک اسپاتیفای></code>
    مثال: <code>اسپاتیفای https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC</code>
😂 دریافت جوک خنده‌دار: <code>جوک</code>
🌸 دریافت شعر: <code>شعر</code>
📝 دریافت بیو پیشنهادی: <code>بیو</code>
🤖 پرسش از هوش مصنوعی:
    <code>.gpt متن یا سوال شما</code>
    مثال: <code>.gpt بهترین خواننده ایران</code>

━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 ارسال و فوروارد گروهی:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔹 برای ارسال یا فوروارد پیام (متنی یا ریپلای) به تمام چت‌های شما، کافیست یکی از دستورات زیر را بنویسید:

📨 <b>ارسال پیام به:</b>
• پیوی‌ها: <code>ارسال به پیوی</code> یا <code>send to privates</code>
• گروه‌ها: <code>ارسال به گروه</code> یا <code>send to groups</code>
• همه چت‌ها: <code>ارسال به همه</code> یا <code>send to all</code>
• مخاطبین: <code>ارسال به مخاطبین</code> یا <code>send to contacts</code>

📤 <b>فوروارد پیام به:</b>
• پیوی‌ها: <code>فوروارد به پیوی</code> یا <code>forward to privates</code>
• گروه‌ها: <code>فوروارد به گروه</code> یا <code>forward to groups</code>
• همه چت‌ها: <code>فوروارد به همه</code> یا <code>forward to all</code>
• مخاطبین: <code>فوروارد به مخاطبین</code> یا <code>forward to contacts</code>

✨ <b>تگ و منشن ادمین‌های گروه:</b>
• تگ ادمین: <code>تگ ادمین</code> یا <code>tag admin</code>
• منشن ادمین: <code>منشن ادمین</code> یا <code>mention admin</code>
🔸 فقط مدیران گروه را منشن می‌کند!

ℹ️ <b>نکات مهم:</b>
- اگر روی یک پیام ریپلای کنید، همان پیام ارسال/فوروارد می‌شود.
- اگر بعد از دستور، متنی بنویسید، آن متن به جای پیام ریپلای ارسال می‌شود.
- برای ارسال گروهی فقط همین دستورات کافیست.

🧹 پاکسازی سریع:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 ترک همه کانال‌ها:
    <code>پاکسازی کانال</code>
    🔹 با این دستور، ربات به صورت خودکار از تمام کانال‌هایی که عضو آن هستید خارج می‌شود.

🚨 ترک همه گروه‌ها:
    <code>پاکسازی گروه</code>
    🔹 با این دستور، ربات به صورت خودکار از همه گروه‌ها و سوپرگروه‌هایی که عضو آن هستید خارج می‌شود.

🕰️ کنترل زمان و وضعیت:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔵 روشن/خاموش کردن نام زمان‌دار:
    <code>زمان روشن</code> | <code>زمان خاموش</code>
    یا: <code>.timename on</code> / <code>.timename off</code>
🔵 روشن/خاموش کردن بیو زمان‌دار:
    <code>زمان‌بیو روشن</code> | <code>زمان‌بیو خاموش</code>
    یا: <code>.timebio on</code> / <code>.timebio off</code>
🟣 وضعیت آنلاین/آفلاین:
    <code>انلاین</code> | <code>افلاین</code>
    یا: <code>.online on</code> / <code>.online off</code>
🟣 وضعیت بازی:
    <code>بازی روشن</code> | <code>بازی خاموش</code>
    یا: <code>.playing on</code> / <code>.playing off</code>
🟣 وضعیت تایپینگ:
    <code>نوشتن روشن</code> | <code>نوشتن خاموش</code>
    یا: <code>.typing on</code> / <code>.typing off</code>

🌐 ترجمه:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔸 ترجمه ریپلای: ریپلای و ارسال <code>ترجمه</code> یا <code>translate</code>
🔸 ترجمه به زبان دلخواه:
    <code>ترجمه انگلیسی سلام</code>
    یا:
    <code>translate en سلام</code>

📆 تاریخ:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 نمایش تاریخ شمسی و میلادی:
    <code>تاریخ</code> یا <code>امروز</code> یا <code>date</code>

🖼️ تغییر عکس پروفایل:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• ریپلای روی یک عکس و ارسال  
  <code>تنظیم پروفایل</code>

⚡ اسپم (متن/ایموجی):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• برای ارسال اسپم (ده‌بار تکرار یک متن یا ایموجی):
  ۱. اگر می‌خواهید یک متن یا ایموجی را اسپم کنید (بدون ریپلای):
      - فقط کافیست بنویسید:
        <code>اسپم [متن دلخواه یا ایموجی]</code>
      - مثال:
        <code>اسپم سلام</code>
        <code>اسپم 🤣</code>
        <code>اسپم متن تستی</code>
  ۲. اگر روی یک پیام ریپلای کنید و بنویسید <code>اسپم</code>، همان پیام ریپلای را ده‌بار ارسال می‌کند.
  ⚠️ اگر چیزی بعد از "اسپم" ننویسید و ریپلای هم نباشد، پیش‌فرض "سلام" ده بار ارسال می‌شود.

📝 سایر نکات:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• تنظیمات فارسی را همه می‌توانند تغییر دهند.
• تنظیمات انگلیسی فقط برای اکانت اصلی فعال است.
• مشاهده وضعیت فعلی ربات: <code>.status</code>
• راهنمایی بیشتر: <a href="https://t.me/Mahdi_r86">سازنده ربات</a>

╔════════════════════════════════════╗
║         @IIII_95_IIII           ║
╚════════════════════════════════════╝
"""

scheduler = AsyncIOScheduler()
scheduler.add_job(update_profile, "interval", seconds=10)
scheduler.add_job(online, "interval", seconds=45)
scheduler.start()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        app.start()
        print("Started ...")
        app.send_message("me", "🟢 **Bot is up and running!**")
        if not scheduler.running:
            scheduler.start()
        loop.run_until_complete(idle())
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        try:
            if scheduler.running:
                scheduler.shutdown()
            app.stop()
        except Exception as e:
            print(f"Error stopping client or scheduler: {e}")
        loop.close()