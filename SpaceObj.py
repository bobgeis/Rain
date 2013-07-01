"""
Objects in Space!  Space objects have coordinates in the game space and need to keep 
track of those in order to be drawn correctly.

Organization:
import modules

constants/global
helper functions:
init



load images (lots!):



classes:

SpaceObj
RandomDebris

ParallaxObj
RandomStar

MovingSpaceObj
RandomRock

AnimatedSpaceObj
RandomCrystal
Explosion

Vessel
Escapepod

Ship
Stingray

Station
"""


import glob, fnmatch, pygame, random

import helper, PilotObj, GameObj

# globals

# space object type keys
SPACEOBJ_LIST = ['Star', 'Sun', 'Debris', 'Rock', 'Crystal']

# space object subtype keys
SUBTYPE_LIST = ['Large', 'Small']

# vessel type keys
VESSEL_LIST = ['Cloverbase', 'Discus', 'Dock', 'Dome', 'Frisbee', 'Leaf', 'Longboat', \
			   'Pod', 'Raindrop', 'Stingray']

# vessel coloring keys
COLORING_LIST = ['Army', 'Builder', 'Civ', 'Garden', 'Grey', 'Medic', 'Miner', 'Navy', 'Pirate', 'Police', \
				 'Science', 'Tree']
				 
# so far flag names match coloring names
FLAG_LIST = ['Army', 'Builder', 'Civ', 'Garden', 'Grey', 'Medic', 'Miner', 'Navy', 'Pirate', 'Police', \
				 'Science', 'Tree']
				 
# cargo keys
CARGO_LIST = ['People', 'Crystal']
				 

				 


# helper functions

def init(game):
	global GAME, VESSEL_IMGS, FLAG_IMGS
	GAME = game
	
	# load images here
	
	
	# get all the vessel file names
	img_names = glob.glob('./Images/Vessel/*/*.png')
	
	# Now to actually load the vessel images!
	# VESSEL_IMGS is a dictionary with the vessel types as keys and another dictionary 
	# for each value.  Each of those dictionaries has vessel colorings as and a list
	# of images for each value.  The list of images correspond to the four glow states
	# that vessels can be drawn in: 0=Off, 1=Dim, 2=Glow, 3=Bright
	VESSEL_IMGS = {vessel:{coloring:[] for coloring in COLORING_LIST} for vessel in VESSEL_LIST}
	for img_name in img_names:
		for vessel in VESSEL_LIST:
			if fnmatch.fnmatch(img_name, '*'+vessel+'*'):
				for coloring in COLORING_LIST:
					if fnmatch.fnmatch(img_name, '*'+coloring+'*'):
						for i in range(4):
							if fnmatch.fnmatch(img_name, '*'+str(i)+'.png'):
								VESSEL_IMGS[vessel][coloring].append(pygame.image.load(img_name))
	
	# import flag images!
	img_names = glob.glob('./Images/Flag/*.png')
	FLAG_IMGS = {}
	for img_name in img_names:
		for flag in FLAG_LIST:
			if fnmatch.fnmatch(img_name, '*'+flag+'*'):
				FLAG_IMGS[flag] = pygame.image.load(img_name)
	
	
	global STAR_IMGS, EXPLOSION_IMGS, FTL_IMGS
	global DEBRIS_IMGS, ROCK_IMGS, SMALLCRYSTAL_IMGS, LARGECRYSTAL_IMGS 
	
	# load images of stars
	file_names = glob.glob('./Images/SpaceObj/Star/*.png')
	STAR_IMGS = []
	for file in file_names:
		STAR_IMGS.append(pygame.image.load(file))
	
	# load images of debris
	file_names = glob.glob('./Images/SpaceObj/Debris/*.png')
	DEBRIS_IMGS = []
	for file in file_names:
		DEBRIS_IMGS.append(pygame.image.load(file))
	
	# load images of rocks
	file_names = glob.glob('./Images/SpaceObj/Rock/*.png')
	ROCK_IMGS = []
	for file in file_names:
		ROCK_IMGS.append(pygame.image.load(file))
	
	# load images of small crystals
	file_names = glob.glob('./Images/SpaceObj/Crystal/Small*.png')
	SMALLCRYSTAL_IMGS = []
	for file in file_names:
		SMALLCRYSTAL_IMGS.append(pygame.image.load(file))
	
	# load images of large crystals
	file_names = glob.glob('./Images/SpaceObj/Crystal/Large*.png')
	LARGECRYSTAL_IMGS = []
	for file in file_names:
		LARGECRYSTAL_IMGS.append(pygame.image.load(file))
		
	# load images of explosions
	file_names = glob.glob('./Images/SpaceObj/Explosion/*.png')
	EXPLOSION_IMGS = []
	for file in file_names:
		EXPLOSION_IMGS.append(pygame.image.load(file))
		
	# load images of vessels going FTL
	file_names = glob.glob('./Images/SpaceObj/FTL/*.png')
	FTL_IMGS = {type:[] for type in VESSEL_LIST}
	for file in file_names:
		for type in VESSEL_LIST:
			if fnmatch.fnmatch(file, '*'+type+'*'):
				FTL_IMGS[type].append(pygame.image.load(file))
	
	



