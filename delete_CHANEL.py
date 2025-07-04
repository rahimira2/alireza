import asyncio
from pyrogram.enums import ChatType

RELOAD_FRAMES = [
    "⏳ منتظر بمانید...\n[░░░░░░░░░░]",
    "⏳ منتظر بمانید...\n[█░░░░░░░░░]",
    "⏳ منتظر بمانید...\n[██░░░░░░░░]",
    "⏳ منتظر بمانید...\n[███░░░░░░░]",
    "⏳ منتظر بمانید...\n[████░░░░░░]",
    "⏳ منتظر بمانید...\n[█████░░░░░]",
    "⏳ منتظر بمانید...\n[██████░░░░]",
    "⏳ منتظر بمانید...\n[███████░░░]",
    "⏳ منتظر بمانید...\n[████████░░]",
    "⏳ منتظر بمانید...\n[█████████░]",
    "⏳ منتظر بمانید...\n[██████████]",
    "✅ عملیات کامل شد!"
]

async def handle_delete_CHANEL(client, m):
    if m.text and m.text.strip() == "پاکسازی کانال":
        msg = await m.reply(RELOAD_FRAMES[0])
        for frame in RELOAD_FRAMES[1:]:
            await asyncio.sleep(0.3)
            await msg.edit(frame)
        deleted = 0
        found = 0
        # لیست آی‌دی کانال‌ها را جداگانه استخراج می‌کنیم
        channel_ids = []
        async for dialog in client.get_dialogs():
            if dialog.chat.type == ChatType.CHANNEL:
                channel_ids.append(dialog.chat.id)
        found = len(channel_ids)
        # حالا به ترتیب همه کانال‌ها را ترک می‌کنیم
        for idx, channel_id in enumerate(channel_ids, 1):
            try:
                await client.leave_chat(channel_id)
                deleted += 1
                await msg.edit(f"در حال ترک کانال {deleted} از {found} ...")
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"خطا در ترک کانال {channel_id}: {e}")
        # بعد از اتمام، فقط یک بار پیام نهایی را می‌فرستیم
        await msg.edit(
            f"✅ پاکسازی کانال‌ها تمام شد!\n"
            f"تعداد کل کانال‌ها: {found}\n"
            f"تعداد موفق ترک شده: {deleted}\n"
            f"{'تمام کانال‌ها ترک شدند.' if deleted==found else 'برخی کانال‌ها ترک نشدند.'}"
        )
        return True
    return False