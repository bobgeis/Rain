


import math, random

import helper, SpaceObj, ScreenObj, PilotObj


class GameObj:
	
	LOOT_MAX = 20
	ROCK_DAMAGE = 5

	def __init__(self, frame):
		self.frame = frame
		self.frame_size = frame.get_size()
		self.frame_center = [int(self.frame_size[0]/2),int(self.frame_size[1]/2)]
		self.corner = [0,0]
		self.center = [self.corner[0] + self.frame_center[0], \
						self.corner[1] + self.frame_center[1]]
		self.centered_on = None		# what is the camera looking at?
		
		self.zone = None			# the current zone
		self.player = None			# the player?
		
		# objects on the screen
		self.screenobj_list = []
		
		# objects in the game space
		self.pilot_list = []	# the list of pilots/vessels in the game space
		self.remove_pilot_set = set() # who's been blown up?
		self.node_list = []		# the list of nodes in the game space
		#self.beam_list = []		# the group of beam objects  # this might not stay a list
		self.wpn_set = set()	# making this a set for now
		self.explosion_set = set()
		
		self.rock_set = set()	# the group of rocks
		self.loot_set = set()	# the group of loot objects
		self.debris_set = set()	# the group of debris
		self.star_set = set()	# the group of background stars
		
		
	def draw(self):
		"""draw everything in the game space"""
		# Remember FIFO and later things are drawn on top of earlier things.
		# draw the background first!
		self.center_camera()
		
		self.frame.fill(self.zone.background_color)
		
		for star in self.star_set:
			star.draw()
			
		for node in self.node_list:
			node.draw()
			
		for wpn in self.wpn_set:
			wpn.draw()
			
		for explosion in self.explosion_set:
			explosion.draw()
			
		for rock in self.rock_set:
			rock.draw()
			
		for loot in self.loot_set:
			loot.draw()
			
		for debris in self.debris_set:
			debris.draw()
			
		for pilot in self.pilot_list:
			pilot.draw()
			
		for pilot in self.pilot_list:
			if hasattr(pilot.vessel, 'draw_upper'):
				pilot.vessel.draw_upper()
				
		for screenobj in self.screenobj_list:
			screenobj.draw()
		
	def center_camera(self):
		self.center = self.centered_on.pos
		self.corner = [self.center[0] - self.frame_center[0],
					   self.center[1] - self.frame_center[1]]
		
	def update(self):
		"""update everything in the game space"""
		remove_set = set()
		self.remove_pilot_set = set()
		
		# vessels
		for pilot in self.pilot_list:
			pilot.update()
			dock_set = pilot.vessel.group_dock_range(self.pilot_list)
			if dock_set:
				pilot.vessel.glow = max(pilot.vessel.GLOW, pilot.vessel.glow)
			collected_set = pilot.vessel.group_dock_collide(self.loot_set)
			for loot in collected_set:
				pilot.collect(loot)
			self.loot_set.difference_update(collected_set)
			collide_set = pilot.vessel.group_collide(self.rock_set)
			for rock in collide_set:
				pilot.vessel.bounce(rock)
				pilot.damage(self.ROCK_DAMAGE)
				
		for pilot in self.remove_pilot_set:
			self.pilot_list.remove(pilot)
			#del pilot
			
		spawned_pilot = self.zone.spawn_pilot()
		if spawned_pilot:
			self.pilot_list.append(spawned_pilot)
			
		# nodes
		for node in self.node_list:
			node.update()
			
		# weapons
		remove_set = set()
		for wpn in self.wpn_set:
			wpn.update()
			wpn.hit_target()
			if wpn.is_done():
				remove_set.add(wpn)
		self.wpn_set.difference_update(remove_set)
		
		# explosions
		remove_set = set()
		for explosion in self.explosion_set:
			explosion.update()
			if explosion.is_done():
				remove_set.add(explosion)
		self.explosion_set.difference_update(remove_set)
		
		# rocks
		remove_set = set()	
		for rock in self.rock_set:
			rock.update()
			if rock.outside_active_area():
				remove_set.add(rock)
			else:
				for wpn in self.wpn_set:
					if wpn.hit(rock):
						rock.die()
						remove_set.add(rock)
		self.rock_set.difference_update(remove_set)
		
		while len(self.rock_set) < self.zone.rock_density:
			self.rock_set.add(SpaceObj.RandomRock())
		
		
		# loot
		remove_set = set()	
		for loot in self.loot_set:
			loot.update()
			if loot.outside_active_area():
				remove_set.add(loot)
		self.loot_set.difference_update(remove_set)
		
		
		
		# debris
		remove_set = set()	
		for debris in self.debris_set:
			debris.update()
			if debris.outside_active_area():
				remove_set.add(debris)
		self.debris_set.difference_update(remove_set)
		
		while len(self.debris_set) < self.zone.debris_density:
			self.debris_set.add(SpaceObj.RandomDebris())
		
		# stars
		remove_set = set()	
		for star in self.star_set:
			star.update()
			if star.outside_active_area():
				remove_set.add(star)
		self.star_set.difference_update(remove_set)
		
		while len(self.star_set) < self.zone.star_density:
			self.star_set.add(SpaceObj.RandomStar())
			
		# screen objects
		for screenobj in self.screenobj_list:
			screenobj.update()
			
		
						
						
	def get_spawn_pt(self, on_screen=False, plane=1):
		"""Gets a  random spawn point within the active area."""
		x = random.randint(self.center[0] - self.frame_size[0] * plane  , \
					self.center[0] + self.frame_size[0] * plane)
		y = random.randint(self.center[1] - self.frame_size[1] * plane  , \
					self.center[1] + self.frame_size[1] * plane  )
		if on_screen:
			return [x,y]
		else:
			while self.pt_on_screen([x,y], plane):
				x = random.randint(self.center[0] - self.frame_size[0] * plane, \
							self.center[0] + self.frame_size[0] * plane)
				y = random.randint(self.center[1] - self.frame_size[1] * plane, \
							self.center[1] + self.frame_size[1] * plane)
			return [x,y]
	
	def pt_on_screen(self, pt, plane=1):
		"""Is the given point on screen?"""
		[x,y] = pt
		return (x < self.center[0] + self.frame_center[0] * plane and \
				x > self.center[0] - self.frame_center[0] * plane) and \
				(y < self.center[1] + self.frame_center[1] * plane and \
				y > self.center[1] - self.frame_center[1]* plane)
				
	def pt_outside_active_area(self, pt, plane=1):
		"""T/F is the point outside the active area? The active area is a rectangle centered
		on the center of the screen, two screens tall and two screens wide."""
		[x,y] = pt
		return x > self.center[0] + self.frame_size[0] * plane   or \
				x < self.center[0] - self.frame_size[0] * plane   or \
				y > self.center[1] + self.frame_size[1] * plane   or \
				y < self.center[1] - self.frame_size[1] * plane  		
				
				
	
	def new_zone(self, zone, vessel):
		
		self.zone = zone
		self.pilot_list = []
		self.pilot_list = zone.pilot_list
		self.pilot_list.append(self.player)
		
		self.node_list = []
		self.node_list = zone.node_list
		
		self.player.target = None
		self.player.focus = None
		self.player.nav = None
		
		self.centered_on = vessel
		self.center_camera()
		
		self.star_set = set()	
		while len(self.star_set) < self.zone.star_density:
			self.star_set.add(SpaceObj.RandomStar(True))
		
		self.rock_set = set()	
		while len(self.rock_set) < self.zone.rock_density:
			self.rock_set.add(SpaceObj.RandomRock())
			
		self.loot_set = set()
		self.debris_set = set()
		self.explosion_set = set()
		self.wpn_set = set()
			
			
		if self.player:
			self.screenobj_list.append(ScreenObj.FocusArrow(self.player))
			self.screenobj_list.append(ScreenObj.TargetArrow(self.player))
			self.screenobj_list.append(ScreenObj.NavArrow(self.player))
			
			
	def player_jump(self):
		if not self.player.nav.in_jump_range(self.player):
			print "not in range"
			return		# if not in jump range, do nothing
		else:
			self.new_zone(self.player.nav.zone, self.player.vessel)
	

	
	