import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first.")
        return

    voice_client = ctx.voice_client
    if not voice_client:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    if voice_client.is_playing():
        voice_client.stop()

    await ctx.send("Downloading audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        except Exception as e:
            await ctx.send("Error downloading audio.")
            print(e)
            return

    voice_client.play(discord.FFmpegPCMAudio(source=filename), after=lambda e: print(f"Finished playing: {e}"))
    await ctx.send(f"Now playing: {info.get('title', 'Unknown Title')}")

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
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Playback stopped.")
    else:
        await ctx.send("Nothing is playing.")

    if os.path.exists("song.mp3"):
        os.remove("song.mp3")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
        if os.path.exists("song.mp3"):
            os.remove("song.mp3")
    else:
        await ctx.send("I'm not in a voice channel.")
