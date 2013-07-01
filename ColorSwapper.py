"""
PaletteSwapper is for generating new colorations sprites.
"""



import sys, pygame, glob, fnmatch
from pygame.locals import *

pygame.init()

# constants

# vessel glow list
# 0: 'Off'			Resting
# 1: 'Dim'
# 2: 'Glow'			Shoot/Dock
# 3: 'Bright'		Shield/Thrust 
#				R   G   B     R   G   B
GLOW = [	[(128,128,  0),( 90, 90,  0)], \
			[( 25,175,175),( 90,150,125)], \
			[(  0,225,225),( 25,175,175)], \
			[(100,255,255),(  0,225,225)]]
			
			
# vessel ftl color lists
# 0: 'darkest and most transparent (hopefully)
# 4: 'lightest

FTL =  [ [[( 90,150,125),( 0, 0, 0, 0)],[( 0, 0, 0, 0),( 0, 0, 0, 0)]], \
		 [[( 25,175,175),( 90,150,125)],[( 0, 0, 0, 0),( 0, 0, 0, 0)]], \
		 [[(  0,225,225),( 25,175,175)],[( 90,150,125),( 0, 0, 0, 0)]], \
		 [[(100,255,255),(  0,225,225)],[( 25,175,175),( 90,150,125)]], \
		 [[(255,255,255),(100,255,255)],[(  0,225,225),( 25,175,175)]], \
		 [[(255,255,255),(255,255,255)],[(100,255,255),(  0,225,225)]], \
		 [[(255,255,255),(255,255,255)],[(255,255,255),(100,255,255)]]]	
				
# the color of the flag frame on grey ships
GREY_FLAG_BORDER = (175,175,175)
# vessel coloring dict			  R   G   B     R   G   B
COLORINGS = {	'Army'		: [(  0,180,  0),(  0,115,  0)], \
				'Blue'		: [( 50, 50,255),(  0,  0,150)], \
				'Builder'	: [(200,200,200),(255,128,  0)], \
				'Civ'		: [(255,255,255),(128,  0,128)], \
				'Garden'	: [(230,230,230),(  0,128,  0)], \
				'Green'		: [(  0,255,  0),(  0,150,  0)], \
				'Grey'		: [(200,200,200),(150,150,150)], \
				'Medic'		: [(255,255,255),(225,  0,  0)], \
				'Miner'		: [(200,200,200),(175, 50, 25)], \
				'Navy'		: [(  0,100,200),(  0, 50,150)], \
				'Pirate'	: [(230,230,230),(100, 90, 50)], \
				'Police'	: [(230,230,230),(  0,  0,200)], \
				'Red'		: [(255,  0,  0),(150,  0,  0)], \
				'Science'	: [(255,255,255),(  0,150,150)], \
				'Yellow'	: [(255,255,  0),(150,150,  0)] }
				
				
# flag name keys
FLAG_LIST = ['Army', 'Blue', 'Builder', 'Civ', 'Garden', 'Green', 'Grey', 'Medic', 'Miner', 'Navy', \
			 'Pirate', 'Police', 'Red', 'Science', 'Yellow']
# ship flag locations
FLAG_LOCS = {	'Stingray'	: [20,12], \
				'Raindrop'	: [11, 7], \
				'Discus'	: [21,21]}

# station flag locations and angles
STATION_FLAGS = { 'Dome' : { 'Loc' : [[37,37],[103,37],[103,103],[37,103]], \
							 'Ang' : [ 0,      -90,     -180,     -270   ]}}
							 


def add_station_flags(type, flag_list, img_list):
	"""Changes the station's flags."""
	new_img_list = []
	for img in img_list:
		new_img = img.copy()
		for i in range(len(flag_list)):
			flag_img = pygame.transform.rotate(FLAG_IMGS[flag_list[i]], \
											STATION_FLAGS[type]['Ang'][i])
			new_img.blit(flag_img, STATION_FLAGS[type]['Loc'][i])
		new_img_list.append(new_img)
	return new_img_list
	

def add_flag(flag_key, type_key, img_list):
	"""Given a list of images of ships in the glow stats and strings as flag and 
	type keys, return a list of new images with the flag blitted onto each image."""
	new_img_list = []
	for img in img_list:
		new_img = img.copy()
		new_img.blit(FLAG_IMGS[flag_key], FLAG_LOCS[type_key])
		new_img_list.append(new_img)
	return new_img_list


