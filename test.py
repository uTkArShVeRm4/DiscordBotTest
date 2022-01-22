from typing import Optional
import image
import discord
from discord import Member, Embed
from discord.ext import commands
import game
from PIL import Image

token = open("../token.txt", "r").read()
client = discord.Client()

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in tester as {0.user}'.format(client))


@client.command()
async def test(ctx, arg: Optional[Member]):
	await ctx.send('test command working')
	target = arg or ctx.author
	print(target)
	embed = Embed(title="test", description="this works")
	embed.set_thumbnail(url=target.display_avatar)
	await ctx.send(embed=embed)
	image.frame_gen()

client.run(token)