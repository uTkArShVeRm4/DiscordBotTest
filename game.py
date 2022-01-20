class Player():

	def __init__(self,mem):

		#modify hp for actual health counter
		self.hp = 10
		self.member = mem
		self.name = mem.name

	def dis_hp(self):
		#current_hp is just for displaying in discord
		return (':green_circle:'*self.hp)+(':red_circle:'*(10-self.hp))

def find_player(id,li):
	for player in li:
		if player.member == id:
			return player