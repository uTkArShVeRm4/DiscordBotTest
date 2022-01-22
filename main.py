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

	async def movement(interaction):
		if interaction.user == active_player.member:
			button_back = Button(label='prev menu')
			button_up=Button(emoji='⬆️')
			button_down=Button(emoji='⬇️')
			button_left=Button(emoji='⬅️')
			button_right=Button(emoji='➡️')

			async def change_frame(interaction):
				ui2 = Embed(title = f"{active_player.name}'s turn", description=active_player.dis_hp())
				file2 = File(image.frame_gen(players), filename="image.png")
				ui2.set_image(url="attachment://image.png")
				ui2.set_thumbnail(url=active_player.member.display_avatar)
				await interaction.message.edit(file=file2,embed=ui2,view=view_move)

			async def check_avail_spaces():
				if active_player.pos[0]<= 0 or (active_player.pos[1]==opp_player.pos[1] and active_player.pos[0]-1 == opp_player.pos[0]):
					button_left.disabled = True
				else:
					button_left.disabled = False	

				if active_player.pos[0]>= 7 or (active_player.pos[1]==opp_player.pos[1] and active_player.pos[0]+1 == opp_player.pos[0]):
					button_right.disabled = True
				else:
					button_right.disabled = False

				if active_player.pos[1]<= 0 or (active_player.pos[0]==opp_player.pos[0] and active_player.pos[1]-1 == opp_player.pos[1]):
					button_up.disabled = True
				else:
					button_up.disabled = False	

				if active_player.pos[1]>= 7 or (active_player.pos[0]==opp_player.pos[0] and active_player.pos[1]+1 == opp_player.pos[1]):
					button_down.disabled = True	
				else:
					button_down.disabled = False			

			async def down(interaction):
				if interaction.user == active_player.member:
					active_player.pos[1] += 1
					await check_avail_spaces()
					await change_frame(interaction)

			async def up(interaction):
				if interaction.user == active_player.member:
					active_player.pos[1] -= 1
					await check_avail_spaces()
					await change_frame(interaction)	

			async def right(interaction):
				if interaction.user == active_player.member:
					active_player.pos[0] += 1
					await check_avail_spaces()
					await change_frame(interaction)	
								
			async def left(interaction):
				if interaction.user == active_player.member:
					active_player.pos[0] -= 1
					await check_avail_spaces()
					await change_frame(interaction)			

			async def back(interaction):
				if interaction.user == active_player.member:		
					await interaction.response.edit_message(view=view)

			button_up.callback = up
			button_down.callback = down	
			button_left.callback = left
			button_right.callback = right
			button_back.callback = back
			button_list = [button_back,button_up,button_down,button_right,button_left]
			view_move = View()
			for button in button_list:
				view_move.add_item(button)
			await interaction.response.edit_message(view=view_move)		

	async def pass_to_next_player(interaction):
		global active_player, opp_player
		if interaction.user == active_player.member:
			opp_player = active_player

			for button in buttons:
				button.disabled = True
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

	button_pass = Button(label='pass',style=discord.ButtonStyle.green)
	button_pass.callback = pass_to_next_player

	button_damage = Button(label="Hit enemy",style=discord.ButtonStyle.red)
	button_damage.callback = deal_damage

	button_movement = Button(label="Move")
	button_movement.callback = movement

	buttons = [button_pass,button_damage,button_movement]

	ui = Embed(title = f"{active_player.name}'s turn", description=active_player.dis_hp())
	file = File(image.frame_gen(players), filename="image.png")
	ui.set_image(url="attachment://image.png")
	ui.set_thumbnail(url=active_player.member.display_avatar)

	view = View()
	for button in buttons:
		view.add_item(button)		
		
	async def main_menu(ctx):
		await ctx.send(file=file,embed=ui,view=view)
	
	await main_menu(ctx)

#start game 
@client.command(aliases=['sg'])
async def startgame(ctx, p2:Optional[Member]):
	global player1, game_state, player2, players, pcycle, active_player, opp_player
	
	if not game_state:

		player1 = game.Player(ctx.message.author)
		player1.pos = [4,3]
		player2 = game.Player(p2)
		player2.pos = [3,4]
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
		
#command to clear chat in server
@client.command()
async def clear(ctx):
    await ctx.channel.purge(limit=50)

#runs the bot ultimately
client.run(token)