"""
EquipObj

Organization:

Globals
init

EquipObj
BasicEquip
FragileEquip
SlowEquip
StationEquip

WpnObj
BeamObj
LanceBeam
"""

import random, pygame, math

import helper, GameObj




GAME = None

LANCECOLOR1 = (100,255,255)
LANCECOLOR2 = (  0,225,225) 
LANCECOLOR3 = ( 25,175,175)
LANCECOLOR4 = ( 50,125,125)
LANCECOLOR5 = ( 25, 50, 50)

LANCECOLORS = [LANCECOLOR1,LANCECOLOR2,LANCECOLOR3,LANCECOLOR4,LANCECOLOR5]

def init(game):
	global GAME
	GAME = game

class EquipObj:
	"""These are objects that contain sets of vessel properties, such as their 
	thrust and turn rates, their shield and cargo capacity, and their weapons and 
	defenses."""
	
	def __init__(self, thrust, retro, turn_rate, shield_max, shield_regen, cargo_max, \
			     main_wpn = None, alt_wpn = None):
		self.thrust = thrust		# acceleration forward in pixels per tick per tick.  Note: FPS is 30 ticks per second
		self.retro = retro			# acceleration in reverse in p/t/t.  Note: positive is forward so this should be < 0
		self.turn_rate = turn_rate 	# turning rate in degrees per tick.  Note: at 30 ticks per second '9' -> 180 degrees per second
		self.shield_max = shield_max
		self.shield_regen = shield_regen
		self.cargo_max = cargo_max
		self.main_wpn = main_wpn
		self.alt_wpn = alt_wpn
		
class BasicEquip(EquipObj):
	
	def __init__(self):
		thrust = 5
		retro = -1
		turn_rate = 9
		shield_max = 100
		shield_regen = .01
		cargo_max = 100
		EquipObj.__init__(self, thrust, retro, turn_rate, shield_max, shield_regen, cargo_max, main_wpn = LanceBeam)
		
class FragileEquip(EquipObj):

	def __init__(self):
		thrust = 1
		retro = -.1
		turn_rate = 4
		shield_max = 10
		shield_regen = 0
		cargo_max = 50
		EquipObj.__init__(self, thrust, retro, turn_rate, shield_max, shield_regen, cargo_max)
		
		
class SlowEquip(EquipObj):

	def __init__(self):
		thrust = .5
		retro = -.1
		turn_rate = 4
		shield_max = 200
		shield_regen = .01
		cargo_max = 200
		EquipObj.__init__(self, thrust, retro, turn_rate, shield_max, shield_regen, cargo_max)

		
class StationEquip(EquipObj):
	
	def __init__(self):
		thrust = 0
		retro = 0
		turn_rate = 0
		shield_max = 500
		shield_regen = .05
		cargo_max = 10000
		EquipObj.__init__(self, thrust, retro, turn_rate, shield_max, shield_regen, cargo_max)
		
		
class WpnObj:
	"""Weapons!  Such as beams and torpedos!"""
	
	def __init__(self, start, angle, target= None):
		self.start = start			# the position of the firing vessel
		self.angle = angle			# the direction the vessel is shooting in
		self.target = None 			# what the vessel is shooting at
		
	def draw(self):
		"""This can vary so much that each weapon must implement it differently."""
		pass
		
	def update(self):
		pass
		
	def is_done(self):
		"""Has the weapon finished?"""
		return True
		
	def hit(self, object):
		"""Did the weapon hit the given object?"""
		return False
		
	def hit_target(self):
		"""Did the weapon hit the target?"""
		return False
	
	
class BeamObj(WpnObj):
	"""Beams are drawn between two points."""
	
	def __init__(self, start, angle, range, lifespan, color_list, target = None):
		self.start = start
		self.angle = angle
		self.range = range
		self.vec = helper.ang2vec(angle)
		self.vec = [self.vec[0] * self.range, self.vec[1] * self.range]
		self.stop = [self.start[0] + self.vec[0], self.start[1] + self.vec[1]]
		self.lifespan = lifespan
		self.age = 0
		self.color_list = color_list
		self.target = target
		self.hit_delay = 0
	
	def draw(self):
		"""Draws the beam object."""
		color = self.choose_color()
		thickness = self.choose_thickness()
		pygame.draw.line(GAME.frame, color, \
					[self.start[0] - GAME.corner[0],self.start[1] - GAME.corner[1]], \
					[self.stop[0] - GAME.corner[0],self.stop[1] - GAME.corner[1]], \
					thickness)
					
	def choose_color(self):
		"""Specific beams should change this."""
		return self.color_list[0]
		
	def choose_thickness(self):
		"""Specific beams should change this."""
		return 1
		
	def update(self):
		self.age += 1
		if self.hit_delay:
			self.hit_delay -= 1
		
	def is_done(self):
		return self.lifespan > 0 and self.age >= self.lifespan 

	def hit(self, object):
		"""Did the beam hit the given target?  Needs the target's pos and the its radius."""
		vec2obj = [object.pos[0] - self.start[0], object.pos[1] - self.start[1]]
		projection = helper.dot_product(self.vec, vec2obj) / self.range
		if projection < 0 or projection > self.range:  # is the target behind the beam or too far in front?
			return False
		elif object.radius**2 + projection**2 < vec2obj[0]**2 + vec2obj[1]**2:  # is the target too far to either side from the beam?
			return False
		else:
			return True
			
	def hit_target(self):
		if self.target:
			return self.hit(self.target.vessel)
		else:
			return False
			
			
			
class LanceBeam(BeamObj):
	"""Represents lance beams, which are fired once to a specific point and then fade rapidly."""
	LANCE_DAMAGE = 10
	
	def __init__(self, start, angle, target = None):
		range = 500 					# range of lance beams
		lifespan = 8 					# lifespan of lance beams
		color_list = LANCECOLORS		# lance colors :)
		BeamObj.__init__(self, start, angle, range, lifespan, color_list, target)
		
	
	def choose_color(self):
		"""What color should the beam be right now?  Varies by beam and probably with age."""
		return self.color_list[min(int(self.age/2),len(self.color_list))]
		
	def choose_thickness(self):
		"""What thickness should the beam be right now?  Varies by beam and probably with age."""
		return max(0,int((self.lifespan - self.age)/2))
		
	def hit_target(self):
		if self.hit_delay:
			pass
		elif BeamObj.hit_target(self):
			self.hit_delay = 8
			self.target.damage(self.LANCE_DAMAGE)