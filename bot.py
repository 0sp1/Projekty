import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx, arg):
    await ctx.send(f"What the fuck {arg}")

@bot.command()
async def join(ctx, arg):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined `{channel}`!{arg}")
    else:
        await ctx.send("You must be in a voice channel first.")
        
@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first.")
        return

    voice_client = ctx.voice_client
    if not voice_client:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    # Download audio

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")