# Overwatch Genji Parkour Discord Bot

> A specialized Discord bot for the Overwatch Genji Parkour community.
> If you're interested, Come and join us via [this link](https://discord.gg/CqS2sJaGd)

[한국어](README.ko.md)

---

## Overview

This bot helps manage the Genji Parkour community on Discord. 
It provides parkour code registration and browsing, a clear board for recording challenge completions, and an anonymous messaging system.

## Features

### Code Management (`/code`)
- **Add** a parkour code with map, difficulty, checkpoint count, description, guide URL, and creator
- **Update** an existing code's information
- **Delete** a code by its workshop code
- **Browse** codes with paginated embed views, filterable by map and difficulty

### Clear Board (`/clear`)
- **Submit** a clear record for a parkour code
- **Browse** the clear board with pagination
- **Authenticate** to post clears (role-gated)
- **Cancel** a pending clear submission
- Admin tools to **approve** or **reject** submissions with a modal reason

### Map Management (`/map`)
- **Add** a new map to the supported map list
- **Edit** an existing map's name
- **Remove** a map from the list

### Anonymous Chat (`/anonymous`)
- **Send** an anonymous message to a designated channel
- **Reply** to an anonymous message thread
- **Block** a user from sending anonymous messages (moderator only)
- Log view for moderators to trace anonymous message authors

## Setup

### Requirements

- Python 3.12+
- A Discord bot token
- SQLite (bundled, no install needed)

### Environment Variables

Create a `.env` file in the project root:

```env
SQLITE_DB_PATH=./db/data.db
DISCORD_BOT_TOKEN=your_bot_token_here

DISCORD_SERVER_ID=your_server_id
LOG_CHANNEL_ID=your_log_channel_id
CLEAR_CHANNEL_ID=your_clear_submission_channel_id
CLEAR_PUB_CHANNEL_ID=your_clear_public_channel_id
```

### Install & Run

```bash
pip install -r requirements.txt
python main.py
```
