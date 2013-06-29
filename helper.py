"""
Some helper functions needed by game modules.
"""

import math, random
	
# for the SOS function which blinks ...---...
SOS_DOT = 4
SOS_DASH = SOS_DOT * 3
SOS_PAUSE = SOS_DOT
SOS_GAP = 3
SOS_LENGTH = 6 * SOS_DOT + 3 * SOS_DASH + 9 * SOS_PAUSE + SOS_GAP * SOS_DASH	
	
# SOS blinker
def SOS_on(age):
	"""Given the age in ticks, return True if the light should be on at the given tick
	in order to spell SOS (...---...) in Morse Code.  Real Morse Code should have 
	dots ~50-60ms in length and dashes ~150-180ms in length, and at 30fps a tick is ~33ms.  
	Given that this game is not real life, we'll have dash = dot*3 and pause = dot, 
	with some gap.  So with 6 dots, 3 dashes, and 9 pauses, we'd have a length of 
	equivalent to 24 dots plus the gap."""
	age = int(age % SOS_LENGTH)/SOS_DOT
	if age > 24:
		return False
	elif age < 6 or age >= 18:
		if age % 2 == 0:
			return True
		else:
			return False
	else:
		if age % 4 == 2:
			return False
		else:
			return True

# 2D scaling, not updating
def scale(p, scalar):
	"""Scale a vector by a number."""
	return [p[0] * scalar, p[1] * scalar]

# 2D distance 
def dist(p, q):
	"""Given two points in the form [x,y], return the distance between them."""
	return math.hypot(p[0] - q[0], p[1] - q[1])
	
# 2D dot product
def dot_product(p,q):
	"""Given two vectors in the form [x,y], return their dot product."""
	return p[0] * q[0] + p[1] * q[1]
	
# 2D cross product
def cross_product(p, q):
	"""Given two vectors in the form [x,y], return the magnitude of their cross product."""
	return p[0] * q[1] - p[1] * q[0]
	
# 2D vector addition
def add(p, q):
	"""Given two vectors in the form [x,y], return their sum."""
	return [p[0] + q[0], p[1] + q[1]]
	
# 2D vector subtraction
def subtract(p, q):
	"""Given two vectors in the form [x,y], return their difference."""
	return [p[0] - q[0], p[1] - q[1]]
	
# 2D magnitude
def mag(vector):
	"""Given a vector in the form [x,y], return its magnitude/length."""
	return math.hypot(p[0], p[1])

# 2D angle to vector
def ang2vec(angle):
	"""Given an angle in degrees widdershins from the x axis, return a unit vector in the form [x,y]"""
	return [math.cos(math.radians(angle)), -math.sin(math.radians(angle))]
	
# 2D vector to angle
def vec2ang(vector):
	"""Given a vector in the form [x,y], return its angle in degrees widdershins from the x axis."""
	return math.degrees(math.atan2(vector[0],vector[1]))
	
# get a nearby spawn point	
def spawn_in_active_zone(camera, WINSIZE, plane=1):
	"""Get a point [x,y] somewhere in the active zone.  The active zone is a square
	3*WINWID wide by 3*WINHEI tall centered on the center of the screen."""
	x = random.randint(int(-WINSIZE[0]*plane + camera[0]), int(2*WINSIZE[0]*plane + camera[0]))
	y = random.randint(int(-WINSIZE[1]*plane + camera[1]), int(2*WINSIZE[1]*plane + camera[1]))
	return [x,y]
	
# get a nearby but offscreen spawn point
def spawn_offscreen(camera, WINSIZE, plane=1):
	"""Return [x,y] which are the coordinates of a point offscreen, but within 
	the active zone."""
	[x,y] = spawn_in_active_zone(camera, WINSIZE, plane)
	while x > camera[0] and x < WINSIZE[0] + camera[0] and \
			y > camera[1] and y < WINSIZE[1] + camera[1]:
		[x,y] = spawn_in_active_zone(camera, WINSIZE, plane)
	return [x,y]	
	


