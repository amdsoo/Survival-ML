# Ariel Morandy -  python! March 2023
import declaration as d
from declaration import *
import pygame
import classes as c
'''import simulation as simu'''
import random


pygame.init()
pygame.font.init()

pygame.display.set_caption('Survival ML')

# basic font for Large Text
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# small font for user typed
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)

# show a long message
display_long_message = False
long_message = ""


class SurvivalGameAI:

	def __init__(self):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		# create the main Objects
		self.world = c.World()
		self.grid = c.Grid()
		self.score = 0

		# initialisation of counters
		self.nb_prey      = 0
		self.nb_prey_max  = 0

		self.nb_predator    = 0
		self.nb_predator_max = 0

		self.prediction_move =0
		self.prediction_move_ok =0
		self.prediction_eat =0
		self.prediction_eat_ok =0
		self.prediction_reproduce =0
		self.prediction_reproduce_ok =0




		self.reset()



	def reset (self):
		# load data starter , plants , preys and 4 predators
		# create randomly plants (fake randomness)
		self.score = 0
		d.all_sprites_animal_list.empty()
		d.all_sprites_plant_list.empty()
		d.animal_list.clear()
		d.plant_list.clear()

		# track of game cycle
		self.world.iteration_index = 0
		self.world.cycle = 0

		# re-initialisation of counters
		self.nb_prey     = number_preys_ini
		self.nb_prey_max = number_preys_ini
		self.nb_predator      = number_predators_ini
		self.nb_predator_max  = number_predators_ini

		self.prediction_move =0
		self.prediction_move_ok =0
		self.prediction_eat =0
		self.prediction_eat_ok =0
		self.prediction_reproduce =0
		self.prediction_reproduce_ok =0



		i = 0
		while i < number_plants_ini:
			x = random.randint(tile_size, screen_width - 2 * tile_size)
			y = random.randint(2 * tile_size, screen_height - 2 * tile_size)
			energy_reserve = random.randint(175, 300)
			plant = c.Plant(x, y, 0)
			plant.energy_reserve = energy_reserve
			d.plant_list.append(plant)
			d.all_sprites_plant_list.add(plant)
			i += 1

		i = 0
		while i < number_preys_ini:
			x = random.randint(tile_size, screen_width - 2 * tile_size)
			y = random.randint(2 * tile_size, screen_height - 2 * tile_size)
			prey = c.Prey(x, y, 0)
			prey.energy_reserve = random.randint(prey.energy_reserve, prey.energy_reserve_max)
			d.animal_list.append(prey)
			d.all_sprites_animal_list.add(prey)
			i += 1


		if number_predators_ini == 1:
			x= screen_width/2
			y = screen_height/2
			predator = c.Predator(x, y, 0)
			predator.energy_reserve = random.randint(predator.energy_reserve_max * 0.8, predator.energy_reserve_max)
			d.animal_list.append(predator)
			d.all_sprites_animal_list.add(predator)
		else:

			i = 0
			while i < number_predators_ini:
				x = random.randint(tile_size, screen_width - 2 * tile_size)
				y = random.randint(2 * tile_size, screen_height - 2 * tile_size)
				predator = c.Predator(x, y, 0)
				predator.energy_reserve = random.randint(predator.energy_reserve_max*0.8, predator.energy_reserve_max)
				d.animal_list.append(predator)
				d.all_sprites_animal_list.add(predator)
				i += 1


	def update_ui (self):

		self.clock.tick(60)

		# refresh the graphics
		self.screen.fill(GREY)
		self.grid.draw(self.screen)
		self.world.draw(self,self.screen)


		d.all_sprites_plant_list.draw(self.screen)
		d.all_sprites_animal_list.draw(self.screen)

		d.all_sprites_animal_list.update()
		d.all_sprites_plant_list.update()
		all_sprites_tmp.draw(self.screen)

		for animal in d.animal_list:
			animal.draw_vision_line(self.screen)

		self.world.draw_gauge(self, self.screen)

		pygame.display.update()
