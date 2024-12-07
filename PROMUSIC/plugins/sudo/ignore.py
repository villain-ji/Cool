from pyrogram import filters
from pyrogram.types import Message
from PROMUSIC import app
from PROMUSIC.misc import IGNORED
from config import OWNER_ID, OWNER_USERNAME  # Replace this with the specific owner ID
from PROMUSIC.utils.decorators.language import language
from PROMUSIC.utils.database import add_ignored_user, is_ignored_user, remove_ignored_user, get_ignored_users

# Ignore a user
@app.on_message(filters.command(["ignore"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
async def ignore_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to ignore them.")
    
    ignored_user_id = message.reply_to_message.from_user.id
    if await is_ignored_user(ignored_user_id):
        return await message.reply_text("This user is already ignored.")
    
    await add_ignored_user(ignored_user_id)
    IGNORED.add(ignored_user_id)
    await message.reply_text(f"Ohk Boss Ab {message.reply_to_message.from_user.mention} ko Ignore Karna Start.")


# Stop ignoring a user
@app.on_message(filters.command(["unignore", "rmignore"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
async def unignore_user(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to unignore them.")
    
    ignored_user_id = message.reply_to_message.from_user.id
    if not await is_ignored_user(ignored_user_id):
        return await message.reply_text("This user is not in the ignore list.")
    
    await remove_ignored_user(ignored_user_id)
    IGNORED.discard(ignored_user_id)
    await message.reply_text(f"Ohk Boss Ab {message.reply_to_message.from_user.mention} ko Ignore Nhi Krenge.")

# Check ignored users
@app.on_message(filters.command(["iglist", "ignored"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
async def ignored_list(client, message: Message):
    ignored_users = await get_ignored_users()
    if not ignored_users:
        return await message.reply_text("No users are currently ignored.")
    
    ignored_text = "Ignored Users:\n\n"
    for user_id in ignored_users:
        name = (await app.get_users(user_id)).mention
        ignored_text += f"- {name}\n"
    await message.reply_text(ignored_text)

# Automatically delete messages if an ignored user mentions the owner

MAIN = 7480332189

@app.on_message(filters.group & filters.text & IGNORED)
async def handle_mentions(client, message: Message):
    # Check if message is a reply to the owner

    if message.text.startswith("/"):  # Modify this check if you use a different prefix for commands
        return
    

    mentioned_owner = False
    if message.reply_to_message and message.reply_to_message.from_user.id == OWNER_ID:
        mentioned_owner = True
    
    # Check for mentions in the message text
    owner_mentions = [
    OWNER_USERNAME.lower(),  # Your username in lowercase
    OWNER_USERNAME.upper(),  # Your username in uppercase
    OWNER_USERNAME.capitalize(),
    "Zeo", "zeo", "ZeoXD", "zeoxd", "ZEO", "zEO", "zEo", "ZeO", "ZEOXD", "@ZEOXD", "yasir", "Yasir"
]  # Add variations of your name/username
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mentioned_text = message.text[entity.offset:entity.offset + entity.length]
                if mentioned_text in [f"@{OWNER_USERNAME}"]:
                    mentioned_owner = True

    # Check for name-based mentions in the text
    if any(name in message.text for name in owner_mentions):
        mentioned_owner = True

    if not mentioned_owner:
        return

    # Check if the user is in the ignore list
    is_ignored = await is_ignored_user(message.from_user.id)
    if is_ignored:
        try:
            # Delete the message and send the "Fuck off" message
            await message.delete()
            await message.reply_text(f"Ignore Kiye The ?, {message.from_user.mention} !!\n\n - @ZeoXD")
        except Exception as e:
            print(f"Error in deleting or replying: {e}")
