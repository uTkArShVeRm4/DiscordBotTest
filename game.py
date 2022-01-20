class Player():
	def __init__(self,name):

		#modify hp for actual health counter
		self.hp = 10


		self.name = name


	def dis_hp(self):
		#current_hp is just for displaying in discord
		return (':green_circle:'*self.hp)+(':red_circle:'*(10-self.hp))

