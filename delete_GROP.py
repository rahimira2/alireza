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

async def handle_delete_GROP(client, m):
    if m.text and m.text.strip() == "پاکسازی گروه":
        msg = await m.reply(RELOAD_FRAMES[0])
        for frame in RELOAD_FRAMES[1:]:
            await asyncio.sleep(0.3)
            await msg.edit(frame)
        deleted = 0
        found = 0
        # لیست گروه‌ها (group و supergroup)
        group_ids = []
        async for dialog in client.get_dialogs():
            if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                group_ids.append(dialog.chat.id)
        found = len(group_ids)
        for idx, group_id in enumerate(group_ids, 1):
            try:
                await client.leave_chat(group_id)
                deleted += 1
                await msg.edit(f"در حال ترک گروه {deleted} از {found} ...")
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"خطا در ترک گروه {group_id}: {e}")
        await msg.edit(
            f"✅ پاکسازی گروه‌ها تمام شد!\n"
            f"تعداد کل گروه‌ها: {found}\n"
            f"تعداد موفق ترک شده: {deleted}\n"
            f"{'تمام گروه‌ها ترک شدند.' if deleted==found else 'برخی گروه‌ها ترک نشدند.'}"
        )
        return True
    return False