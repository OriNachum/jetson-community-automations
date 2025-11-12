#!/usr/bin/env python3
"""
Discord Server Data Downloader

This script downloads all public channel information from a Discord server including:
- Channels (organized in folders)
- Threads (saved as separate files)
- Messages (saved as separate files)

Usage:
    python download_discord_data.py
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OUTPUT_DIR = Path("./discord_data")
MAX_MESSAGES_PER_CHANNEL = None  # None = unlimited, set a number to limit


class DiscordDataDownloader:
    """Downloads and organizes Discord server data."""
    
    def __init__(self, token: str, output_dir: Path):
        """
        Initialize the downloader.
        
        Args:
            token: Discord bot token
            output_dir: Directory to save downloaded data
        """
        self.token = token
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup Discord client with necessary intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        self.client = discord.Client(intents=intents)
        self.setup_events()
        
    def setup_events(self):
        """Setup Discord client events."""
        
        @self.client.event
        async def on_ready():
            print(f"✅ Logged in as {self.client.user}")
            print(f"📊 Connected to {len(self.client.guilds)} server(s)")
            
            # Download data from all guilds
            for guild in self.client.guilds:
                await self.download_guild_data(guild)
            
            print("\n✨ Download complete!")
            await self.client.close()
    
    async def download_guild_data(self, guild: discord.Guild):
        """
        Download all data from a guild.
        
        Args:
            guild: Discord guild object
        """
        print(f"\n📁 Processing server: {guild.name} (ID: {guild.id})")
        
        # Create guild directory
        guild_dir = self.output_dir / self.sanitize_filename(guild.name)
        guild_dir.mkdir(exist_ok=True)
        
        # Save guild metadata
        guild_metadata = {
            "id": guild.id,
            "name": guild.name,
            "description": guild.description,
            "member_count": guild.member_count,
            "created_at": guild.created_at.isoformat(),
            "download_date": datetime.utcnow().isoformat()
        }
        
        with open(guild_dir / "server_info.json", "w", encoding="utf-8") as f:
            json.dump(guild_metadata, f, indent=2, ensure_ascii=False)
        
        # Process all text channels (public only)
        channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
        print(f"📢 Found {len(channels)} text channel(s)")
        
        for channel in channels:
            # Skip private channels
            if not channel.permissions_for(guild.me).read_messages:
                print(f"  ⏭️  Skipping private channel: {channel.name}")
                continue
                
            await self.download_channel_data(guild_dir, channel)
    
    async def download_channel_data(self, guild_dir: Path, channel: discord.TextChannel):
        """
        Download all data from a channel.
        
        Args:
            guild_dir: Guild directory path
            channel: Discord text channel object
        """
        print(f"\n  📄 Processing channel: #{channel.name}")
        
        # Create channel directory
        channel_dir = guild_dir / self.sanitize_filename(f"channel_{channel.name}")
        channel_dir.mkdir(exist_ok=True)
        
        # Save channel metadata
        channel_metadata = {
            "id": channel.id,
            "name": channel.name,
            "topic": channel.topic,
            "category": channel.category.name if channel.category else None,
            "created_at": channel.created_at.isoformat(),
            "position": channel.position,
            "nsfw": channel.nsfw
        }
        
        with open(channel_dir / "channel_info.json", "w", encoding="utf-8") as f:
            json.dump(channel_metadata, f, indent=2, ensure_ascii=False)
        
        # Download messages
        await self.download_messages(channel_dir, channel)
        
        # Download threads
        await self.download_threads(channel_dir, channel)
    
    async def download_messages(self, channel_dir: Path, channel: discord.TextChannel):
        """
        Download all messages from a channel.
        
        Args:
            channel_dir: Channel directory path
            channel: Discord text channel object
        """
        messages_dir = channel_dir / "messages"
        messages_dir.mkdir(exist_ok=True)
        
        messages_list = []
        message_count = 0
        
        try:
            async for message in channel.history(limit=MAX_MESSAGES_PER_CHANNEL, oldest_first=True):
                message_count += 1
                
                message_data = self.format_message(message)
                messages_list.append(message_data)
                
                # Save individual message file
                message_filename = f"msg_{message.id}_{self.sanitize_filename(message.created_at.strftime('%Y%m%d_%H%M%S'))}.json"
                with open(messages_dir / message_filename, "w", encoding="utf-8") as f:
                    json.dump(message_data, f, indent=2, ensure_ascii=False)
                
                if message_count % 100 == 0:
                    print(f"    📥 Downloaded {message_count} messages...")
            
            print(f"    ✅ Downloaded {message_count} messages from #{channel.name}")
            
            # Save all messages in a single file as well
            with open(channel_dir / "all_messages.json", "w", encoding="utf-8") as f:
                json.dump(messages_list, f, indent=2, ensure_ascii=False)
                
        except discord.Forbidden:
            print(f"    ❌ No permission to read messages in #{channel.name}")
        except Exception as e:
            print(f"    ❌ Error downloading messages: {e}")
    
    async def download_threads(self, channel_dir: Path, channel: discord.TextChannel):
        """
        Download all threads from a channel.
        
        Args:
            channel_dir: Channel directory path
            channel: Discord text channel object
        """
        threads_dir = channel_dir / "threads"
        threads_dir.mkdir(exist_ok=True)
        
        thread_count = 0
        
        try:
            # Get active threads
            active_threads = channel.threads
            
            # Get archived threads
            archived_threads = []
            async for thread in channel.archived_threads(limit=None):
                archived_threads.append(thread)
            
            all_threads = list(active_threads) + archived_threads
            
            if not all_threads:
                print(f"    ℹ️  No threads found in #{channel.name}")
                return
            
            for thread in all_threads:
                thread_count += 1
                await self.download_thread_data(threads_dir, thread)
            
            print(f"    ✅ Downloaded {thread_count} thread(s) from #{channel.name}")
            
        except discord.Forbidden:
            print(f"    ❌ No permission to read threads in #{channel.name}")
        except Exception as e:
            print(f"    ❌ Error downloading threads: {e}")
    
    async def download_thread_data(self, threads_dir: Path, thread: discord.Thread):
        """
        Download data from a thread.
        
        Args:
            threads_dir: Threads directory path
            thread: Discord thread object
        """
        thread_filename = f"thread_{thread.id}_{self.sanitize_filename(thread.name)}.json"
        
        # Collect thread metadata
        thread_data = {
            "id": thread.id,
            "name": thread.name,
            "created_at": thread.created_at.isoformat() if thread.created_at else None,
            "archived": thread.archived,
            "locked": thread.locked,
            "message_count": thread.message_count,
            "messages": []
        }
        
        # Download thread messages
        try:
            async for message in thread.history(limit=None, oldest_first=True):
                thread_data["messages"].append(self.format_message(message))
        except discord.Forbidden:
            print(f"      ⏭️  No permission to read thread: {thread.name}")
        except Exception as e:
            print(f"      ❌ Error reading thread {thread.name}: {e}")
        
        # Save thread data
        with open(threads_dir / thread_filename, "w", encoding="utf-8") as f:
            json.dump(thread_data, f, indent=2, ensure_ascii=False)
    
    def format_message(self, message: discord.Message) -> dict:
        """
        Format a Discord message into a dictionary.
        
        Args:
            message: Discord message object
            
        Returns:
            Dictionary containing message data
        """
        return {
            "id": message.id,
            "author": {
                "id": message.author.id,
                "name": message.author.name,
                "display_name": message.author.display_name,
                "bot": message.author.bot
            },
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "edited_at": message.edited_at.isoformat() if message.edited_at else None,
            "attachments": [
                {
                    "id": att.id,
                    "filename": att.filename,
                    "url": att.url,
                    "size": att.size
                }
                for att in message.attachments
            ],
            "embeds": [
                {
                    "title": embed.title,
                    "description": embed.description,
                    "url": embed.url,
                    "color": embed.color.value if embed.color else None
                }
                for embed in message.embeds
            ],
            "reactions": [
                {
                    "emoji": str(reaction.emoji),
                    "count": reaction.count
                }
                for reaction in message.reactions
            ],
            "pinned": message.pinned,
            "mention_everyone": message.mention_everyone,
            "mentions": [
                {
                    "id": user.id,
                    "name": user.name
                }
                for user in message.mentions
            ],
            "jump_url": message.jump_url
        }
    
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Sanitize a string to be used as a filename.
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized string safe for filenames
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Limit length
        max_length = 200
        if len(name) > max_length:
            name = name[:max_length]
        
        return name.strip()
    
    async def run(self):
        """Start the download process."""
        if not self.token:
            raise ValueError("DISCORD_BOT_TOKEN not found in .env file")
        
        print("🤖 Starting Discord Data Downloader...")
        print(f"📂 Output directory: {self.output_dir.absolute()}")
        
        await self.client.start(self.token)


async def main():
    """Main entry point."""
    downloader = DiscordDataDownloader(
        token=DISCORD_BOT_TOKEN,
        output_dir=OUTPUT_DIR
    )
    
    try:
        await downloader.run()
    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