# classes begin here

class SpaceObj:
	
	def __init__(self, pos, img):
		if pos:
			self.pos = [pos[0],pos[1]]
		self.img = img
		
	def draw(self):
		img = self.choose_img()
		
		img_size = img.get_size()
		
		x = self.pos[0] - GAME.corner[0] - int(img_size[0]/2)
		y = self.pos[1] - GAME.corner[1] - int(img_size[1]/2)
		
		GAME.frame.blit(img, [x,y])
		
	def choose_img(self):
		return self.img
		
	def update(self):
		pass
		
	def get_spawn_pt(self, on_screen=False):
		"""Get a random spawn point in the active area 
		(assumed offscreen with parallax plane 1)."""
		return GAME.get_spawn_pt(on_screen)
			 
	def on_screen(self):
		"""Is the object on screen?"""
		return GAME.pt_on_screen(self.pos)
	
	def outside_active_area(self):
		"""Is the object outside the active area?"""
		return GAME.pt_outside_active_area(self.pos)
	
	def die(self):
		"""Object is destroyed somehow.  This won't matter for some things."""
		pass
		
			
class RandomDebris(SpaceObj):
	"""Debris are bits of space fluff and clouds that exist to help give the player
	a sense of their motion and/or a sense of how dirty the zone is."""
	
	def __init__(self):
		angle = random.randrange(360)
		index = random.randrange(len(DEBRIS_IMGS))
		img = pygame.transform.rotate(DEBRIS_IMGS[index], angle)	# to put the image at a random angle
		SpaceObj.__init__(self, None, img)
		self.pos = self.get_spawn_pt()		
		
		
class ParallaxObj(SpaceObj):
	"""ParallaxObj are distant objects, such as stars and planets.  They are some distance
	 in the background and their movement across the screen is at a different rate than 
	 other objects."""
	
	def __init__(self, pos, plane, img):
		SpaceObj.__init__(self, pos, img)
		self.plane = plane
		
	def draw(self):
		img = self.choose_img()
		
		img_size = img.get_size()
		
		x = int((self.pos[0] - GAME.center[0])/self.plane + GAME.frame_center[0] - img_size[0]/2)
		y = int((self.pos[1] - GAME.center[1])/self.plane + GAME.frame_center[1] - img_size[1]/2)
		
		GAME.frame.blit(img, [x,y])
		
	# these methods have to be rewritten to account for the plane	
	def get_spawn_pt(self, on_screen=False):
		"""Get a random spawn point in the active area 
		(assumed offscreen with parallax plane 1)."""
		return GAME.get_spawn_pt(on_screen, self.plane)
			 
	def on_screen(self):
		"""Is the object on screen?"""
		return GAME.pt_on_screen(self.pos, self.plane)
	
	def outside_active_area(self):
		"""Is the object outside the active area?"""
		return GAME.pt_outside_active_area(self.pos, self.plane)
		
		
class RandomStar(ParallaxObj):
	"""A random star."""
	MIN_PLANE = 10
	MAX_PLANE = 30
	
	def __init__(self, on_screen=False):
		plane = random.randint(self.MIN_PLANE,self.MAX_PLANE)
		img = STAR_IMGS[random.randrange(len(STAR_IMGS))]
		ParallaxObj.__init__(self, None, plane, img)
		self.pos = self.get_spawn_pt(on_screen)
		
		
