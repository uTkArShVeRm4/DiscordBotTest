from typing import Optional
from random import randint
from itertools import cycle
import discord
from discord import Member, Embed, File
from discord.ext import commands
import discord.utils
from discord.ui import Button,View
import game
import asyncio 
import image
token = open("../token.txt", "r").read()
client = discord.Client()

client = commands.Bot(command_prefix='$')
#logs in the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



#defining a game state variable to track if game is in process
game_state = False
players = []
player1 = None
player2 = None
active_player = None
opp_player = None
pcycle = None

#loop to check if game is over and deletes player objects
async def game_event(ctx):
	global game_state, player1, player2, active_player, opp_player
	while game_state:
			if player1.hp <= 0 or player2.hp <= 0:
				game_state = False
				await ctx.message.channel.send('**Game Over!**')
				del player1, player2, active_player, opp_player
			await asyncio.sleep(1)




@client.command(aliases=["ui"])
async def turn_ui(ctx):
	global active_player, opp_player


	async def pass_to_next_player(interaction):
		global active_player, opp_player
		if interaction.user == active_player.member:
			opp_player = active_player
			button_pass.disabled = True
			button_damage.disabled = True
			await interaction.response.edit_message(view=view)
			active_player = next(pcycle)
			await turn_ui(ctx)


	async def deal_damage(interaction):
		global active_player, opp_player
		if interaction.user == active_player.member:
			damage = randint(1,6)
			opp_player.hp -= damage

			button_damage.disabled = True
			await interaction.response.edit_message(view=view)
			await interaction.followup.send(f'{active_player.name} dealt {damage} damage')
			



	ui = Embed(title = f"{active_player.name}'s turn", description=active_player.dis_hp())


	file = File(image.frame_gen(players), filename="image.png")
	ui.set_image(url="attachment://image.png")

	# ui.set_image(url='attachment://images/grid1.png')

	ui.set_thumbnail(url=active_player.member.display_avatar)
	


	button_pass = Button(label='pass')
	button_pass.callback = pass_to_next_player

	button_damage = Button(label="Hit enemy",style=discord.ButtonStyle.red)
	button_damage.callback = deal_damage

	view = View()
	view.add_item(button_pass)
	view.add_item(button_damage)
	await ctx.send(file=file,embed=ui,view=view)




#start game 
@client.command(aliases=['sg'])
async def startgame(ctx, p2:Optional[Member]):
	global player1, game_state, player2, players, pcycle, active_player, opp_player
	
	if not game_state:

		player1 = game.Player(ctx.message.author)
		player1.posx = 4
		player1.posy = 3
		player2 = game.Player(p2)
		player2.posx = 3
		player2.posy = 4
		players = [player2,player1]
		await image.image_extractor(player1)
		await image.image_extractor(player2)
		game_state = True
		active_player = player1
		opp_player = player2
		pcycle = cycle(players)
		
		embed = Embed(title='Game Start', description=f'{player1.name} vs {player2.name}')

		await ctx.send(embed = embed)

		await turn_ui(ctx)

		#keep this at the bottom 
		await game_event(ctx)
	else:
		await ctx.send('**unable to start game**')	
	# except NameError:
	# 	player1 = game.Player(ctx.message.author)
	# 	player2 = game.Player(p2)
	# 	game_state = True
	# 	active_player = player1
	# 	opp_player = player2
	# 	pcycle = cycle(players)
	
	# 	embed = Embed(title='Game Start', description=f'{player1.name} vs {player2.name}')

	# 	await ctx.send(embed = embed)


	# 	await turn_ui(ctx)
	# 	await game_event(ctx)		
		

#command to clear chat in server
@client.command()
async def clear(ctx):
    await ctx.channel.purge(limit=50)



#runs the bot ultimately
client.run(token)