def recolor_vessel(old_key, new_key, img_list):
	"""Given an img_list of vessels in the glow states, return a list of new images
	with the new coloration."""
	new_img_list = []
	for img in img_list:
		new_img = double_replace_color(COLORINGS[old_key], COLORINGS[new_key], img)
		new_img_list.append(new_img)
	return new_img_list
	
def make_ftl(img):
	"""Make versions of img with colors corresponding to FTL."""
	new_img_list = []
	for state in range(len(FTL)):
		new_img = double_replace_color(GLOW[0], FTL[state][0], img)
		new_img = double_replace_color(COLORINGS['Grey'], FTL[state][1], new_img)
		new_img_list.append(new_img)
	return new_img_list
	
def remove_flag_frame(img):
	new_img = replace_color(GREY_FLAG_BORDER, COLORINGS['Grey'][0], img)
	return new_img
	
	
def make_glow(img):
	"""Given an img of a vessel in the 'Off' (GLOW[0]) state, return a list of images
	 in each glow state."""
	new_img_list = []
	for state in range(len(GLOW)):
		new_img = double_replace_color(GLOW[0], GLOW[state], img)	
		new_img_list.append(new_img)
	return new_img_list	
	
	
def double_replace_color(color_list1, color_list2, img):
	img = img.copy()
	pixObj = pygame.PixelArray(img)
	img_size = img.get_size()
	for x in range(img_size[0]):
		for y in range(img_size[1]):
			if pixObj[x][y] == img.map_rgb(color_list1[1]):
				pixObj[x][y] = color_list2[1]
			elif pixObj[x][y] == img.map_rgb(color_list1[0]):
				pixObj[x][y] = color_list2[0]
	del pixObj	
	return img
	
def replace_color(color1, color2, img):
	img = img.copy()
	pixObj = pygame.PixelArray(img)
	img_size = img.get_size()
	for x in range(img_size[0]):
		for y in range(img_size[1]):
			if pixObj[x][y] == img.map_rgb(color1):
				pixObj[x][y] = color2
	del pixObj	
	return img
	
	
def save_img_list(prefix, img_list):
	"""Save the images in the image list as .png, named with the prefix + index number."""
	for i in range(len(img_list)):
		pygame.image.save(img_list[i], './SavedImages/'+prefix + str(i) + '.png')

def load_grey_img(name):
	"""Load and return and image."""
	img = pygame.image.load('./GreyImages/'+name+'.png')
	return img


def load_flags():
	img_names = glob.glob('./Images/Flag/*.png')
	global FLAG_IMGS
	FLAG_IMGS = {}
	for img_name in img_names:
		for flag in FLAG_LIST:
			if fnmatch.fnmatch(img_name, '*'+flag+'*'):
				FLAG_IMGS[flag] = pygame.image.load(img_name)




def main():
	load_flags()
	
	# use this to make things glow
	"""
	img = load_grey_img('CircleGlow')
	glow_list = make_glow(img)
	save_img_list('Glow', glow_list)
	"""
	# use this to make things FTL
	
	type = 'Longboat'
	img = load_grey_img(type)
	img = remove_flag_frame(img)
	ftl_list = make_ftl(img)
	save_img_list(type, ftl_list)
	
	# use this for vessels 
	"""
	type = 'Raindrop'
	grey_img = load_grey_img(type)
	grey_glow_list = make_glow(grey_img)
	for flag in FLAG_LIST:
		color_glow_list = recolor_vessel('Grey', flag, grey_glow_list)
		save_img_list(flag, color_glow_list)
	"""
	
	# use this for ships 
	"""
	type = 'Discus'
	grey_img = load_grey_img(type)
	grey_glow_list = make_glow(grey_img)
	for flag in FLAG_LIST:
		color_glow_list = recolor_vessel('Grey', flag, grey_glow_list)
		color_glow_list = add_flag(flag, type, color_glow_list)	
		save_img_list(flag, color_glow_list)
	"""
	
	
	# use this for stations
	"""
	type = 'Dome'
	flag_list = ['Medic', 'Police', 'Miner', 'Garden']	# make sure you have the right number of flags!
	grey_img = load_grey_img(type)
	grey_glow_list = make_glow(grey_img)
	flag_glow_list = add_station_flags(type, flag_list, grey_glow_list)
	save_img_list('Grey', flag_glow_list)
	"""
	


if __name__ == '__main__':
	main()