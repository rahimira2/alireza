async def handle_block(message):
    """
    هندلر مسدودسازی کاربر با دستور "مسدود" یا "بلاک"
    استفاده در کد اصلی: if await handle_block(m): return
    """
    command = message.text.strip().lower()
    if command not in ["مسدود", "بلاک"]:
        return False

    target_id = None
    target_info = None

    # حالت ریپلای به پیام کاربر دیگر
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        target_id = user.id
        name = ((user.first_name or "") + (" " + user.last_name if getattr(user, "last_name", None) else "")).strip()
        username = f"@{user.username}" if getattr(user, 'username', None) else ""
        target_info = f"{username} ({name})" if username else name
    # حالت پیوی (نه Saved Messages)
    elif message.chat.type == "private":
        my_id = (await message._client.get_me()).id
        # فقط اگر با خودت چت نمی‌کنی (Saved Messages نباشد)
        if message.chat.id != my_id:
            target_id = message.chat.id
            user = await message._client.get_users(target_id)
            name = ((user.first_name or "") + (" " + user.last_name if getattr(user, "last_name", None) else "")).strip()
            username = f"@{user.username}" if getattr(user, 'username', None) else ""
            target_info = f"{username} ({name})" if username else name

    if not target_id:
        await message.edit_text("❗ لطفاً روی پیام کاربر ریپلای کن یا در پیوی کاربر باش.")
        return True

    try:
        await message._client.block_user(target_id)
        if not target_info:
            target_info = str(target_id)
        await message.edit_text(f"⛔ کاربر {target_info} با موفقیت مسدود شد.")
    except Exception as e:
        await message.edit_text(f"خطا در مسدودسازی کاربر:\n{e}")
    return True