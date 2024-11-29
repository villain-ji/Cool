from pyrogram import filters
from pyrogram.types import Message
from PROMUSIC import app
from config import OWNER_ID  # Replace this with the specific owner ID
from PROMUSIC.utils.database import add_ignored_user, is_ignored_user, remove_ignored_user, get_ignored_users

# Ignore a user
@app.on_message(filters.command("ignore") & filters.user(OWNER_ID))
async def ignore_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to ignore them.")
    
    ignored_user_id = message.reply_to_message.from_user.id
    if await is_ignored_user(ignored_user_id):
        return await message.reply_text("This user is already ignored.")
    
    await add_ignored_user(ignored_user_id)
    await message.reply_text(f"User {ignored_user_id} is now ignored.")

# Stop ignoring a user
@app.on_message(filters.command("unignore") & filters.user(OWNER_ID))
async def unignore_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to unignore them.")
    
    ignored_user_id = message.reply_to_message.from_user.id
    if not await is_ignored_user(ignored_user_id):
        return await message.reply_text("This user is not in the ignore list.")
    
    await remove_ignored_user(ignored_user_id)
    await message.reply_text(f"User {ignored_user_id} is no longer ignored.")

# Check ignored users
@app.on_message(filters.command("ignoredlist") & filters.user(OWNER_ID))
async def ignored_list(client, message: Message):
    ignored_users = await get_ignored_users()
    if not ignored_users:
        return await message.reply_text("No users are currently ignored.")
    
    ignored_text = "Ignored Users:\n"
    for user_id in ignored_users:
        ignored_text += f"- {user_id}\n"
    await message.reply_text(ignored_text)

# Automatically delete messages if an ignored user mentions the owner
@app.on_message(filters.mentioned)
async def auto_delete_mention(client, message: Message):
    if not message.from_user:
        return

    ignored_user_id = message.from_user.id
    if not await is_ignored_user(ignored_user_id):
        return

    # Check if the message mentions the OWNER_ID
    if OWNER_ID not in [entity.user.id for entity in message.entities if entity.type == "mention"]:
        return

    await message.delete()
    await client.send_message(ignored_user_id, "Fuck off.")
