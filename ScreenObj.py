

import glob, fnmatch, pygame, random

import helper




GAME = None

def init(game):
	global GAME, ARROWGLOW_IMGS, CIRCLEGLOW_IMGS, ARROWCOLOR_IMGS, CIRCLECOLOR_IMGS
	GAME = game
	
	# load images here
	
	file_names = glob.glob('./Images/ScreenObj/Arrow/Glow*.png')
	ARROWGLOW_IMGS = []
	for file in file_names:
		ARROWGLOW_IMGS.append(pygame.image.load(file))
		
	file_names = glob.glob('./Images/ScreenObj/Circle/Glow*.png')
	CIRCLEGLOW_IMGS = []
	for file in file_names:
		CIRCLEGLOW_IMGS.append(pygame.image.load(file))
		
	ARROWCOLOR_IMGS = [pygame.image.load('./Images/ScreenObj/Arrow/Red.png'), \
					   pygame.image.load('./Images/ScreenObj/Arrow/Yellow.png'), \
					   pygame.image.load('./Images/ScreenObj/Arrow/Green.png'), \
					   pygame.image.load('./Images/ScreenObj/Arrow/Blue.png')]
					   
	CIRCLECOLOR_IMGS = [pygame.image.load('./Images/ScreenObj/Circle/Red.png'), \
					   pygame.image.load('./Images/ScreenObj/Circle/Yellow.png'), \
					   pygame.image.load('./Images/ScreenObj/Circle/Green.png'), \
					   pygame.image.load('./Images/ScreenObj/Circle/Blue.png')]





class ScreenObj:
		
	def __init__(self, screen_pos, img):
		self.screen_pos = screen_pos
		self.img = img
		
	def draw(self):
		"""draws the object onto the screen"""
		img = self.choose_img()
		img_size = img.get_size()
		
		# find blit coordinates
		x = self.screen_pos[0] - int(img_size[0]/2)
		y = self.screen_pos[1] - int(img_size[1]/2)
		
		# and blit!
		GAME.frame.blit(img, [x,y])
		
	def choose_img(self):
		return self.img
		
	def update(self):
		pass
		
		
class GuideArrow(ScreenObj):

	def __init__(self, screen_pos, start_pilot, stop_pilot, img, alt_img=None):
		ScreenObj.__init__(self, screen_pos, img)
		self.start = start_pilot
		self.stop = stop_pilot
		self.angle = 0
		self.alt_img = alt_img
		
	def choose_img(self):
		if not self.stop and self.alt_img:
			return self.alt_img
		else:
			return pygame.transform.rotate(self.img, self.angle)
		
	def update(self):
		self.angle = helper.vec2ang([self.start.vessel.pos[0] - self.stop.vessel.pos[0], \
							self.start.vessel.pos[1] - self.stop.vessel.pos[1]])
							
							
class FocusArrow(GuideArrow):

	def __init__(self, player):
		screen_pos = [16, GAME.frame_size[1] - 28]
		start_pilot = player
		stop_pilot = player.focus
		img = ARROWCOLOR_IMGS[3]
		alt_img = CIRCLECOLOR_IMGS[3]
		GuideArrow.__init__(self, screen_pos, start_pilot, stop_pilot, img, alt_img)
		
		
		
	def update(self):
		self.stop = self.start.focus
		if self.stop:
			GuideArrow.update(self)
			
			
class TargetArrow(GuideArrow):

	def __init__(self, player):
		screen_pos = [GAME.frame_size[0] - 28, 28]
		start_pilot = player
		stop_pilot = player.target
		img = ARROWCOLOR_IMGS[0]
		alt_img = CIRCLECOLOR_IMGS[0]
		GuideArrow.__init__(self, screen_pos, start_pilot, stop_pilot, img, alt_img)
		
	def update(self):
		self.stop = self.start.target
		if self.stop:
			GuideArrow.update(self)
			
			
class NavArrow(GuideArrow):

	def __init__(self, player):
		screen_pos = [GAME.frame_size[0] - 28, GAME.frame_size[1] - 28]
		start_pilot = player
		stop_pilot = player.nav
		img = ARROWGLOW_IMGS[3]
		alt_img = CIRCLEGLOW_IMGS[3]
		GuideArrow.__init__(self, screen_pos, start_pilot, stop_pilot, img, alt_img)
		
	def update(self):
		self.stop = self.start.nav
		if self.stop:
			self.angle = helper.vec2ang([self.start.vessel.pos[0] - self.stop.parallax_obj.pos[0], \
							self.start.vessel.pos[1] - self.stop.parallax_obj.pos[1]])
	
	
	
	
	
	
	
	
	
	
	