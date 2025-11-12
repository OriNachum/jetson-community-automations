# Discord Server Data Downloader

This automation script downloads all public channel information from your Discord server, organized into a structured folder hierarchy.

## Features

- ✅ Downloads all public text channels
- ✅ Saves each message as a separate JSON file
- ✅ Downloads all threads (active and archived)
- ✅ Saves thread data with all messages
- ✅ Captures message metadata (author, timestamps, reactions, attachments, embeds)
- ✅ Organizes data into folders per channel
- ✅ Skips private channels automatically
- ✅ Creates comprehensive metadata files

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file (or use the existing one) with your Discord bot token:

```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

### 3. Create Discord Bot

If you haven't created a Discord bot yet:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Copy the bot token and add it to your `.env` file
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot`
8. Select bot permissions:
   - ✅ Read Messages/View Channels
   - ✅ Read Message History
9. Copy the generated URL and invite the bot to your server

## Usage

Run the script:

```bash
python download_discord_data.py
```

The script will:
1. Connect to Discord using your bot token
2. Process all servers the bot has access to
3. Download all public channels, threads, and messages
4. Save everything to the `discord_data` folder

## Output Structure

```
discord_data/
├── ServerName/
│   ├── server_info.json                    # Server metadata
│   ├── channel_ChannelName/
│   │   ├── channel_info.json               # Channel metadata
│   │   ├── all_messages.json               # All messages in one file
│   │   ├── messages/
│   │   │   ├── msg_123456_20251112_143022.json
│   │   │   ├── msg_123457_20251112_143045.json
│   │   │   └── ...
│   │   └── threads/
│   │       ├── thread_789012_ThreadName.json
│   │       └── ...
│   └── channel_AnotherChannel/
│       └── ...
```

## Data Format

### Server Info
```json
{
  "id": 123456789,
  "name": "Server Name",
  "description": "Server description",
  "member_count": 150,
  "created_at": "2023-01-01T00:00:00",
  "download_date": "2025-11-12T14:30:00"
}
```

### Channel Info
```json
{
  "id": 987654321,
  "name": "general",
  "topic": "General discussion",
  "category": "Text Channels",
  "created_at": "2023-01-01T00:00:00",
  "position": 0,
  "nsfw": false
}
```

### Message
```json
{
  "id": 111222333,
  "author": {
    "id": 444555666,
    "name": "username",
    "display_name": "Display Name",
    "bot": false
  },
  "content": "Message content",
  "created_at": "2025-11-12T14:30:00",
  "edited_at": null,
  "attachments": [],
  "embeds": [],
  "reactions": [],
  "pinned": false,
  "mention_everyone": false,
  "mentions": [],
  "jump_url": "https://discord.com/channels/..."
}
```

### Thread
```json
{
  "id": 777888999,
  "name": "Thread Name",
  "created_at": "2025-11-12T14:30:00",
  "archived": false,
  "locked": false,
  "message_count": 15,
  "messages": [
    // Array of message objects
  ]
}
```

## Configuration Options

You can modify the script to customize behavior:

- **MAX_MESSAGES_PER_CHANNEL**: Set to a number to limit messages downloaded per channel (default: `None` = unlimited)
- **OUTPUT_DIR**: Change the output directory path (default: `./discord_data`)

## Notes

- The script only downloads **public channels** that the bot has access to
- Private channels and DMs are automatically skipped
- The bot needs appropriate permissions to read message history
- Large servers may take significant time to download
- Attachment files are not downloaded, only metadata and URLs are saved

## Troubleshooting

### "DISCORD_BOT_TOKEN not found in .env file"
Make sure your `.env` file exists and contains the bot token.

### "No permission to read messages"
Ensure your bot has the "Read Message History" permission in the server.

### "Forbidden" errors
The bot lacks necessary permissions. Check the bot's role permissions in Discord.

## License

This script is part of the jetson-community-automations project.