class MovingSpaceObj(SpaceObj):
	"""Moving space objects can have liner and angular velocity, like asteroids."""
	def __init__(self, pos, vel, angle, angvel, radius, mass, img):
		SpaceObj.__init__(self, pos, img)
		self.vel = [vel[0],vel[1]]
		self.angle = angle
		self.angvel = angvel
		self.radius = radius
		self.mass = mass
		
	def choose_img(self):
		return pygame.transform.rotate(self.img, self.angle)
		
	def update(self):
		# ballistic motion
		self.pos[0] += int(self.vel[0])
		self.pos[1] += int(self.vel[1])
		self.angle += self.angvel
		
	def collide(self, object):
		"""did self collide with the given space obj?"""
		return helper.dist(self.pos, object.pos) < self.radius + object.radius
		
	def group_collide(self, group):
		"""Which members of the group collided?"""
		collide_set = set()
		for object in group:
			if self.collide(object):
				collide_set.add(object)
		return collide_set
		
	def bounce(self, object):
		"""Bounce away from the given object."""
		self.vel[0] += (self.pos[0] - object.pos[0])/self.mass
		self.vel[1] += (self.pos[1] - object.pos[1])/self.mass
		object.vel[0] -= (self.pos[0] - object.pos[0])/object.mass
		object.vel[1] -= (self.pos[1] - object.pos[1])/object.mass
		
class RandomRock(MovingSpaceObj):
	ROCK_VEL = 5
	ROCK_ANGVEL = 10
	ROCK_RADIUS = 23
	ROCK_MASS = 10
	CRYSTAL_CHANCE = 0.3
	
	def __init__(self):
		vel = [random.randint(-self.ROCK_VEL, self.ROCK_VEL), \
				random.randint(-self.ROCK_VEL, self.ROCK_VEL)]
		angle = random.randrange(360)
		angvel = random.randint(-self.ROCK_ANGVEL, self.ROCK_ANGVEL)
		img = ROCK_IMGS[random.randrange(len(ROCK_IMGS))]	# get a random rock
		MovingSpaceObj.__init__(self, None, vel, angle, angvel, self.ROCK_RADIUS, self.ROCK_MASS, img)
		self.pos = self.get_spawn_pt()		
		
	def die(self):
		"""Rocks can die."""
		GAME.explosion_set.add(Explosion(self.pos, self.vel, self.angle, self.angvel))
		if random.random() < self.CRYSTAL_CHANCE:
			GAME.loot_set.add(RandomCrystal(self.pos, self.vel, self.angle, self.angvel))
		
	
class AnimatedSpaceObj(MovingSpaceObj):
	"""Animated space objects can move, but also can change their image with time,
	so they need to remember their age as well as have a list of images and a
	method to cycle through them.  The default ASO will cycle backwards through 
	the img_list and then stop."""
	def __init__(self, pos, vel, angle, angvel, radius, mass, img_list, step_rate=1, cycle=False):
		MovingSpaceObj.__init__(self, pos, vel, angle, angvel, radius, mass, None)
		self.img_list = img_list
		self.step_rate = step_rate
		self.age = 0
		self.cycle = cycle
		
	def choose_img(self):
		index = self.choose_index()
		return pygame.transform.rotate(self.img_list[index], self.angle)
		
	def choose_index(self):
		if self.cycle:
			eff_age = self.age % (self.step_rate * len(self.img_list))
		else:
			eff_age = self.age
		index = len(self.img_list) - 1 - int(eff_age / self.step_rate)
		return max(0,index)
		
	def update(self):
		MovingSpaceObj.update(self)
		self.age += 1
		
	def is_done(self):
		return self.age >= len(self.img_list) * self.step_rate 
		
				
