"""
LoveBot - A Romantic Telegram Bot with Admin & Music Features
Inspired by Rose Bot functionality
"""

import logging
import os
import asyncio
import random
from datetime import datetime

from telegram import (
    Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.error import TelegramError

from config import BOT_TOKEN, OWNER_ID, ROMANTIC_RESPONSES, FLIRT_LINES
from music import MusicPlayer
from admin import AdminManager
from romantic import RomanticChat

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global instances
music_player = MusicPlayer()
admin_manager = AdminManager()
romantic_chat = RomanticChat()


# ─────────────────────────────────────────────
#  START / HELP
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name

    keyboard = [
        [InlineKeyboardButton("💕 Chat with me", callback_data="romantic"),
         InlineKeyboardButton("🎵 Music", callback_data="music_help")],
        [InlineKeyboardButton("🛡️ Admin Cmds", callback_data="admin_help"),
         InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = (
        f"*Hey {name}! 💖*\n\n"
        "I'm *LoveBot* — your romantic companion, group guardian & music player!\n\n"
        "✨ *What I can do:*\n"
        "💕 Chat romantically with you\n"
        "🛡️ Manage & moderate your group\n"
        "🎵 Play music in voice chats\n"
        "🌹 Send love & compliments\n\n"
        "_Add me to your group and make me admin to unlock all features!_"
    )
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *LoveBot Commands*\n\n"
        "━━━━ 💕 *Romantic* ━━━━\n"
        "/love — get a love message\n"
        "/flirt — receive a flirt line\n"
        "/hug — virtual hug 🤗\n"
        "/kiss — virtual kiss 💋\n"
        "/poem — romantic poem 📜\n"
        "/compliment — sweet compliment\n\n"
        "━━━━ 🛡️ *Admin* ━━━━\n"
        "/ban @user — ban a user\n"
        "/unban @user — unban a user\n"
        "/kick @user — kick from group\n"
        "/mute @user [time] — mute user\n"
        "/unmute @user — unmute user\n"
        "/warn @user — warn a user\n"
        "/warns @user — check warnings\n"
        "/pin — pin a message\n"
        "/unpin — unpin message\n"
        "/promote @user — promote to admin\n"
        "/demote @user — demote admin\n"
        "/lock — lock the chat\n"
        "/unlock — unlock the chat\n"
        "/purge — delete messages\n"
        "/filters — manage word filters\n\n"
        "━━━━ 🎵 *Music* ━━━━\n"
        "/play [song] — play a song\n"
        "/pause — pause music\n"
        "/resume — resume music\n"
        "/skip — skip current song\n"
        "/stop — stop music\n"
        "/queue — view song queue\n"
        "/volume [0-200] — set volume\n"
        "/np — now playing\n\n"
        "━━━━ 📊 *Info* ━━━━\n"
        "/id — get your user ID\n"
        "/info @user — user information\n"
        "/stats — group statistics\n"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  CALLBACK QUERIES
# ─────────────────────────────────────────────

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "romantic":
        response = romantic_chat.get_random_love()
        await query.edit_message_text(f"💕 {response}\n\n_Use /love, /flirt, /poem for more!_",
                                       parse_mode=ParseMode.MARKDOWN)
    elif data == "music_help":
        text = ("🎵 *Music Commands*\n\n"
                "/play [song name or YouTube URL]\n"
                "/pause — pause playback\n"
                "/resume — resume playback\n"
                "/skip — next song\n"
                "/stop — stop & clear queue\n"
                "/queue — view queue\n"
                "/np — now playing\n"
                "/volume [0-200] — adjust volume\n\n"
                "_Note: I must be in a voice chat to play music._")
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    elif data == "admin_help":
        text = ("🛡️ *Admin Commands*\n\n"
                "Make me admin in your group to use:\n"
                "/ban /unban /kick /mute /unmute\n"
                "/warn /warns /pin /promote /demote\n"
                "/lock /unlock /purge /filters\n\n"
                "_I'll keep your group safe & beautiful! 🌹_")
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    elif data == "help":
        await query.edit_message_text("Use /help for the full command list! 💖",
                                       parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  ROMANTIC COMMANDS
# ─────────────────────────────────────────────

async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    msg = romantic_chat.get_love_message(name)
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def flirt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    line = romantic_chat.get_flirt(name)
    await update.message.reply_text(line, parse_mode=ParseMode.MARKDOWN)


async def hug_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    hugs = [
        f"*{name}*, here's a big warm hug just for you! 🤗💕",
        f"Wrapping my arms around you, *{name}*! 🤗✨",
        f"You deserve all the hugs in the world, *{name}*! 🤗🌹",
        f"*{name}*, I'm sending you the tightest virtual hug! 💖🤗",
    ]
    await update.message.reply_text(random.choice(hugs), parse_mode=ParseMode.MARKDOWN)


async def kiss_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    kisses = [
        f"*{name}*, a soft kiss on your forehead 💋✨",
        f"Mwah! 💋 Sending all my love to you, *{name}*!",
        f"A sweet kiss just for you, *{name}* 💋🌹",
        f"*{name}*... 💋 You make my heart skip a beat! 💓",
    ]
    await update.message.reply_text(random.choice(kisses), parse_mode=ParseMode.MARKDOWN)


async def poem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    poem = romantic_chat.get_poem(name)
    await update.message.reply_text(poem, parse_mode=ParseMode.MARKDOWN)


async def compliment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    compliment = romantic_chat.get_compliment(name)
    await update.message.reply_text(compliment, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  INFO COMMANDS
# ─────────────────────────────────────────────

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    text = (f"👤 *Your Info*\n"
            f"ID: `{user.id}`\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username or 'none'}\n\n"
            f"💬 *Chat Info*\n"
            f"Chat ID: `{chat.id}`\n"
            f"Type: {chat.type}")
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = None
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        # try mention
        entities = update.message.entities or []
        for entity in entities:
            if entity.type == "mention":
                username = update.message.text[entity.offset+1:entity.offset+entity.length]
                await update.message.reply_text(
                    f"ℹ️ Use reply to get info, or check @{username}'s profile directly.",
                    parse_mode=ParseMode.MARKDOWN)
                return
    
    if not target:
        target = update.effective_user

    warn_count = admin_manager.get_warn_count(target.id, update.effective_chat.id)
    text = (f"👤 *User Info*\n"
            f"Name: {target.full_name}\n"
            f"ID: `{target.id}`\n"
            f"Username: @{target.username or 'none'}\n"
            f"⚠️ Warnings: {warn_count}/3")
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        count = await context.bot.get_chat_member_count(chat.id)
    except:
        count = "N/A"
    text = (f"📊 *Group Stats*\n"
            f"Group: {chat.title}\n"
            f"ID: `{chat.id}`\n"
            f"Members: {count}\n"
            f"Type: {chat.type}\n"
            f"Songs played today: {music_player.songs_played}")
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  ADMIN COMMANDS
# ─────────────────────────────────────────────

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    chat = update.effective_chat
    if chat.type == "private":
        return True
    try:
        member = await context.bot.get_chat_member(chat.id, user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False


async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get target user from reply or mention."""
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    elif context.args:
        try:
            uid = int(context.args[0])
            return await context.bot.get_chat_member(update.effective_chat.id, uid)
        except:
            pass
    return None


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ You need to be an admin to use this!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to a user or provide their ID to ban.")
        return
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason given"
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(
            f"🚫 *{target.full_name}* has been banned!\n📝 Reason: {reason}",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to user or provide ID.")
        return
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(
            f"✅ *{target.full_name}* has been unbanned! Welcome back 🌹",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def kick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to user or provide ID.")
        return
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason given"
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(
            f"👢 *{target.full_name}* has been kicked!\n📝 Reason: {reason}",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to user or provide ID.")
        return
    try:
        perms = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, perms)
        await update.message.reply_text(
            f"🔇 *{target.full_name}* has been muted! 🤫",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to user or provide ID.")
        return
    try:
        perms = ChatPermissions(
            can_send_messages=True, can_send_media_messages=True,
            can_send_other_messages=True, can_add_web_page_previews=True
        )
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, perms)
        await update.message.reply_text(
            f"🔊 *{target.full_name}* can speak again! 🎉",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to user to warn them.")
        return
    reason = " ".join(context.args[1:]) if context.args else "No reason"
    chat_id = update.effective_chat.id
    count = admin_manager.add_warn(target.id, chat_id)
    
    if count >= 3:
        try:
            await context.bot.ban_chat_member(chat_id, target.id)
            await update.message.reply_text(
                f"⛔ *{target.full_name}* has been banned after 3 warnings!",
                parse_mode=ParseMode.MARKDOWN)
            admin_manager.reset_warns(target.id, chat_id)
        except TelegramError as e:
            await update.message.reply_text(f"❌ Auto-ban failed: {e}")
    else:
        await update.message.reply_text(
            f"⚠️ *{target.full_name}* has been warned! ({count}/3)\n📝 Reason: {reason}",
            parse_mode=ParseMode.MARKDOWN)


async def warns_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = await get_target_user(update, context)
    if not target:
        target = update.effective_user
    count = admin_manager.get_warn_count(target.id, update.effective_chat.id)
    await update.message.reply_text(
        f"⚠️ *{target.full_name}* has *{count}/3* warnings.",
        parse_mode=ParseMode.MARKDOWN)


async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("❓ Reply to a message to pin it.")
        return
    try:
        await context.bot.pin_chat_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id)
        await update.message.reply_text("📌 Message pinned!")
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def unpin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    try:
        await context.bot.unpin_all_chat_messages(update.effective_chat.id)
        await update.message.reply_text("📌 All messages unpinned!")
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def promote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to a user to promote.")
        return
    try:
        await context.bot.promote_chat_member(
            update.effective_chat.id, target.id,
            can_delete_messages=True, can_restrict_members=True,
            can_pin_messages=True, can_invite_users=True
        )
        await update.message.reply_text(
            f"⭐ *{target.full_name}* has been promoted to admin! 🎉",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def demote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❓ Reply to a user to demote.")
        return
    try:
        await context.bot.promote_chat_member(
            update.effective_chat.id, target.id,
            can_delete_messages=False, can_restrict_members=False,
            can_pin_messages=False, can_invite_users=False
        )
        await update.message.reply_text(
            f"📉 *{target.full_name}* has been demoted.",
            parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def lock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    try:
        perms = ChatPermissions(can_send_messages=False)
        await context.bot.set_chat_permissions(update.effective_chat.id, perms)
        await update.message.reply_text("🔒 Chat has been locked! Only admins can send messages.")
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    try:
        perms = ChatPermissions(
            can_send_messages=True, can_send_media_messages=True,
            can_send_other_messages=True, can_add_web_page_previews=True
        )
        await context.bot.set_chat_permissions(update.effective_chat.id, perms)
        await update.message.reply_text("🔓 Chat has been unlocked! Everyone can speak again 🎉")
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: {e}")


async def purge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("❓ Reply to a message to purge from there.")
        return
    start_id = update.message.reply_to_message.message_id
    end_id = update.message.message_id
    deleted = 0
    for msg_id in range(start_id, end_id + 1):
        try:
            await context.bot.delete_message(update.effective_chat.id, msg_id)
            deleted += 1
        except:
            pass
    note = await update.message.reply_text(f"🗑️ Purged {deleted} messages!")
    await asyncio.sleep(3)
    try:
        await note.delete()
    except:
        pass


# ─────────────────────────────────────────────
#  MUSIC COMMANDS
# ─────────────────────────────────────────────

async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🎵 Usage: `/play [song name or YouTube URL]`\n\nExample: `/play Shape of You`",
            parse_mode=ParseMode.MARKDOWN)
        return
    query = " ".join(context.args)
    result = await music_player.add_to_queue(query, update.effective_user.first_name)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.pause()
    await update.message.reply_text(result)


async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.resume()
    await update.message.reply_text(result)


async def skip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.skip()
    await update.message.reply_text(result)


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.stop()
    await update.message.reply_text(result)


async def queue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.get_queue()
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


async def now_playing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = music_player.now_playing()
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


async def volume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/volume [0-200]`", parse_mode=ParseMode.MARKDOWN)
        return
    try:
        vol = int(context.args[0])
        result = music_player.set_volume(vol)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Please provide a number between 0 and 200.")


# ─────────────────────────────────────────────
#  FILTERS COMMAND
# ─────────────────────────────────────────────

async def filters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Admins only!")
        return
    
    if not context.args:
        filters_list = admin_manager.get_filters(update.effective_chat.id)
        if not filters_list:
            await update.message.reply_text("📋 No active word filters.")
            return
        text = "📋 *Active Filters:*\n" + "\n".join(f"• `{f}`" for f in filters_list)
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return

    action = context.args[0].lower()
    if action == "add" and len(context.args) > 1:
        word = context.args[1].lower()
        admin_manager.add_filter(update.effective_chat.id, word)
        await update.message.reply_text(f"✅ Filter added: `{word}`", parse_mode=ParseMode.MARKDOWN)
    elif action == "remove" and len(context.args) > 1:
        word = context.args[1].lower()
        admin_manager.remove_filter(update.effective_chat.id, word)
        await update.message.reply_text(f"✅ Filter removed: `{word}`", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(
            "Usage:\n`/filters` — list filters\n"
            "`/filters add [word]` — add filter\n"
            "`/filters remove [word]` — remove filter",
            parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  MESSAGE HANDLER — Romantic AI Chat + Filter
# ─────────────────────────────────────────────

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    
    # Check word filters
    active_filters = admin_manager.get_filters(chat_id)
    for word in active_filters:
        if word in text:
            try:
                await update.message.delete()
                warn_count = admin_manager.add_warn(update.effective_user.id, chat_id)
                await context.bot.send_message(
                    chat_id,
                    f"⚠️ Message deleted — filtered word detected.\n"
                    f"*{update.effective_user.first_name}* now has {warn_count}/3 warnings.",
                    parse_mode=ParseMode.MARKDOWN)
            except:
                pass
            return

    # Respond if mentioned/replied to or in private chat
    bot_username = context.bot.username
    is_private = update.effective_chat.type == "private"
    is_mentioned = f"@{bot_username}".lower() in text if bot_username else False
    is_reply = (update.message.reply_to_message and
                update.message.reply_to_message.from_user and
                update.message.reply_to_message.from_user.username == bot_username)

    if is_private or is_mentioned or is_reply:
        # Clean the message
        clean_text = text.replace(f"@{bot_username}".lower(), "").strip() if bot_username else text
        name = update.effective_user.first_name
        response = romantic_chat.get_ai_response(clean_text, name, update.effective_user.id)
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    token = os.getenv("BOT_TOKEN", BOT_TOKEN)
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN not set! Edit config.py or set BOT_TOKEN env variable.")
        return

    app = Application.builder().token(token).build()

    # Start & Help
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Romantic
    app.add_handler(CommandHandler("love", love_command))
    app.add_handler(CommandHandler("flirt", flirt_command))
    app.add_handler(CommandHandler("hug", hug_command))
    app.add_handler(CommandHandler("kiss", kiss_command))
    app.add_handler(CommandHandler("poem", poem_command))
    app.add_handler(CommandHandler("compliment", compliment_command))

    # Info
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("stats", stats_command))

    # Admin
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("unban", unban_command))
    app.add_handler(CommandHandler("kick", kick_command))
    app.add_handler(CommandHandler("mute", mute_command))
    app.add_handler(CommandHandler("unmute", unmute_command))
    app.add_handler(CommandHandler("warn", warn_command))
    app.add_handler(CommandHandler("warns", warns_command))
    app.add_handler(CommandHandler("pin", pin_command))
    app.add_handler(CommandHandler("unpin", unpin_command))
    app.add_handler(CommandHandler("promote", promote_command))
    app.add_handler(CommandHandler("demote", demote_command))
    app.add_handler(CommandHandler("lock", lock_command))
    app.add_handler(CommandHandler("unlock", unlock_command))
    app.add_handler(CommandHandler("purge", purge_command))
    app.add_handler(CommandHandler("filters", filters_command))

    # Music
    app.add_handler(CommandHandler("play", play_command))
    app.add_handler(CommandHandler("pause", pause_command))
    app.add_handler(CommandHandler("resume", resume_command))
    app.add_handler(CommandHandler("skip", skip_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("queue", queue_command))
    app.add_handler(CommandHandler("np", now_playing_command))
    app.add_handler(CommandHandler("volume", volume_command))

    # Message handler (romantic AI + filter)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("🌹 LoveBot is running!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
