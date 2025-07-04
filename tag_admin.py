from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.types import Message

async def handle_tag_admin(client, m: Message):
    text = (m.text or "").strip().lower()
    commands = [
        "تگ ادمین",
        "منشن ادمین",
        "tag admin",
        "mention admin"
    ]
    if text not in commands:
        return False

    chat_type = getattr(m.chat, 'type', None)
    if hasattr(chat_type, "value"):
        chat_type = chat_type.value.lower()
    elif isinstance(chat_type, str):
        chat_type = chat_type.lower()
    else:
        chat_type = ""

    if chat_type not in ["group", "supergroup"]:
        await m.reply("این دستور فقط در گروه‌ها قابل استفاده است.")
        return True

    admins = []
    async for member in client.get_chat_members(m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if not member.user.is_bot:
            admins.append(member.user)

    if not admins:
        await m.reply("هیچ ادمینی در این گروه پیدا نشد!")
        return True

    mention_text = "🟢 منشن ادمین‌های گروه:\n"
    for user in admins:
        name = user.first_name or ""
        if user.last_name:
            name += " " + user.last_name
        mention_text += f"• <a href='tg://user?id={user.id}'>{name}</a>\n"

    # 👇 نکته مهم: استفاده از ParseMode.HTML
    await m.reply(mention_text, quote=True, parse_mode=ParseMode.HTML)
    return True