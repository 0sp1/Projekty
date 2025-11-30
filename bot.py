import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import uuid

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queues = {}
loop_mode = {}

async def play_next(ctx):
    guild_id = ctx.guild.id
    voice_client = ctx.voice_client

    if guild_id not in queues or len(queues[guild_id]) == 0:
        return

    if loop_mode.get(guild_id, False):
        title, filename = queues[guild_id][0]
    else:
        title, filename = queues[guild_id].pop(0)

    def after_play(err):
        if err:
            print("Error:", err)
        asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)

    voice_client.play(discord.FFmpegPCMAudio(filename), after=after_play)
    asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: **{title}**"), bot.loop)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined `{channel}`!")
    else:
        await ctx.send("You're not in a voice channel.")

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

    unique_id = str(uuid.uuid4())[:8]
    output_name = f"song_{unique_id}.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_name,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            real_name = ydl.prepare_filename(info)
            filename = real_name.replace('.webm', '.mp3').replace('.m4a', '.mp3')
            title = info.get("title", "Unknown Title")
    except Exception as e:
        await ctx.send("Error downloading audio.")
        print(e)
        return

    if guild_id not in queues:
        queues[guild_id] = []

    queues[guild_id].append((title, filename))
    await ctx.send(f"Added to queue: **{title}**")

    if not voice_client.is_playing() and len(queues[guild_id]) == 1:
        await play_next(ctx)

@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("⏭ Skipped!")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Playback paused.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resuming playback.")
    else:
        await ctx.send("Nothing is paused.")

@bot.command()
async def stop(ctx):
    guild_id = ctx.guild.id
    queues[guild_id] = []
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
    await ctx.send("Stopped and cleared queue.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id not in queues or len(queues[guild_id]) == 0:
        await ctx.send("The queue is empty.")
        return

    message = "**Current Queue:**\n"
    for i, (title, _) in enumerate(queues[guild_id], start=1):
        message += f"`{i}.` {title}\n"
    await ctx.send(message)

@bot.command()
async def remove(ctx, index: int):
    guild_id = ctx.guild.id
    if guild_id not in queues or len(queues[guild_id]) == 0:
        await ctx.send("The queue is empty.")
        return
    if index < 1 or index > len(queues[guild_id]):
        await ctx.send("Invalid index.")
        return

    title, _ = queues[guild_id].pop(index - 1)
    await ctx.send(f"Removed **{title}** from the queue.")

@bot.command()
async def clear(ctx):
    guild_id = ctx.guild.id
    if guild_id not in queues or len(queues[guild_id]) == 0:
        queues[guild_id] = []
        await ctx.send("Queue is already empty.")
        return
    queues[guild_id] = []
    await ctx.send("Queue cleared.")

@bot.command()
async def loop(ctx):
    guild_id = ctx.guild.id
    current = loop_mode.get(guild_id, False)
    loop_mode[guild_id] = not current

    if loop_mode[guild_id]:
        await ctx.send("Loop mode enabled.")
    else:
        await ctx.send("Loop mode disabled.")
