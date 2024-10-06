import asyncio
import datetime
from PROMUSIC import app
from pyrogram import Client
from config import START_IMG_URL, IMG_URL
from PROMUSIC.utils.database import get_served_chats, get_served_users
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# Specify the channel ID and message ID you want to forward
CHANNEL_ID = -1002231749322  # Replace with your channel ID
MESSAGE_ID = 26  # Replace with the actual message ID from the channel

async def forward_message_to_chats():
    try:
        chats = await get_served_chats()
        users = await get_served_users()

        # Forward message to all chats
        for chat in chats:
            chat_id = int(chat["chat_id"])
            try:
                await app.forward_messages(chat_id, CHANNEL_ID, MESSAGE_ID)
                await asyncio.sleep(0.2)  # Sleep for 0.2 seconds to avoid FloodWait
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue

        # Forward message to all users
        for user in users:
            user_id = int(user["user_id"])
            try:
                await app.forward_messages(user_id, CHANNEL_ID, MESSAGE_ID)
                await asyncio.sleep(0.2)  # Sleep for 0.2 seconds to avoid FloodWait
            except FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue

    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats

async def continuous_broadcast():
    while True:
        await forward_message_to_chats()  # Call the forward message function
        await asyncio.sleep(82800)  # Sleep (82800 seconds) between next broadcast

# Start the continuous broadcast loop
asyncio.create_task(continuous_broadcast())