class RandomCrystal(AnimatedSpaceObj):
	"""Random crystal."""
	SMALLCRYSTAL_CHANCE = .7
	SMALLCRYSTAL_MAX = 10
	LARGECRYSTAL_MAX = 30
	CRYSTAL_MASS = 5
	STEP_RATE = 30
	def __init__(self, pos, vel, angle, angvel):
		self.cargo = {}
		if random.random() < self.SMALLCRYSTAL_CHANCE:
			img_list = SMALLCRYSTAL_IMGS
			self.cargo['Crystal'] = random.randint(1, self.SMALLCRYSTAL_MAX)
			radius = 2
		else:
			img_list = LARGECRYSTAL_IMGS
			self.cargo['Crystal'] = random.randint(self.SMALLCRYSTAL_MAX, self.LARGECRYSTAL_MAX)
			radius = 4
		AnimatedSpaceObj.__init__(self, pos, vel, angle, angvel*3, radius, self.CRYSTAL_MASS, img_list, self.STEP_RATE)
		
		
		
class Explosion(AnimatedSpaceObj):
	"""An explosion.  Remember to remove it when it's done."""
	def __init__(self, pos, vel, angle, angvel):
		AnimatedSpaceObj.__init__(self, pos, vel, angle, angvel, 1, 1, EXPLOSION_IMGS, 1)
		
class AnimateFTL(AnimatedSpaceObj):
	"""The light created by a vessel going FTL."""
	def __init__(self, pos, vel, angle, angvel, vessel_type):
		AnimatedSpaceObj.__init__(self, pos, vel, angle-90, angvel, 1, 1, FTL_IMGS[vessel_type], 1)
		


class Vessel(AnimatedSpaceObj):
	"""Vessels are ships, boats, pods, etc. In space!  They each have an image associated
	with each of the 4 glow states: off, dim, glow, and bright."""
	GLOW_STEP = 3
	BRIGHT = GLOW_STEP*4 - 1		# Bright if engine is on or shields hit
	GLOW = GLOW_STEP*3 - 1			# Glow if firing or docking
	DIM = GLOW_STEP*2 - 1			# Dim  before off
	
	def __init__(self, pos, vel, angle, angvel, radius, dock_radius, mass, \
				 type, coloring):
				 
		# parts to do with ballistics and collisions
		if pos:
			self.pos = [pos[0], pos[1]]
		self.vel = [vel[0], vel[1]]
		self.angle = angle
		self.angvel = angvel
		self.radius = radius				# the radius for collisions
		self.dock_radius = dock_radius		# the radius for docking
		self.mass = mass
		self.accel = 0			# current acceleration
		self.age = 0
		
		# parts to do with appearance
		self.type = type
		self.coloring = coloring
		img_list = VESSEL_IMGS[type][coloring]
		self.img_list = [pygame.transform.rotate(img, -90) \
						 for img in img_list]					# vessel images are pointing up, but angle = 0 is pointing to the right
		self.img_size = self.img_list[0].get_size()
			
		# image marker used to calculate the index of self.img_list when drawing
		self.glow = 0
		GAME.explosion_set.add(AnimateFTL(self.pos, self.vel, self.angle, self.angvel, self.type))
		

		
		
	def draw(self):
		"""draw the vessel"""
		img = self.choose_img()
		
		img_size = img.get_size()
		
		x = self.pos[0] - GAME.corner[0] - int(img_size[0]/2)
		y = self.pos[1] - GAME.corner[1] - int(img_size[1]/2)
		
		GAME.frame.blit(img, [x,y])
		
	def choose_img(self):
		"""Choose what image to draw from the dictionary of images and rotate it."""
		index = min(len(self.img_list) -1, int(self.glow / self.GLOW_STEP))
		return pygame.transform.rotate(self.img_list[index], self.angle)	
		
	def change_coloring(self, new_coloring):
		"""Changes the vessel's coloring."""
		self.coloring = new_coloring
		self.img_list = [transform.rotate(img,-90) \
						 for img in VESSEL_IMGS['type']['color']]	
		
	def update(self):
		"""Update the ship every tick."""
		# you are now 1 tick older!
		self.age += 1
		if self.glow:
			self.glow -= 1
		
		# ballistic motion
		self.pos[0] += int(self.vel[0])
		self.pos[1] += int(self.vel[1])
		self.angle += self.angvel
		
		# we need to update vel
		# acceleration
		if self.accel:
			vec = helper.ang2vec(self.angle)
			self.vel[0] += vec[0] * self.accel
			self.vel[1] += vec[1] * self.accel
			self.glow = max(self.glow, self.GLOW)
		# friction
		self.vel[0] *= GAME.zone.friction
		self.vel[1] *= GAME.zone.friction
		
	def dock_collide(self, object):
		"""Is the given object in range of self's dock?"""
		return helper.dist(self.pos,object.pos) < self.dock_radius + object.radius
		
	def dock_range(self, vessel):
		"""Are this and that within each other's dock range?"""
		return helper.dist(self.pos,vessel.pos) < self.dock_radius + vessel.dock_radius
		
	def group_dock_collide(self, group):
		"""Which members of the group dock collided?"""
		collide_set = set()
		for object in group:
			if self.dock_collide(object):
				collide_set.add(object)
		return collide_set
			
	def group_dock_range(self, group):
		"""Which members of the pilot group are in docking range?"""
		dock_set = set()
		for pilot in group:	
			if not self == pilot.vessel and self.dock_range(pilot.vessel):
				dock_set.add(pilot)
		return dock_set
			
	def die(self):
		"""If you die, make an explosion."""
		GAME.explosion_set.add(Explosion(self.pos, self.vel, self.angle, self.angvel))
		
	def jump(self):
		"""FTL jump!"""
		GAME.explosion_set.add(AnimateFTL(self.pos, self.vel, self.angle, self.angvel, self.type))
		
	def is_station(self):
		return False		# are you a station?


