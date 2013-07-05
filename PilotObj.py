"""
PilotObj
"""

import math, random

import helper, SpaceObj, GameObj, EquipObj

CARGO_LIST = ['People', 'Crystal']


def init(game):
	global GAME
	GAME = game

class PilotObj:

	def __init__(self, vessel, equip):
		self.vessel = vessel
		self.equip = equip
		self.shield_max = equip.shield_max
		self.shield_regen = equip.shield_regen
		self.shield = equip.shield_max
		self.cargo_max = equip.cargo_max
		self.alive = True
		
		self.cargo = {key:0 for key in CARGO_LIST}
		
		self.target = None
		self.focus = None
		self.nav = None
		
	def draw(self):
		self.vessel.draw()
		
	def update(self):
		if self.shield <= 0:
			self.die()
		else:
			self.shield += self.shield_regen
			self.shield = min(self.shield,self.shield_max)
		self.vessel.update()
		if not self.focus in GAME.pilot_list:
			self.focus = None
		if not self.target in GAME.pilot_list:
			self.target = None
			
	def thrust_for(self):				# accelerate forward	
		self.vessel.glow = max(self.vessel.glow, self.vessel.GLOW)			
		self.vessel.accel = self.equip.thrust		
	
	def thrust_rev(self):				# accelerate in reverse		
		self.vessel.glow = max(self.vessel.glow, self.vessel.GLOW)		
		self.vessel.accel = self.equip.retro
	
	def thrust_off(self):				# stop accelerating
		self.vessel.accel = 0
	
	def turn_left(self):				# turn left
		self.vessel.angvel = self.equip.turn_rate
	
	def turn_right(self):				# turn right
		self.vessel.angvel = -self.equip.turn_rate
	
	def turn_off(self):					# stop turning
		self.vessel.angvel = 0
		
	def shoot_main(self):
		if not None == self.equip.main_wpn:
			GAME.wpn_set.add(self.equip.main_wpn(self.vessel.pos,self.vessel.angle,self.target))
			self.vessel.glow = max(self.vessel.glow, self.vessel.BRIGHT)
	
	def shoot_alt(self):
		if self.equip.alt_wpn:
			GAME.wpn_set.add(self.equip.alt_wpn(self.vessel.pos,self.vessel.angle,self.target))
			self.vessel.glow = max(self.vessel.glow, self.vessel.BRIGHT)
		
	def collect(self, loot):
		for key in loot.cargo:
			self.cargo[key] += loot.cargo[key]
			
	def damage(self, amount):
		self.shield -= amount
		self.vessel.glow = max(self.vessel.glow, self.vessel.BRIGHT)
			
	def die(self):
		self.alive = False
		self.vessel.die()
		GAME.remove_pilot_set.add(self)
		self.vessel.dock_radius = -self.vessel.dock_radius		# so you can't collect anything that you release upon death
		for i in range(8):
			if random.random() < .7:
				GAME.loot_set.add(SpaceObj.Escapepod(self.vessel.coloring, self.vessel.pos))
				
	def jump(self):
		self.vessel.jump()
		GAME.remove_pilot_set.add(self)
				
	def dock_range(self, pilot):
		"""Is my vessel within docking range ofthe other pilot's vessel?"""
		return self.vessel.dock_range(pilot.vessel)
			
	def group_dock_range(self, group):
		"""Which members of the pilot group are in docking range?"""
		dock_set = set()
		for pilot in group:	
			if not self == pilot.vessel and self.dock_range(pilot.vessel):
				dock_set.add(pilot)
		return dock_set
				
	def focus_dock(self):
		"""Dock with the focus object."""
		if not self.focus:
			pass		# do nothing if there is no focus
		elif not self.dock_range(self.focus):
			pass		# do nothing if the focus is out of range
		elif self.focus.vessel.is_station():
			self.shield = self.equip.shield_max	# if it's a station, repair the shields
			if self.focus.takes_cargo():
				for key in self.cargo:
					self.focus.cargo[key] += self.cargo[key]
					self.cargo[key] = 0
				
	def takes_cargo(self):
		return self.vessel.is_station()
		
	# progress your focus forward and back through the pilot list
	def change_focus(self):
		if len(GAME.pilot_list) == 0:
			self.focus = None
			return
		if self.focus == None:
			self.focus = GAME.pilot_list[0]
		else:
			index = GAME.pilot_list.index(self.focus)
			if index + 1 == len(GAME.pilot_list):
				self.focus = GAME.pilot_list[0]
			else:
				self.focus = GAME.pilot_list[index+1]
		if self.focus == self and len(GAME.pilot_list) >1:
			self.change_focus()
	
	def change_focus_rev(self):
		if len(GAME.pilot_list) == 0:
			self.focus = None
			return
		if self.focus == None:
			self.focus = GAME.pilot_list[-1]
		else:
			index = GAME.pilot_list.index(self.focus)
			if index - 1 == -1:
				self.focus = GAME.pilot_list[-1]
			else:
				self.focus = GAME.pilot_list[index-1]
		if self.focus == self and len(GAME.pilot_list) >1:
			self.change_focus_rev()
		
	# progress your target forward and back through the pilot list
	def change_target(self):
		if len(GAME.pilot_list) == 0:
			self.target = None
			return
		if self.target == None:
			self.target = GAME.pilot_list[0]
		else:
			index = GAME.pilot_list.index(self.target)
			if index + 1 == len(GAME.pilot_list):
				self.target = GAME.pilot_list[0]
			else:
				self.target = GAME.pilot_list[index+1]
		if self.target == self and len(GAME.pilot_list) >1:
			self.change_target()
	
	def change_target_rev(self):
		if len(GAME.pilot_list) == 0:
			self.target = None
			return
		if self.target == None:
			self.target = GAME.pilot_list[-1]
		else:
			index = GAME.pilot_list.index(self.target)
			if index - 1 == -1:
				self.target = GAME.pilot_list[-1]
			else:
				self.target = GAME.pilot_list[index-1]
		if self.target == self and len(GAME.pilot_list) >1:
			self.change_target_rev()
		

class RandomDirection(PilotObj):

	def __init__(self, vessel, equip):
		PilotObj.__init__(self, vessel, equip)
		self.vessel.angle = random.randrange(360)
		self.thrust_for()
		self.age_max = 500
		
	def update(self):
		PilotObj.update(self)
		if self.vessel.age > self.age_max:
			self.jump()








