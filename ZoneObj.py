"""
ZoneObj
"""

# colors	   R   G   B	# no particular colors are required, and you may need to add some to this.
BLACK = 	(  0,  0,  0)
WHITE = 	(255,255,255)
GREY = 		(128,128,128)

RED =   	(255,  0,  0)
GREEN = 	(  0,255,  0)
BLUE =  	(  0,  0,255)

YELLOW = 	(255,255,  0)
MAGENTA = 	(255,  0,255)
CYAN = 		(  0,255,255)

import random, copy

import helper, SpaceObj, PilotObj, EquipObj, GameObj



def init(game):
	global GAME
	GAME = game




class ZoneObj:
	"""Zone objects represent separate areas that player can travel to.  For example
	one zone would represent the area around a star, another deep space, another the 
	area around a planet, and another might be in hyperspace or a blackhole."""
	
	def __init__(self, name, size, shape, friction, star_density, debris_density, \
				rock_density, spawn_chance, background_color, pilot_list, spawn_pilot_list, \
				node_list):
		self.name = name
		self.size = size		# if there's an edge, how far away is it from the origin? (at the closest point)
		self.shape = shape		# what shape is the edge? Ex: 'Square', 'Circle'
		self.friction = friction
		self.star_density = star_density
		self.debris_density = debris_density
		self.rock_density = rock_density
		self.background_color = background_color
		self.spawn_chance = spawn_chance
		
		self.spawn_pilot_list = spawn_pilot_list
		self.pilot_list = pilot_list
		self.node_list = node_list
		
	def spawn_pilot(self):
		pass
		
		
		
class Starting(ZoneObj):
	"""This is the starting zone that we've been playing with so far."""
	
	def __init__(self):
		pilot_list = []
		pilot_list.append(PilotObj.PilotObj(SpaceObj.Dome([0,0]),EquipObj.StationEquip()))
		spawn_pilot_list = []
		spawn_pilot_list.append(PilotObj.PilotObj(SpaceObj.Raindrop(GAME.get_spawn_pt(True),'Civ'),EquipObj.BasicEquip()))
		node_list = []
		spawn_chance = 0.005
		friction = 0.9
		star_density = 100
		debris_density = 20
		rock_density = 20
		ZoneObj.__init__(self, 'Maia: Asteroid Belt', None, None, friction, star_density, \
				debris_density, rock_density, spawn_chance, \
				BLACK, pilot_list, spawn_pilot_list, node_list)
				
	def spawn_pilot(self):
		if random.random() < self.spawn_chance:
			GAME.pilot_list.append(PilotObj.RandomDirection(SpaceObj.Raindrop(GAME.get_spawn_pt(),'Civ'),EquipObj.FragileEquip()))
				
				
class Next(ZoneObj):
	"""This is the next zone after the starting zone."""
	
	def __init__(self):
		pilot_list = []
		spawn_pilot_list = []
		node_list = []
		friction = 0.9
		star_density = 200
		debris_density = 10
		rock_density = 5
		spawn_chance = 0
		ZoneObj.__init__(self, 'Maia: Verdeluna', None, None, friction, star_density, \
				debris_density, rock_density, spawn_chance, \
				BLACK, pilot_list, spawn_pilot_list, node_list)