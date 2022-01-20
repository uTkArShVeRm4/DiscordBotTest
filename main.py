import discord
from discord.ext import commands
import discord.utils
import game
import asyncio 
token = open("token.txt", "r").read()
client = discord.Client()


client = commands.Bot(command_prefix='$')

#logs in the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



#defining a game state variable to track if game is in process
game_state = False


async def game_event(ctx):
	global game_state, player1
	while game_state:
			if player1.hp <= 0:
				game_state = False
				await ctx.message.channel.send('**Game Over!**')
				del player1
			await asyncio.sleep(1)



@client.command(aliases=['sg'])
async def startgame(ctx):
	global player1, game_state
	try:
		if not game_state:

			player1 = game.Player(ctx.message.author.name)
			game_state = True
			
			await ctx.send('**Game Started**')
			await ctx.send(f'**{player1.name} has {player1.hp} hp**')
			await game_event(ctx)
		else:
			await ctx.send('**unable to start game**')	
	except NameError:
		player1 = game.Player(ctx.message.author.name)
		game_state = True
			
		await ctx.send('**game started**')
		await ctx.send(f'**{player1.name} has {player1.hp} hp**')
		await game_event(ctx,player1)		
		
@client.command()
async def damage(ctx, damage):
	global player1
	try:
		player1.hp = player1.hp - int(damage)
		await ctx.send(f'**you took {damage}**')
	except NameError:
		await ctx.send('**You are not an active player to use this command**')


@client.command()
async def health(ctx):
	global player1
	try:
		await ctx.send(f'**you have {player1.hp}**')
		await ctx.send(f'**you have {player1.dis_hp()}**')
	except NameError:
		await ctx.send('**You are not an active player to use this command**')	


#command to clear chat in server
@client.command()
async def clear(ctx):
    await ctx.channel.purge(limit=50)



#runs the bot ultimately
client.run(token)
