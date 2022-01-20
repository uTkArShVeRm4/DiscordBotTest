from typing import Optional

import discord
from discord import Member, Embed
from discord.ext import commands
import game

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
	embed = Embed(title="information", description=":green_circle:"*10)
	embed.set_thumbnail(url=target.avatar_url)
	await ctx.send(embed=embed)

@client.command()
async def sg(ctx):
	player1 = game.Player(ctx.author)
	await ctx.send(player1.name)
	await ctx.send(player1.hp)
	await ctx.send(player1.member)



client.run(token)