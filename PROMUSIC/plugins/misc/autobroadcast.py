import asyncio
import datetime
from PROMUSIC import app
from pyrogram import Client
from config import START_IMG_URL, IMG_URL
from PROMUSIC.utils.database import get_served_chats, get_served_users
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait


MESSAGE = f"""**๏ ᴛʜɪs ɪs ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ + ᴍᴀɴᴀɢᴇᴍɴᴇᴛ ʀᴏʙᴏᴛ 💗. 💌

🎧 ᴘʟᴀʏ + ᴠᴘʟᴀʏ + ᴄᴘʟᴀʏ 🎧

➥ sᴜᴘᴘᴏʀᴛᴇᴅ ᴡᴇʟᴄᴏᴍᴇ - ʟᴇғᴛ ɴᴏᴛɪᴄᴇ, ᴛᴀɢᴀʟʟ, ᴠᴄᴛᴀɢ, ʙᴀɴ - ᴍᴜᴛᴇ, sʜᴀʏʀɪ, ʟʏʀɪᴄs, sᴏɴɢ - ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅ, ᴇᴛᴄ... 💕

🔐ᴜꜱᴇ » [/start](https://t.me/{app.username}?start=true) ᴛᴏ ᴄʜᴇᴄᴋ ʙᴏᴛ

➲ ʙᴏᴛ :** @{app.username}"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
        ]
    ]
)

CELEBRATION_VID_URL = "https://github.com/doraemon890/ANNIE-X-MUSIC/assets/155803358/dcbec346-bb98-4818-9a1c-683e9c3107b0"

BD_VID = "https://telegra.ph/file/943bb99829ec526c3f99a.mp4"

async def send_message_to_chats():
    try:
        chats = await get_served_chats()
        users = await get_served_users()

        # Send message to chats
        for chat in chats:
            chat_id = int(chat["chat_id"])
            try:
                await app.send_photo(chat_id, photo=IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                await asyncio.sleep(0.2)  # Sleep for 0.2 seconds to avoid FloodWait
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue

        # Send message to users
        for user in users:
            user_id = int(user["user_id"])
            try:
                await app.send_photo(user_id, photo=IMG_URL, caption=MESSAGE, reply_markup=BUTTON)
                await asyncio.sleep(0.2)  # Sleep for 0.2 seconds to avoid FloodWait
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue

    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats
async def continuous_broadcast():
    while True:
        await send_message_to_chats()
        await asyncio.sleep(82800)  # Sleep (82800 seconds) between next broadcast

# Start the continuous broadcast loop
# asyncio.create_task(continuous_broadcast())