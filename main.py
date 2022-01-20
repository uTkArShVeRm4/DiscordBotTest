from typing import Optional
import discord
from discord import Member, Embed
from discord.ext import commands
import discord.utils
import game
import asyncio 
token = open("../token.txt", "r").read()
client = discord.Client()

client = commands.Bot(command_prefix='$')
#logs in the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



#defining a game state variable to track if game is in process
game_state = False


async def game_event(ctx):
	global game_state, player1, player2
	while game_state:
			if player1.hp <= 0 or player2.hp <= 0:
				game_state = False
				await ctx.message.channel.send('**Game Over!**')
				del player1, player2
			await asyncio.sleep(1)



@client.command(aliases=['sg'])
async def startgame(ctx, p2:Member):
	global player1, game_state, player2
	try:
		if not game_state:

			player1 = game.Player(ctx.message.author)
			player2 = game.Player(p2)
			game_state = True
			
			embed = Embed(title="Game Starts", description=f"{player1.name} vs {player2.name}")
			
			await ctx.send(embed=embed)
			await game_event(ctx)
		else:
			await ctx.send('**unable to start game**')	
	except NameError:
		player1 = game.Player(ctx.message.author)
		player2 = game.Player(p2)
		game_state = True
			
		embed = Embed(title="Game Starts", description=f"{player1.name} vs {player2.name}")
		await ctx.send(embed=embed)
		
		await game_event(ctx)		
		
@client.command()
async def damage(ctx, target: Member, damage):
	target = game.find_player(target,[player1,player2])
	try:
		target.hp = target.hp - int(damage)
		await ctx.send(f'**{target.name} took {damage}**')
	except NameError:
		await ctx.send('**You are not an active player to use this command**')


@client.command()
async def health(ctx, target: Optional[Member]):
	target = game.find_player(target,[player1,player2])
	try:
		await ctx.send(f'**{target.name} has {target.hp} hp**')
		await ctx.send(f'{target.dis_hp()}')
	except NameError:
		await ctx.send('**You are not an active player to use this command**')	


#command to clear chat in server
@client.command()
async def clear(ctx):
    await ctx.channel.purge(limit=50)



#runs the bot ultimately
client.run(token)
