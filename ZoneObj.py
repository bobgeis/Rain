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
				rock_density, background_color, pilot_list, \
				node_list):
		self.name = name
		self.size = size		# if there's an edge, how far away is it from the origin? (at the closest point)
		self.shape = shape		# what shape is the edge? Ex: 'Square', 'Circle'
		self.friction = friction
		self.star_density = star_density
		self.debris_density = debris_density
		self.rock_density = rock_density
		self.background_color = background_color
		
		self.pilot_list = pilot_list
		self.node_list = node_list
		
	def spawn_pilot(self):
		pass
		
		
		
class Starting(ZoneObj):
	"""This is the starting zone that we've been playing with so far."""
	SPAWN_RAINDROP_CHANCE = 0.005
	SPAWN_DISCUS_CHANCE = 0.001
	
	def __init__(self):
		pilot_list = []
		pilot_list.append(PilotObj.PilotObj(SpaceObj.Dome([0,0]),EquipObj.StationEquip()))
		node_list = []
		node_sprite = SpaceObj.ParallaxObj([5000,5000], 5, SpaceObj.PLANET_IMG)
		node_list.append(Node([5000,5000],[1000,1000],node_sprite, Next()))
		friction = 0.9
		star_density = 100
		debris_density = 20
		rock_density = 20
		ZoneObj.__init__(self, 'Maia: Asteroid Belt', None, None, friction, star_density, \
				debris_density, rock_density, \
				BLACK, pilot_list, node_list)
				
	def spawn_pilot(self):
		if random.random() < self.SPAWN_RAINDROP_CHANCE:
			GAME.pilot_list.append(PilotObj.RandomDirection( \
					SpaceObj.Raindrop(GAME.get_spawn_pt(),'Civ'),EquipObj.FragileEquip()))
		elif random.random() < self.SPAWN_DISCUS_CHANCE:
			GAME.pilot_list.append(PilotObj.RandomDirection( \
					SpaceObj.Discus([0,0], random.choice(['Medic','Miner','Police'])), \
					EquipObj.SlowEquip()))
			
				
class Next(ZoneObj):
	"""This is the next zone after the starting zone."""
	
	def __init__(self):
		pilot_list = []
		node_list = []
		friction = 0.9
		star_density = 300
		debris_density = 10
		rock_density = 5
		ZoneObj.__init__(self, 'Maia: Verdeluna', None, None, friction, star_density, \
				debris_density, rock_density, \
				BLACK, pilot_list, node_list)
				
				
class Splash(ZoneObj):
	"""This is a zone for the splash screen."""
	
	def __init__(self):
		pilot_list = []
		rain_drop = PilotObj.PilotObj(SpaceObj.Raindrop([50000,50000],'Civ'),EquipObj.BasicEquip())
		rain_drop.vessel.angle = 90
		rain_drop.thrust_for()
		pilot_list.append(rain_drop)
		node_list = []
		friction = .99
		star_density = 200
		debris_density = 5
		rock_density = 0
		ZoneObj.__init__(self, 'Splash Zone', None, None, friction, star_density, \
				debris_density, rock_density, \
				BLACK, pilot_list, node_list)
				
				
class Node:
	"""Nodes represent links between zones."""
	
	def __init__(self, pos, out_pos, parallax_obj, zone):
		self.pos = pos
		self.out_pos = out_pos
		self.parallax_obj = parallax_obj
		self.zone = zone
		
	def draw(self):
		self.parallax_obj.draw()
		
	def update(self):
		pass
		
	def make_anti_node(self):
		return Node(out_pos, pos, None, Game.zone)
		
	def in_jump_range(self, pilot):
		return helper.dist(self.pos,pilot.vessel.pos) <= 10 + pilot.vessel.radius
		
		
		
		