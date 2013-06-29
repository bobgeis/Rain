"""
Rain
"""



__title__ = 'Rain'
__version__ = '5ish'
__author__ = 'Bob Geis'
__date__ = '2013-06-27'


# import stuff
import random, sys, pygame, math
from pygame.locals import *

# import game modules
import helper, GameObj, SpaceObj, ScreenObj, ZoneObj, PilotObj, EquipObj

# set constants
WINWID = 800				# the size of the game window
WINHEI = 600
WINSIZE = [WINWID,WINHEI]
HALFWINWID = int(WINWID/2) 	# half size of the game window, in case it is important
HALFWINHEI = int(WINHEI/2)
WINCENT = [HALFWINWID,HALFWINHEI]
FPS = 30					# frames per second, used in the main game loop FPSCLOCK.tick(FPS) to govern the game speed

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

# important colors
BGCOLOR = 	BLACK


# some helper functions

def init():
	"""This does some initialization that we want."""
	SpaceObj.init(GAME)
	ScreenObj.init(GAME)
	PilotObj.init(GAME)
	EquipObj.init(GAME)
	ZoneObj.init(GAME)

# this quits the game and exits python
def terminate():
	"""Quit the game and exit python."""
	pygame.quit()
	sys.exit()	
	
	
	
	
	
	
# call the main() function to run the game
def main():  
	"""main() is divided into approximately four sections
	the first part sets up the game, initializes variables and things
	the last three parts are contained within the main game loop: "while True:"
	the second part is the event handler, it loops through all the events and responds appropriately
	the third part updates the game logic in response to the events and evolution of the game state
	the fourth part draws everything to the screen."""
	
	global FPSCLOCK, FRAME, BASICFONT, GAME
	
	
	# Part One: Setup
	# initialize pygame
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	FRAME = pygame.display.set_mode((WINWID, WINHEI))
	pygame.display.set_caption('Rain')
	
	# font		# fonts are initialized by the pygame.init() call above, so global fonts need to be declared after that
	BASICFONT = pygame.font.Font('freesansbold.ttf', 12)
	
	paused = False
	
	GAME = GameObj.GameObj(FRAME)
	init()							# make a GAME object, then call init, because many modules use the GAME as a global for camera info 
	
	
	
	player_ship = SpaceObj.Stingray([0,0], 'Medic')
	player = PilotObj.PilotObj(player_ship, EquipObj.BasicEquip())
	GAME.player = player
	GAME.new_zone(ZoneObj.Starting())
	
	GAME.centered_on = player_ship
	
	player.focus = GAME.pilot_list[0]
	
	while True:  # main game loop

		# Part Two: Input
		# handle events
		
		for event in pygame.event.get():  # handle events
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			elif event.type == KEYUP and event.key == K_p:
				if paused:
					paused = False
				else:
					paused = True
			if paused or not player.alive:
				pass
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					player.thrust_for()
				elif event.key == K_DOWN:
					player.thrust_rev()
				elif event.key == K_LEFT:
					player.turn_left()
				elif event.key == K_RIGHT:
					player.turn_right()
				elif event.key == K_RSHIFT:
				 	player.thrust_for()
				elif event.key == K_SPACE:
				 	player.shoot_main()
				elif event.key == K_LSHIFT:
				 	player.shoot_alt()
				elif event.key == K_d:
				 	player.focus_dock()
				elif event.key == K_f:
					player.change_focus()
				elif event.key == K_g:
					player.change_focus_rev()
				elif event.key == K_t:
					player.change_target()
				elif event.key == K_y:
					player.change_target_rev()
			elif event.type == KEYUP:
				if event.key == K_UP or event.key == K_DOWN:
					player.thrust_off()
				elif event.key == K_LEFT or event.key == K_RIGHT:
					player.turn_off()
			
		
		
		# Part Three: Evolve
		# update game logic
		
		if not paused:
			GAME.update()
		
		
		# Part Four: Output 		
		# fill the draw queue. Remember FIFO and later things are drawn on top of earlier things.
		GAME.draw()
		
		
		player_text = BASICFONT.render('Shields: '+str(int(player.shield))+ \
					'     Crystal: '+str(player.cargo['Crystal'])+ \
					'     People: '+str(player.cargo['People']), True, WHITE)
		FRAME.blit(player_text, [0,0])
		
		if player.focus:
			focus_text = BASICFONT.render('Shields:  '+str(int(player.focus.shield))+ \
						'     Crystal: '+str(player.focus.cargo['Crystal'])+ \
						'     People: '+str(player.focus.cargo['People']), True, WHITE)
			FRAME.blit(focus_text, [0,WINHEI-12])
			
		if player.target:
			target_text = BASICFONT.render('Shields:  '+str(int(player.target.shield))+ \
						'     Crystal: '+str(player.target.cargo['Crystal'])+ \
						'     People: '+str(player.target.cargo['People']), True, WHITE)
			img_size = target_text.get_size()
			FRAME.blit(target_text, [WINWID-img_size[0],0])
		
		# draw the paused box
		if paused:
			pause_text = BASICFONT.render("Game Paused", True, WHITE)
			img_size = pause_text.get_size()
			pygame.draw.rect(FRAME, BLUE, \
					(WINCENT[0] - img_size[0]/2, WINCENT[1] - img_size[1]/2, \
					img_size[0], img_size[1])) 
			FRAME.blit(pause_text, [WINCENT[0] - img_size[0]/2, WINCENT[1] - img_size[1]/2])
			
		# now we actually draw everything
		pygame.display.update()
		
		# tick the game clock FPS times per second
		FPSCLOCK.tick(FPS)

				
	
# this calls main() only if the script is run, and not if it is being imported elsewhere (like for testing)
if __name__ == '__main__':
	main()