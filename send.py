from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, UserIsBlocked
import asyncio

async def get_my_chats(client, types):
    chats = []
    async for dialog in client.get_dialogs():
        if dialog.chat.type in types:
            chats.append(dialog.chat.id)
    return chats

async def get_contacts(client):
    contacts = []
    users = await client.get_contacts()
    for user in users:
        contacts.append(user.id)
    return contacts

async def send_to_chats(client, message, chat_ids, text=None, forward=False):
    sent = 0
    failed = 0
    for chat_id in chat_ids:
        try:
            if forward and message.reply_to_message:
                await client.forward_messages(chat_id, message.chat.id, message.reply_to_message.id)
            elif text:
                await client.send_message(chat_id, text)
            elif message.reply_to_message:
                await message.reply_to_message.copy(chat_id)
            else:
                continue
            sent += 1
            await asyncio.sleep(0.2)
        except (PeerIdInvalid, UserIsBlocked):
            failed += 1
        except Exception as e:
            print(f"[send_to_chats] Error for {chat_id}: {e}")
            failed += 1
    return sent, failed

async def animated_waiting(msg, stop_event):
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
    ]
    last = None
    i = 0
    while not stop_event.is_set():
        frame = RELOAD_FRAMES[i % len(RELOAD_FRAMES)]
        if frame != last:
            try:
                await msg.edit(frame)
            except Exception as e:
                if "MESSAGE_NOT_MODIFIED" not in str(e):
                    print(f"[animated_waiting] {e}")
            last = frame
        i += 1
        await asyncio.sleep(0.2)

async def handle_send_commands(client, m):
    text = m.text or ""
    cmd = text.strip().lower()

    commands = {
        "ارسال به پیوی": {"types": [ChatType.PRIVATE], "forward": False},
        "send to privates": {"types": [ChatType.PRIVATE], "forward": False},

        "ارسال به گروه": {"types": [ChatType.GROUP, ChatType.SUPERGROUP], "forward": False},
        "send to groups": {"types": [ChatType.GROUP, ChatType.SUPERGROUP], "forward": False},

        "ارسال به همه": {"types": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP], "forward": False},
        "send to all": {"types": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP], "forward": False},

        "ارسال به مخاطبین": {"types": [], "contacts": True, "forward": False},
        "send to contacts": {"types": [], "contacts": True, "forward": False},

        "فوروارد به پیوی": {"types": [ChatType.PRIVATE], "forward": True},
        "forward to privates": {"types": [ChatType.PRIVATE], "forward": True},

        "فوروارد به گروه": {"types": [ChatType.GROUP, ChatType.SUPERGROUP], "forward": True},
        "forward to groups": {"types": [ChatType.GROUP, ChatType.SUPERGROUP], "forward": True},

        "فوروارد به همه": {"types": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP], "forward": True},
        "forward to all": {"types": [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP], "forward": True},

        "فوروارد به مخاطبین": {"types": [], "contacts": True, "forward": True},
        "forward to contacts": {"types": [], "contacts": True, "forward": True},
    }

    found = None
    for key in commands:
        if cmd.startswith(key):
            found = key
            break
    if not found:
        return False

    params = commands[found]

    # استخراج متن اضافه دقیق
    extra_text = None
    remain = text[len(found):].strip()
    if remain:
        extra_text = remain

    if not m.reply_to_message and not extra_text:
        await m.reply("لطفاً روی یک پیام ریپلای کنید یا متنی بعد از دستور بنویسید.")
        return True

    if params.get("contacts"):
        chat_ids = await get_contacts(client)
    else:
        chat_ids = await get_my_chats(client, params["types"])

    if not chat_ids:
        await m.reply("هیچ چتی پیدا نشد.")
        return True

    waiting = await m.reply("⏳ منتظر بمانید...\n[░░░░░░░░░░]")
    stop_event = asyncio.Event()
    task = asyncio.create_task(animated_waiting(waiting, stop_event))

    sent, failed = await send_to_chats(
        client=client,
        message=m,
        chat_ids=chat_ids,
        text=extra_text,
        forward=params["forward"]
    )

    stop_event.set()
    await task

    await waiting.edit(f"✅ ارسال/فوروارد انجام شد!\nموفق: {sent}\nناموفق: {failed}")
    return True