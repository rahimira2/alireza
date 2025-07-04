from pyrogram.raw import functions, types

privacy_keys = [
    (types.InputPrivacyKeyPhoneNumber(), "شماره (phone)", "📱"),
    (types.InputPrivacyKeyStatusTimestamp(), "بازدید (seen)", "🕒"),
    (types.InputPrivacyKeyProfilePhoto(), "پروفایل (profile)", "🖼️"),
    (types.InputPrivacyKeyForwards(), "فوروارد (forward)", "🔁"),
    (types.InputPrivacyKeyPhoneCall(), "تماس (calls)", "📞"),
    (types.InputPrivacyKeyAddedByPhone(), "دعوت (invite)", "➕"),
    (types.InputPrivacyKeyVoiceMessages(), "ویس (voice)", "🎤"),
]

def privacy_to_text(rules):
    if not rules:
        return "نامشخص"
    if any(rule.__class__.__name__ == "PrivacyValueAllowAll" for rule in rules):
        return "همه"
    if any(rule.__class__.__name__ == "PrivacyValueDisallowAll" for rule in rules):
        return "هیچکس"
    if any(rule.__class__.__name__ == "PrivacyValueAllowContacts" for rule in rules):
        return "مخاطبین"
    return "سفارشی"

async def get_privacy_status(client):
    result = {}
    for key_obj, fa_name, emoji in privacy_keys:
        res = await client.invoke(functions.account.GetPrivacy(key=key_obj))
        result[fa_name] = privacy_to_text(res.rules)
    return result

def format_farsi(status):
    lines = [
        "┏━━━ وضعیت حریم خصوصی شما ━━━┓\n"
    ]
    for (_, fa_name, emoji) in privacy_keys:
        lines.append(f"{emoji} {fa_name}: {status.get(fa_name, 'نامشخص')}")
    lines.append("\n┗━━━━━━━━━━━━━━━━━━━━━━┛")
    return "\n".join(lines)

def format_english(status):
    english_names = [
        ("Phone", "📱"),
        ("Seen", "🕒"),
        ("Profile", "🖼️"),
        ("Forward", "🔁"),
        ("Calls", "📞"),
        ("Invite", "➕"),
        ("Voice", "🎤"),
    ]
    lines = [
        "┏━━━ Your Privacy Status ━━━┓\n"
    ]
    for ((_, fa_name, emoji), (en_name, _)) in zip(privacy_keys, english_names):
        lines.append(f"{emoji} {en_name}: {status.get(fa_name, 'Unknown')}")
    lines.append("\n┗━━━━━━━━━━━━━━━━━━┛")
    return "\n".join(lines)

fa_commands = ["وضعیت حریم"]
en_commands = ["STATUS PRIVACY"]

async def handle_privet(message):
    """
    هندلر وضعیت حریم خصوصی - قابل استفاده در if await handle_privet(m): return
    """
    text = message.text.strip().upper()
    if text in [cmd.upper() for cmd in fa_commands]:
        status = await get_privacy_status(message._client)
        await message.edit_text(format_farsi(status))
        return True
    elif text in [cmd.upper() for cmd in en_commands]:
        status = await get_privacy_status(message._client)
        await message.edit_text(format_english(status))
        return True
    return False