class Escapepod(Vessel):
	"""Escapepods or lifeboats launched from exploding vessels or spawned randomly."""
	
	ESCAPEPOD_CHANCE = .7	# the chance of getting an escapepod (vs a lifeboat)
	ESCAPEPOD_MAX = 6		# max number of people in an escapepod
	LIFEBOAT_MAX = 18		# max number of people in a lifeboat
	ESCAPE_VEL = 25			# how fast the the escape pods/boats are moving at creation (they are slowed by friction)
	ESCAPEPOD_MASS = 5
	
	def __init__(self, coloring, pos = None):
		if not pos:
			pos = self.get_spawn_pt()
		self.cargo = {}
		if random.random() < self.ESCAPEPOD_CHANCE:
			type = 'Pod'
			self.cargo['People'] = random.randint(1, self.ESCAPEPOD_MAX)
			radius = 4
			dock_radius = 2
		else:
			type = 'Longboat'
			self.cargo['People'] = random.randint(self.ESCAPEPOD_MAX, self.LIFEBOAT_MAX)
			radius = 6
			dock_radius = 4
			
		vel = [random.randint(-self.ESCAPE_VEL,self.ESCAPE_VEL), \
			   random.randint(-self.ESCAPE_VEL,self.ESCAPE_VEL)]
			   
		angle = random.randrange(360)
		angvel = random.randint(-7,7)
		
		Vessel.__init__(self, pos, vel, angle, angvel, radius, dock_radius, self.ESCAPEPOD_MASS, \
				 type, coloring)	
			
	def update(self):
		Vessel.update(self)
		if self.age % (self.GLOW_STEP * 6) == 0:
			self.glow = self.BRIGHT					# this is to make the escape pods blink at some rate
			

		
		
			
class Ship(Vessel):
	"""Ships are vessels big enough to have a flag."""
	
	def __init__(self, pos, vel, angle, angvel, radius, dock_radius, mass, \
		type, coloring, flag, flag_loc):
		Vessel.__init__(self, pos, vel, angle, angvel, radius, dock_radius, mass, \
				 type, coloring)
		self.flag = flag
		self.rot_flag_loc = self.get_rot_flag_loc(flag_loc)
			
	def get_rot_flag_loc(self, flag_loc):
		"""Finds out where the flag should be in the rotated image, given the previous 
		unrotated location.  Remember that the rotation is 90 degrees clockwise."""
		if flag_loc == None:				# if it doesn't have a flag, then go no further!
			return
		x = self.img_size[1] - flag_loc[1] - 10		# flags are 10 pixels square
		y = flag_loc[0]
		return [x,y]
	
	def set_flag(self, new_flag, angle = -90):
		"""Changes the ship's flag."""
		if self.rot_flag_loc == None:		# if it doesn't have a flag, then go no further!
			return
		self.flag = new_flag 
		flag_img = pygame.transform.rotate(FLAG_IMGS[self.flag],angle)
		for img in self.img_list:
			img.blit(flag_img, self.rot_flag_loc)
		

