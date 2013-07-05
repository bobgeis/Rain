"""
Rain

This is the main file, run it to play the game.
You will need pygame!

Rain is a game similar to asteroids where you fly a space ship and collect 
space crystals and space pods and return them to the space station.  
There might be more added later. 

The controls are:

-Escape Key to quit.

-Left/Right Arrow Keys to rotate your ship left or right.

-Up/Down Arrow Keys to accelerate your ship forward or in reverse.

-Space Bar to fire the main weapon.

-Left Shift to fire the alternate weapon (not implemented atm).

-'D' Key to dock with the space station when you are in range.

-'F' and 'G' Keys to cycle through the focus list. 
You can dock with the current focus if it is a space station.

-'T' and 'Y' Keys to cycle through the target list. 
You can fire on the current target even if it isn't hostile.

Have fun!

Code and art by me.

Some Influences:

Rice Rocks made for Coursera:
http://www.codeskulptor.org/#user16_BQzpUJrvg8XGhHh.py 

Squirrel Eat Squirrel by Al Sweigart:
http://inventwithpython.com/pygame/chapter8.html

"""



__title__ = 'Rain'
__other_title__ = 'SpaceShip'
__other_other_title__ = 'Dwarves in Space'
__author__ = 'Bob Geis'
__email__ = 'bobgeis@gmail.com'


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


# colors	   R   G   B	
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
	BIGFONT = pygame.font.Font('freesansbold.ttf', 36)
	
	paused = False
	started = False
	
	GAME = GameObj.GameObj(FRAME)
	init()							# make a GAME object, then call init, because many modules use the GAME as a global for camera info 
	
	
	
	player_ship = SpaceObj.Stingray([0,0], 'Medic')
	player = PilotObj.PilotObj(player_ship, EquipObj.BasicEquip())
	GAME.player = player
	splash_zone = ZoneObj.Splash()
	GAME.new_zone(splash_zone, splash_zone.pilot_list[0].vessel)
	
	while True:  # main game loop

		# Part Two: Input
		# handle events
		
		for event in pygame.event.get():  # handle events
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			elif started and event.type == KEYUP and event.key == K_p:
				if paused:
					paused = False
				else:
					paused = True
			if not started:
				if  event.type == KEYUP and event.key == K_SPACE:
					started = True
					GAME.new_zone(ZoneObj.Starting(), player.vessel)
					player.focus = GAME.pilot_list[0]
					player.nav = GAME.node_list[0]
				else:
					pass
			elif paused or not player.alive:
				pass
			elif event.type == KEYDOWN:
				if event.key == K_UP:			# movement controls
					player.thrust_for()
				elif event.key == K_DOWN:
					player.thrust_rev()
				elif event.key == K_LEFT:
					player.turn_left()
				elif event.key == K_RIGHT:
					player.turn_right()
				elif event.key == K_RSHIFT:
				 	player.thrust_for()
				elif event.key == K_SPACE:		# weapon controls
				 	player.shoot_main()
				elif event.key == K_LSHIFT:
				 	player.shoot_alt()
				elif event.key == K_d:			# focus control
				 	player.focus_dock()
				elif event.key == K_f:
					player.change_focus()
				elif event.key == K_g:			# target control
					player.change_focus_rev()
				elif event.key == K_t:
					player.change_target()
				elif event.key == K_y:
					player.change_target_rev()
				elif event.key == K_j:
					GAME.player_jump()
			elif event.type == KEYUP:
				if event.key == K_UP or event.key == K_DOWN:		# movement controls again
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
		
		if started:
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
		if paused and started:
			pause_text = BASICFONT.render("Game Paused", True, WHITE)
			img_size = pause_text.get_size()
			pygame.draw.rect(FRAME, BLUE, \
					(WINCENT[0] - img_size[0]/2, WINCENT[1] - img_size[1]/2, \
					img_size[0], img_size[1])) 
			FRAME.blit(pause_text, [WINCENT[0] - img_size[0]/2, WINCENT[1] - img_size[1]/2])
		
		# if the game hasn't started yet, let's draw something to show that
		if not started:
			splash_text = BIGFONT.render("Rain", True, WHITE)
			splash_size = splash_text.get_size()
			FRAME.blit(splash_text, [WINCENT[0] - splash_size[0]/2, 64 - splash_size[1]/2])
			start_text = BASICFONT.render( \
					"Press Space to Begin", \
					True, WHITE)
			start_size = start_text.get_size()
			FRAME.blit(start_text, [WINCENT[0] - start_size[0]/2, WINHEI - 32 - start_size[1]/2])
			
		# now we actually draw everything
		pygame.display.update()
		
		# tick the game clock FPS times per second
		FPSCLOCK.tick(FPS)

				
	
# this calls main() only if the script is run, and not if it is being imported elsewhere (like for testing)
if __name__ == '__main__':
	main()