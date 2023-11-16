# Ariel Morandy - Fev 2023
import declaration as d
from declaration import *
import classes as c
import random
import method as m
import pygame


def gameupdate_action(game,animal,final_move):
	score = 0
	reward = 0
	game_over = False
	newanimal = None

	# decode action
	action = 0
	if final_move [1] == 1:
		action = 1
	elif final_move [2] == 1:
		action = 2
	elif final_move [3] == 1:
		action = 3

	# step 1: Reproduction
	go = True

	# in case of a predator, we use the machine learning algo
	if action == 3: # "Reproduce"

		game.prediction_reproduce += 1
		ratio = game.nb_predator * 2 / game.nb_prey
		if ratio > 1: ratio = 1

		if animal.energy_reserve > animal.energy_reproduction:

			#generation of an animal.
			x, y = animal.rect.centerx+random.randint(-tile_size,tile_size),animal.rect.centery+random.randint(-tile_size,tile_size)
			newanimal = c.Predator(x,y,random.randint(0,360))
			d.animal_list.append(newanimal)
			d.all_sprites_animal_list.add(newanimal)
			newanimal.state = "Hunting"
			newanimal.move = False
			newanimal.generation = animal.generation + 1

			# cost for reproduction.
			animal.energy_reserve = animal.energy_reserve - animal.energy_reproduction_cost

			animal.move = False

			# score increases because of generation of new predator
			score  = predator_reproduce_reward
			reward = predator_reproduce_reward
			game.prediction_reproduce_ok += 1
		else:
			# the action from AI cannot be executed because lack of energy. -> penalty
			score  = -predator_reproduce_reward
			reward = -predator_reproduce_reward

	elif action == 2: # "Eat"

		game.prediction_eat += 1
		# check if the animal can eat within a circle <= tilesize
		# Predator --> Prey
		lunch = False
		lunch, food = m.capture_food(animal)
		if lunch:
			# the animal is eating
			animal.move = False
			go = False
			animal.state = "Eating"
			'''print("Animal Eating")'''
			animal.energy_reserve = animal.energy_reserve + food.energy_reserve

			# we kill the Plant or the Prey
			food.energy_reserve = 0

			if animal.energy_reserve > animal.energy_reserve_max:
				animal.energy_reserve = animal.energy_reserve_max

			# score increases because of eating was successfull
			score  = predator_eat_reward
			reward = predator_eat_reward
			game.prediction_eat_ok += 1
		else:
			# the action from AI cannot be executed because no prey available . -> penalty
			score  = -predator_eat_reward
			reward = -predator_eat_reward

	elif action == 1: # "Move" and go
		game.prediction_move += 1
		# step 3: Move
		# if the animal has finished its step we recompute a direction
		if  animal.move is False and animal.state =="Hunting" :
			#if Predator has locked the prey, we don't change direction
			animal.energy_reserve = animal.energy_reserve - animal.energy_per_move
			if isinstance(animal,c.Predator) and animal.vision_lock:
				'''print ("Predator hunting")'''
				# score increases because of the AI gave the right advice
				score  = predator_move_reward
				reward = predator_move_reward
				game.prediction_move_ok += 1
			else:
				# we recompute an angle, randomly.
				angle = random.randint(animal.angle -animal.direction_change_angle, animal.angle+ animal.direction_change_angle)
				angle = angle % 360
				animal.angle = angle
				animal.rotate()
				score  = -predator_move_reward
				reward = -predator_move_reward

		animal.move = True

	# final check, if predator is not dead
	animal.energy_reserve = animal.energy_reserve - animal.energy_per_cycle
	# and dies if no energy
	if animal.energy_reserve < 0:
		'''print("Predator died")'''
		# score decreases because of death of predator
		score  = - predator_reproduce_reward
		reward = - predator_reproduce_reward
		d.animal_list.remove(animal)
		pygame.sprite.Sprite.kill(animal)


	return reward, score


def gameupdate_refresh(game):
	nb_prey = 0
	nb_predator = 0

	go = True
	newanimal_list = []

	for animal in d.animal_list:
		if isinstance(animal, c.Prey):
			# 1/Most important, animal tries to reproduce
			if animal.energy_reserve > animal.energy_reproduction and game.nb_prey < number_prey_limit :
				# generation of a prey.
				x, y = animal.rect.centerx+random.randint(-tile_size,tile_size),animal.rect.centery+random.randint(-tile_size,tile_size)
				newanimal = c.Prey (x,y,random.randint(0,360))
				# cost for reproduction.
				animal.energy_reserve = animal.energy_reserve - animal.energy_reproduction_cost
				# we add to the list of new animal
				newanimal_list.append(newanimal)
				newanimal.generation = animal.generation + 1
				go = False
				animal.move = False

			# step 2: Food
			if go:
				# check if the animal can eat within a circle <= tilesize
				# Predator --> Prey
				# Prey --> Plant

				lunch = False
				lunch, food = m.capture_food(animal)

				if lunch:
					# the animal is eating
					animal.move = False
					'''go = False'''
					animal.state = "Eating"
					'''print("Animal Eating")'''
					animal.energy_reserve = animal.energy_reserve + food.energy_reserve

					# we kill the Plant
					food.energy_reserve = 0

					if animal.energy_reserve > animal.energy_reserve_max:
						animal.energy_reserve = animal.energy_reserve_max

			# step 3: Move
			# if the animal has finished its step we recompute a direction
			if animal.move is False and go:
				# we recompute an angle, randomly.
				angle = random.randint(animal.angle - animal.direction_change_angle,
				                       animal.angle + animal.direction_change_angle)
				angle = angle % 360
				animal.angle = angle
				animal.rotate()

				animal.move = True

	#adding newanimal in the regular list.
	for newanimal in newanimal_list:
		d.animal_list.append(newanimal)
		d.all_sprites_animal_list.add(newanimal)
		newanimal.state = "Hunting"
		newanimal.move = False

	newanimal_list.clear()

	# cleaning up for Plant
	for plant in d.plant_list:
		plant.energy_reserve = plant.energy_reserve -plant.energy_per_cycle

		if plant.energy_reserve <0 and plant.state == "Alive":
			plant.update()
			plant.state = "Dead"

		if plant.state == "Dead":
			plant.regeneration_step = plant.regeneration_step + 1

			if plant.regeneration_step == plant.regeneration_time:
				plant.state = "Alive"
				plant.regeneration_step = 0
				plant.energy_reserve = plant.energy_reserve_max
				plant.update()

	# cleaning up for Preys and counting few things
	for animal in d.animal_list:
		if isinstance(animal, c.Prey):

			# we count the prey
			nb_prey += 1

			# each prey loses energy
			animal.energy_reserve = animal.energy_reserve -animal.energy_per_cycle

			# and more if it moves
			if animal.move:
				animal.energy_reserve = animal.energy_reserve - animal.energy_per_move

			# and dies if no energy
			if animal.energy_reserve <0 :
				'''print("Animal died")'''
				d.animal_list.remove(animal)
				pygame.sprite.Sprite.kill(animal)

			if animal.state == "Eating":
				animal.state = "Hunting"
				animal.move = False

		elif isinstance(animal, c.Predator):
			# we only count predator
			nb_predator += 1


	# we update the counter
	game.nb_prey          = nb_prey
	game.nb_prey_max      = max (game.nb_prey    , game.nb_prey_max)

	game.nb_predator      = nb_predator
	game.nb_predator_max  = max (nb_predator, game.nb_predator_max)





