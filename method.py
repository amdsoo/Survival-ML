import math
import declaration as d
import classes as c
from declaration import *


# basic font for user typed
pygame.font.init()
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)


def capture_food (this):
	# works in S coordinates, for Predator and Prey
	lunch = False
	food = None

	x1, y1 = this.rect.centerx,this.rect.centery

	if isinstance(this,c.Prey):
		for food in d.plant_list:
			x2, y2 = food.rect.centerx, food.rect.centery
			if food.energy_reserve >0:
				distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
				if distance <tile_size:
					'''print (this,"has captured", food)'''
					lunch = True
					return lunch, food
	if isinstance(this,c.Predator):
		for food in d.animal_list:
			x2, y2 = food.rect.centerx, food.rect.centery
			if isinstance(food,c.Prey) and food.energy_reserve >0:
				distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
				if distance <tile_size:
					'''print (this,"has captured", food)'''
					lunch = True
					return lunch, food

	return lunch, food


def get_center_from_object(this):
	# works in W coordinates, for machine and Cargo
	x1_screen, y1_screen = this.rect.topleft
	x2_screen, y2_screen = this.rect.bottomright
	dx = x2_screen - x1_screen
	dy = y2_screen - y1_screen

	centerx, centery = this.x+dx, this.y+dy

	return centerx, centery


def find_closest_prey (this):

	# this method returns the closest Prey or None
	# draw vision Line
	radtodeg = math.pi / 180
	dist = this.vision_distance
	angle = this.angle
	animal_focus = None

	focus_list = []

	x0, y0 = this.rect.centerx, this.rect.centery

	# center line of vision and two lines representing the angular vision cone
	xc, yc = x0 + math.cos(angle * radtodeg) * dist, y0 - math.sin(angle * radtodeg) * dist
	angle = this.angle + this.vision_angle / 2
	xl, yl = x0 + math.cos(angle * radtodeg) * dist, y0 - math.sin(angle * radtodeg) * dist
	angle = this.angle - this.vision_angle / 2
	xr, yr = x0 + math.cos(angle * radtodeg) * dist, y0 - math.sin(angle * radtodeg) * dist

	linec = ((x0, y0), (xc, yc))
	linel = ((x0, y0), (xl, yl))
	liner = ((x0, y0), (xr, yr))

	for animal in d.animal_list:
		if animal !=this and isinstance(animal,c.Prey):
			clipped_linec = animal.rect.clipline(linec)
			clipped_linel = animal.rect.clipline(linel)
			clipped_liner = animal.rect.clipline(liner)

			if clipped_linec:
				start, end = clipped_linec
				x1, y1 = start
				x2, y2 = end
				mid_x = (x1 + x2) / 2
				mid_y = (y1 + y2) / 2
				distance = math.sqrt((mid_x - x0) ** 2 + (mid_y - y0) ** 2)
				focus_list.append ([distance,animal])
			if clipped_linel:
				start, end = clipped_linel
				x1, y1 = start
				x2, y2 = end
				mid_x = (x1 + x2) / 2
				mid_y = (y1 + y2) / 2
				distance = math.sqrt((mid_x - x0) ** 2 + (mid_y - y0) ** 2)
				focus_list.append ([distance,animal])
			if clipped_liner:
				start, end = clipped_liner
				x1, y1 = start
				x2, y2 = end
				mid_x = (x1 + x2) / 2
				mid_y = (y1 + y2) / 2
				distance = math.sqrt((mid_x - x0) ** 2 + (mid_y - y0) ** 2)
				focus_list.append ([distance,animal])

		# now we take the first in the list, who is the closest
		animal_focus = None
		if focus_list:
			focus_list.sort(key=lambda i: i[0])
			animal_focus = focus_list [0][1]

	return animal_focus






