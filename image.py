from PIL import Image
import os
import discord
from discord import Member, File

#grid is 1410x1410 px with 10 px border
#8 by 8
async def image_extractor(player):

	await player.member.display_avatar.save(f'./images/playerimgs/{player.name}.png')

	with Image.open(f'./images/playerimgs/{player.name}.png') as pimg:
		pimg = pimg.resize((150,150))
		pimg.save(f"./images/playerimgs/{player.name}.png")

		player.img = pimg	

def frame_gen(players):
	
	with Image.open('./images/grid.png') as grid:

		for player in players:
			grid.paste(player.img,(13+176*player.pos[0],13+176*player.pos[1]),player.img)				
			grid.save('./images/grid1.png')
		return 'images/grid1.png'