class Stingray(Ship):
	"""Stingrays are a specific type of Ship."""
	
	def __init__(self, pos, coloring):
		radius = 23
		dock_radius = 15
		mass = 10
		flag_loc = [20,12]
		Ship.__init__(self, pos, [0,0], 90, 0, radius, dock_radius, mass, 'Stingray', \
			coloring, coloring, flag_loc)
			
class Raindrop(Ship):
	
	def __init__(self, pos, coloring):
		radius = 12
		dock_radius = 8
		mass = 10
		flag_loc = [11,17]
		Ship.__init__(self, pos, [0,0], 90, 0, radius, dock_radius, mass, 'Raindrop', \
			coloring, coloring, flag_loc)
		
class Discus(Ship):
	
	def __init__(self, pos, coloring):
		radius = 23
		dock_radius = 20
		mass = 10
		flag_loc = [21,21]
		Ship.__init__(self, pos, [0,0], 90, 0, radius, dock_radius, mass, 'Discus', \
			coloring, coloring, flag_loc)
			
		
		
		
class Station(Ship):
	"""Stations are large immobile vessels that can have multiple flags."""
	
	def __init__(self, pos, angle, angvel, radius, dock_radius, type, coloring, flags, \
				flag_locs, flag_angles):
		mass = 1
		Vessel.__init__(self, pos, [0,0], angle, angvel, radius, dock_radius, mass, \
				type, coloring)
		self.flags = flags
		self.rot_flag_locs = self.get_rot_flag_locs(flag_locs)
		self.flag_angles = flag_angles
		
		
	def get_rot_flag_locs(self, flag_locs):
		"""Finds the locations of the station's flags."""
		rot_flag_locs = []
		for flag_loc in flag_locs:
			x = self.img_size[1] - flag_loc[1] - 10		# flags are 10 pixels square
			y = flag_loc[0]
			rot_flag_locs.append([x,y])
		return rot_flag_locs
		
	def set_flags(self, flags):
		"""Changes the station's flags."""
		self.flags = flags
		for i in range(len(flags)):
			flag_img = pygame.transform.rotate(FLAG_IMGS[flags[i]],self.flag_angles[i]-90)
			for img in self.img_list:
				img.blit(flag_img, self.rot_flag_locs[i])
				
	
	def bounce(self, object):
		"""Bounce away from the given object."""
		# stations are stationary!  They do not bounce!
		object.vel[0] -= (self.pos[0] - object.pos[0])/object.mass
		object.vel[1] -= (self.pos[1] - object.pos[1])/object.mass
		
	def is_station(self):
		return True
				

class Dome(Station):
	"""The Dome station has an upper part and a lower part.  The upper part should be 
	drawn *after* the player."""
	
	def __init__(self, pos):
		angle = random.randrange(360)
		radius = 70
		dock_radius = 50
		flags = ['Medic', 'Police', 'Miner', 'Garden']
		flag_locs = [[37,37],[103,37],[103,103],[37,103]]
		flag_angles = [0,-90,-180,-270]
		Station.__init__(self, pos, angle, 0, radius, dock_radius, 'Dome', \
			'Grey', flags, flag_locs, flag_angles)
		self.lower_img_list = VESSEL_IMGS['Dock']['Grey']
		
	def choose_img(self):
		"""Choose what image to draw from the dictionary of images and rotate it."""
		index = min(len(self.img_list) -1, int(self.glow / self.GLOW_STEP))
		return pygame.transform.rotate(self.lower_img_list[index], self.angle)	
		
	def draw_upper(self):
		index = min(len(self.img_list) -1, int(self.glow / self.GLOW_STEP))
		img = pygame.transform.rotate(self.img_list[index], self.angle)
		img_size = img.get_size()
		
		x = self.pos[0] - GAME.corner[0] - int(img_size[0]/2)
		y = self.pos[1] - GAME.corner[1] - int(img_size[1]/2)
		
		GAME.frame.blit(img, [x,y])
			


		

		
		
		