import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

queues = {}
loop_mode = {}
skip_votes = {}
current_song = {}
volumes = {}

async def auto_disconnect_check(ctx):
    voice = ctx.voice_client
    if voice and voice.channel and len(voice.channel.members) == 1:
        await voice.disconnect()

async def play_next(ctx):
    guild_id = ctx.guild.id
    voice_client = ctx.voice_client
    skip_votes[guild_id] = set()

    if guild_id not in queues or not queues[guild_id]:
        current_song[guild_id] = None
        await auto_disconnect_check(ctx)
        return

    if loop_mode.get(guild_id, False):
        title, filename = queues[guild_id][0]
    else:
        title, filename = queues[guild_id].pop(0)

    current_song[guild_id] = title
    volume = volumes.get(guild_id, 1.0)
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), volume=volume)

    def after_play(error):
        asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)

    voice_client.play(source, after=after_play)
    asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {title}"), bot.loop)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    if before.channel and not after.channel:
        for vc in bot.voice_clients:
            if vc.channel == before.channel and len(vc.channel.members) == 1:
                await vc.disconnect()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def help(ctx):
    await ctx.send(
        "!join\n"
        "!leave\n"
        "!play <url or playlist>\n"
        "!queue\n"
        "!skip\n"
        "!pause\n"
        "!resume\n"
        "!stop\n"
        "!remove <index>\n"
        "!clear\n"
        "!loop\n"
        "!volume <0-100>\n"
        "!nowplaying"
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("Joined voice channel.")
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command()
async def play(ctx, url):
    guild_id = ctx.guild.id

    if not ctx.author.voice:
        await ctx.send("Join a voice channel first.")
        return

    voice_client = ctx.voice_client
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()

    await ctx.send("Downloading audio...")

    if guild_id not in queues:
        queues[guild_id] = []

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'ignoreerrors': True,
        'outtmpl': 'song_%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                count = 0
                for entry in info['entries']:
                    if not entry:
                        continue
                    title = entry.get("title", "Unknown Title")
                    filename = f"song_{entry['id']}.mp3"
                    queues[guild_id].append((title, filename))
                    count += 1
                await ctx.send(f"Added {count} songs to the queue.")
            else:
                title = info.get("title", "Unknown Title")
                filename = f"song_{info['id']}.mp3"
                queues[guild_id].append((title, filename))
                await ctx.send(f"Added to queue: {title}")

    except Exception:
        await ctx.send("Error downloading audio.")
        return

    if not voice_client.is_playing():
        await play_next(ctx)

@bot.command()
async def skip(ctx):
    guild_id = ctx.guild.id
    voice_client = ctx.voice_client

    if not voice_client or not voice_client.is_playing():
        await ctx.send("Nothing is playing.")
        return

    if guild_id not in skip_votes:
        skip_votes[guild_id] = set()

    if not ctx.author.voice or ctx.author.voice.channel != voice_client.channel:
        await ctx.send("You must be in the voice channel.")
        return

    non_bot = [m for m in voice_client.channel.members if not m.bot]
    required = max(1, len(non_bot) // 2 + 1)

    if ctx.author.id in skip_votes[guild_id]:
        await ctx.send("You already voted.")
        return

    skip_votes[guild_id].add(ctx.author.id)

    if len(skip_votes[guild_id]) >= required:
        skip_votes[guild_id] = set()
        voice_client.stop()
        await ctx.send("Song skipped.")
    else:
        await ctx.send(f"Skip votes: {len(skip_votes[guild_id])}/{required}")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed.")
    else:
        await ctx.send("Nothing is paused.")

@bot.command()
async def stop(ctx):
    guild_id = ctx.guild.id
    queues[guild_id] = []
    skip_votes[guild_id] = set()
    current_song[guild_id] = None
    if ctx.voice_client:
        ctx.voice_client.stop()
    await ctx.send("Stopped and cleared queue.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left voice channel.")
    else:
        await ctx.send("Not connected.")

@bot.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id not in queues or not queues[guild_id]:
        await ctx.send("Queue is empty.")
        return

    msg = ""
    for i, (title, _) in enumerate(queues[guild_id], 1):
        msg += f"{i}. {title}\n"
    await ctx.send(msg)

@bot.command()
async def remove(ctx, index: int):
    guild_id = ctx.guild.id
    if guild_id not in queues or not queues[guild_id]:
        await ctx.send("Queue is empty.")
        return
    if index < 1 or index > len(queues[guild_id]):
        await ctx.send("Invalid index.")
        return
    title, _ = queues[guild_id].pop(index - 1)
    await ctx.send(f"Removed {title}")

@bot.command()
async def clear(ctx):
    guild_id = ctx.guild.id
    queues[guild_id] = []
    skip_votes[guild_id] = set()
    current_song[guild_id] = None
    await ctx.send("Queue cleared.")

@bot.command()
async def loop(ctx):
    guild_id = ctx.guild.id
    loop_mode[guild_id] = not loop_mode.get(guild_id, False)
    await ctx.send("Loop enabled." if loop_mode[guild_id] else "Loop disabled.")

@bot.command()
async def volume(ctx, amount: int):
    if amount < 0 or amount > 100:
        await ctx.send("Volume must be 0-100.")
        return
    volume_value = amount / 100
    volumes[ctx.guild.id] = volume_value
    if ctx.voice_client and isinstance(ctx.voice_client.source, discord.PCMVolumeTransformer):
        ctx.voice_client.source.volume = volume_value
    await ctx.send(f"Volume set to {amount}%")

@bot.command()
async def nowplaying(ctx):
    title = current_song.get(ctx.guild.id)
    await ctx.send(f"Currently playing: {title}" if title else "Nothing is playing.")
