from pyrogram.raw import functions

async def get_blocked_users(client):
    blocked = []
    offset = 0
    limit = 100
    while True:
        result = await client.invoke(
            functions.contacts.GetBlocked(offset=offset, limit=limit)
        )
        users = result.users
        if not users:
            break
        blocked.extend(users)
        if len(users) < limit:
            break
        offset += len(users)
    return blocked

def format_blocked_users(users):
    if not users:
        return (
            "┏━━━━━━━━━━━━━━━━━━━━━━┓\n"
            "🚫 هیچ کاربر بلاک‌شده‌ای وجود ندارد.\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━┛"
        )
    lines = ["┏━━ 📛 لیست کاربران بلاک‌شده ━━┓"]
    for i, user in enumerate(users, 1):
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else ""
        display = f"{username} ({name})" if username else name
        lines.append(f"{i}. {display}")
    lines.append("┗━━━━━━━━━━━━━━━━━━━━━━┛")
    return "\n".join(lines)

async def handle_blocked(message):
    """
    استفاده به شکل if await handle_blocked(m): return
    """
    if message.text.strip().lower() in ["لیست بلاک", "blocked list"]:
        users = await get_blocked_users(message._client)
        text = format_blocked_users(users)
        await message.edit_text(text)
        return True
    return False