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

async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("Join a voice channel first.")
        return

bot.run("")