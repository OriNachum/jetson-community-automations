# Discord Bot Permissions Guide

This document outlines the required permissions and setup for the Discord Data Downloader bot.

## Required Discord Bot Permissions

### Bot Intents (Required in Discord Developer Portal)

The bot requires the following **Privileged Gateway Intent** to be enabled in the Discord Developer Portal:

1. **Message Content Intent** - Required to read message content

**Note:** Server Members Intent is NOT required. The bot only needs to read messages, not access member lists.

**How to enable:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Navigate to the "Bot" section
4. Scroll down to "Privileged Gateway Intents"
5. Enable **MESSAGE CONTENT INTENT**
6. Click "Save Changes"

### Bot Permissions (Numerical Value: 67584)

The bot needs the following permissions when added to a server:

#### Required Text Permissions
- **Read Messages/View Channels** - Access to view channels
- **Read Message History** - Required to download historical messages
- **Read Message Content** - Required to access message content (via Message Content Intent)

#### Optional Permissions
- **Send Messages** - Not required for downloading data. The bot operates in read-only mode and doesn't need to send messages. If you encounter permission errors, this permission is not the cause.

## Bot Invite URL

Use the following URL template to invite the bot to your server (replace `YOUR_CLIENT_ID` with your bot's client ID):

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=67584&scope=bot
```

### Permission Breakdown
- `67584` = Read Messages + Read Message History

## Environment Setup

### Required Environment Variables

Create a `.env` file in the `discord/` directory with the following:

```env
DISCORD_BOT_TOKEN=your_bot_token_here
```

**Where to find your bot token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Navigate to the "Bot" section
4. Click "Reset Token" or "Copy" to get your bot token
5. **⚠️ Keep this token secret! Never commit it to version control.**

## Script Behavior

### What the Bot Can Access

The script will download:
- ✅ **Public text channels** - All channels the bot has permission to view
- ✅ **Channel messages** - All message history in accessible channels
- ✅ **Threads** - Both active and archived threads
- ✅ **Message metadata** - Authors, timestamps, reactions, embeds, attachments URLs
- ✅ **Server information** - Server name, description, member count

### What the Bot Cannot/Will Not Access

- ❌ **Private channels** - Channels the bot doesn't have permission to view are automatically skipped
- ❌ **DMs** - Direct messages are not accessed
- ❌ **Voice channels** - Only text channels are downloaded
- ❌ **Attachment files** - Only URLs are saved, not the actual files

### Privacy Considerations

- The bot only accesses channels it has explicit permission to read
- All downloaded data is stored locally in the `discord_data/` directory
- The script displays which channels are being processed and skips private ones
- Message content includes all public messages visible to the bot

## Troubleshooting

### Common Issues

#### "No permission to read messages"
- **Solution**: Ensure the bot role has "View Channel" and "Read Message History" permissions for the channel
- Check channel-specific permission overrides that might block bot access

#### "Privileged intent provided is not enabled or whitelisted"
- **Solution**: Enable the required intents in the Discord Developer Portal (see above)

#### "Invalid token"
- **Solution**: Verify your `DISCORD_BOT_TOKEN` in the `.env` file is correct
- Try regenerating the token in the Developer Portal

#### Bot can't see certain channels
- **Solution**: Check the bot's role permissions in server settings
- Ensure the bot role is positioned high enough in the role hierarchy
- Verify channel-specific permission overrides

## Security Best Practices

1. **Token Security**
   - Never share your bot token
   - Never commit `.env` files to version control
   - Regenerate token immediately if compromised

2. **Permission Principle**
   - Only grant minimum required permissions
   - Regularly audit bot permissions
   - Remove bot from servers when not needed

3. **Data Handling**
   - Downloaded data contains user information - handle responsibly
   - Comply with Discord's Terms of Service and Developer Terms
   - Consider GDPR/privacy regulations if applicable
   - Secure the `discord_data/` directory appropriately

## Rate Limits

Discord enforces rate limits on API requests:
- The script uses `discord.py` which handles rate limiting automatically
- Large servers may take significant time to download
- The script processes channels sequentially to avoid hitting limits

## Support

For issues related to:
- **Discord API**: Check [Discord Developer Documentation](https://discord.com/developers/docs)
- **discord.py library**: Visit [discord.py Documentation](https://discordpy.readthedocs.io/)
- **This script**: Review the README and script comments
