# 🌹 LoveBot — Romantic Telegram Bot

A full-featured Telegram bot with **romantic AI chat**, **group moderation**, and **music playback** — inspired by Rose Bot.

---

## ✨ Features

| Feature | Details |
|---|---|
| 💕 Romantic Chat | Chat romantically in DM or groups (when mentioned) |
| 🛡️ Group Admin | Ban, kick, mute, warn, pin, promote, filters & more |
| 🎵 Music | Queue-based music with YouTube search via yt-dlp |
| 🌹 Love Commands | `/love`, `/flirt`, `/hug`, `/kiss`, `/poem`, `/compliment` |
| 📊 Info Commands | `/id`, `/info`, `/stats` |

---

## 🚀 Setup

### 1. Get a Bot Token
1. Open Telegram and message **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **token** you receive

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
Edit `config.py`:
```python
BOT_TOKEN = "YOUR_TOKEN_FROM_BOTFATHER"
OWNER_ID   = 123456789  # Your Telegram user ID (from @userinfobot)
```

Or use environment variables:
```bash
export BOT_TOKEN="your_token_here"
```

### 4. Run
```bash
python bot.py
```

---

## 🛡️ Admin Commands

Make the bot an **admin** in your group first, then:

| Command | Description |
|---|---|
| `/ban @user [reason]` | Ban a user |
| `/unban @user` | Unban a user |
| `/kick @user [reason]` | Kick a user |
| `/mute @user` | Mute a user |
| `/unmute @user` | Unmute a user |
| `/warn @user [reason]` | Warn (auto-ban at 3 warns) |
| `/warns @user` | Check warning count |
| `/pin` | Pin replied-to message |
| `/unpin` | Unpin all messages |
| `/promote @user` | Promote to admin |
| `/demote @user` | Remove admin |
| `/lock` | Lock chat (members can't send) |
| `/unlock` | Unlock chat |
| `/purge` | Delete messages from reply onward |
| `/filters` | List word filters |
| `/filters add [word]` | Add a word filter |
| `/filters remove [word]` | Remove a word filter |

---

## 💕 Romantic Commands

| Command | Description |
|---|---|
| `/love` | Get a love message |
| `/flirt` | Receive a flirt line |
| `/hug` | Virtual hug 🤗 |
| `/kiss` | Virtual kiss 💋 |
| `/poem` | A romantic poem 📜 |
| `/compliment` | A sweet compliment |

The bot also responds romantically when:
- You message it in **private chat**
- You **@mention** it in a group
- You **reply** to its messages

---

## 🎵 Music Commands

| Command | Description |
|---|---|
| `/play [song or URL]` | Add to queue & play |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/skip` | Skip current song |
| `/stop` | Stop & clear queue |
| `/queue` | View the song queue |
| `/np` | Now playing info |
| `/volume [0-200]` | Set volume |

> **Note:** For actual audio in voice chats, install `pytgcalls` and join a voice chat before using `/play`. The bot will manage the queue regardless.

---

## 📁 Project Structure

```
lovebot/
├── bot.py          # Main bot — all handlers
├── config.py       # Token, owner ID, response data
├── romantic.py     # Romantic responses & AI chat logic
├── admin.py        # Warning & word filter tracking
├── music.py        # Queue management & playback control
├── requirements.txt
└── README.md
```

---

## 🔧 Permissions Needed

When adding to a group, give the bot these admin permissions:
- ✅ Delete messages
- ✅ Ban users
- ✅ Restrict members
- ✅ Pin messages
- ✅ Invite users via link
- ✅ Manage voice chats (for music)

---

## 💡 Tips

- **Anti-spam**: Use `/filters add [word]` to auto-delete messages with bad words
- **Auto-ban**: Users get auto-banned after 3 warnings
- **Music**: Works best with YouTube links or song names with yt-dlp installed
- **Private chat**: Bot is fully romantic in DMs — no commands needed, just chat!

---

## 🌹 Made with love
