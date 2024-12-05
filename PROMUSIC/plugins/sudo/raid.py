import time
from pyrogram import Client, filters
from PROMUSIC import app
from PROMUSIC.misc import SUDOERS


@app.on_message(filters.command("spamm", prefixes="/") & SUDOERS)
def spam_command(client, message):
    # Ensure the command is used in reply to a message
    if not message.reply_to_message:
        message.reply_text("Reply to a user's message to spam.")
        return

    # Parse command arguments (e.g., "/spam 20 Hello")
    command_args = message.text.split(maxsplit=2)
    if len(command_args) < 3:
        message.reply_text("Usage: `/spam <count> <message>`")
        return

    # Extract count and message
    try:
        count = int(command_args[1])
        if count <= 0:
            raise ValueError
    except ValueError:
        message.reply_text("Please provide a valid positive number for the count.")
        return

    spam_text = command_args[2]
    user_mention = message.reply_to_message.from_user.mention(style="md")

    # Start spamming
    for _ in range(count):
        try:
            message.chat.send_message(f"{user_mention} {spam_text}")
            time.sleep(0.5)  # Delay between messages to avoid being rate-limited
        except Exception as e:
            print(f"Error while sending spam: {e}")
            break
