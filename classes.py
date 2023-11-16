import math

from declaration import *
import declaration as d
import method as m
import pickle as pick


pygame.font.init()

# basic font for user typed
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# small font for user typed
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)


class World:
	def __init__(self):
		self.tile_list = []
		# load images
		grey_img = pygame.image.load('img/grey.png')
		colmax = screen_width // tile_size
		rowmax = screen_height// tile_size
		col_count = 0

		self.score = 0
		self.cycle = 0

		# number of iterations between two game update (nothing shoud run faster than this)
		self.iteration = 5
		# tracking game simulation trigger
		self.iteration_index = 0

		while col_count < colmax:
			# top level
			img = pygame.transform.scale(grey_img, (tile_size, tile_size))
			img_rect = img.get_rect()
			img_rect.x = col_count * tile_size
			img_rect.y = 0
			tile = (img, img_rect)
			self.tile_list.append(tile)

			# lowlevel
			img = pygame.transform.scale(grey_img, (tile_size, tile_size))
			img = pygame.transform.rotate(img, 180)
			img_rect = img.get_rect()
			img_rect.x = col_count * tile_size
			img_rect.y = rowmax* tile_size - tile_size
			tile = (img, img_rect)
			self.tile_list.append(tile)

			col_count +=1

	def draw(self, game, screen):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

		# create rectangle
		input_rect = pygame.Rect(tile_size, 0, 16 * tile_size, tile_size)
		pygame.draw.rect(screen, GREY, input_rect)
		text_surface = my_font.render("Cycle / " + str(self.cycle) , False, BLACK)
		screen.blit(text_surface, (input_rect.x + 5, 0))
		text_surface = my_font.render("Score /"+str(game.score), False, BLACK)
		screen.blit(text_surface, (input_rect.x + 10*tile_size, 0))

		# create Statistic
		input_rect2 = pygame.Rect(24*tile_size, 0, 12* tile_size, tile_size)
		pygame.draw.rect(screen, GREY, input_rect2)
		text_surface = my_font.render("Predators / " + str(game.nb_predator) +" Max /" +str(game.nb_predator_max), False, BLACK)
		screen.blit(text_surface, (input_rect2.x + 5, 0))

		input_rect3 = pygame.Rect(48*tile_size, 0, 12* tile_size, tile_size)
		pygame.draw.rect(screen, GREY, input_rect3)
		text_surface = my_font.render("Preys / " + str(game.nb_prey) +" Max /" +str(game.nb_prey_max), False, BLACK)
		screen.blit(text_surface, (input_rect3.x + 5, 0))

	def draw_gauge (self, game, screen):
		# we draw two gauges at the bottom right


		'''self.prediction_reproduce =0
		self.prediction_reproduce_ok =0'''

		guage_width =  1*tile_size
		guage_height = 3*tile_size
		xpos= 58


		if game.prediction_move!=0:
			bad_prediction  = 1-game.prediction_move_ok/game.prediction_move
			good_prediction = game.prediction_move_ok/game.prediction_move
		else:
			bad_prediction =1
			good_prediction=0

		# draw bad prediction
		guage_height_bad= guage_height*bad_prediction
		input_rect = pygame.Rect(xpos*tile_size,screen_height-guage_height-tile_size,guage_width,guage_height_bad)
		pygame.draw.rect(screen, RED, input_rect)

		text_surface = my_font_S.render("M/"+str(game.prediction_move), False, BLACK)
		screen.blit(text_surface, (input_rect.x-5, input_rect.y -15))

		# draw good prediction
		guage_height_good= guage_height*good_prediction
		input_rect = pygame.Rect(xpos*tile_size,screen_height-guage_height-tile_size+guage_height_bad,guage_width,guage_height_good)
		pygame.draw.rect(screen, GREEN, input_rect)

		if game.prediction_eat!=0:
			bad_prediction  = 1-game.prediction_eat_ok/game.prediction_eat
			good_prediction = game.prediction_eat_ok/game.prediction_eat
		else:
			bad_prediction =1
			good_prediction=0

		# draw bad prediction
		guage_height_bad= guage_height*bad_prediction
		input_rect = pygame.Rect((xpos+2)*tile_size,screen_height-guage_height-tile_size,guage_width,guage_height_bad)
		pygame.draw.rect(screen, RED, input_rect)

		text_surface = my_font_S.render("K/"+str(game.prediction_eat), False, BLACK)
		screen.blit(text_surface, (input_rect.x-5, input_rect.y -15))

		# draw good prediction
		guage_height_good= guage_height*good_prediction
		input_rect = pygame.Rect((xpos+2)*tile_size,screen_height-guage_height-tile_size+guage_height_bad,guage_width,guage_height_good)
		pygame.draw.rect(screen, GREEN, input_rect)


		if game.prediction_reproduce!=0:
			bad_prediction  = 1-game.prediction_reproduce_ok/game.prediction_reproduce
			good_prediction = game.prediction_reproduce_ok/game.prediction_reproduce
		else:
			bad_prediction =1
			good_prediction=0

		# draw bad prediction
		guage_height_bad= guage_height*bad_prediction
		input_rect = pygame.Rect((xpos+4)*tile_size,screen_height-guage_height-tile_size,guage_width,guage_height_bad)
		pygame.draw.rect(screen, RED, input_rect)

		text_surface = my_font_S.render("B/"+str(game.prediction_reproduce), False, BLACK)
		screen.blit(text_surface, (input_rect.x-5, input_rect.y -15))

		# draw good prediction
		guage_height_good= guage_height*good_prediction
		input_rect = pygame.Rect((xpos+4)*tile_size,screen_height-guage_height-tile_size+guage_height_bad,guage_width,guage_height_good)
		pygame.draw.rect(screen, GREEN, input_rect)




class Grid:
	def __init__(self):
		pass

	def draw (self, screen):
		horiz  =  world_height // tile_size + 1
		vertic =  world_width  // tile_size + 1

		h, v = 0, 0
		offsetx= 0
		offsety= 0
		delta_row = offsety // tile_size
		delta_col = offsetx // tile_size

		test_indent = 9

		i = 0
		for line in range(0, horiz):
			pygame.draw.line(screen,(255, 255, 255),(0 ,line * tile_size),(screen_width, line * tile_size))
			# Write Text (Col,Row) and Screen/World Coordinates
			'''if i > 0:
				text = "(" + str(delta_col) + "," + str(delta_row + i + 1) + ")"
				text = str(delta_row + i + 1) + ")"
				text_surface = my_font_S.render(text, True, WHITE)
				screen.blit(text_surface, (test_indent, tile_size * i + tile_size))
			i = i + 1'''

		i = 0
		for line in range(0, vertic):
			pygame.draw.line(screen,(255, 255, 255),(line * tile_size , tile_size), (line * tile_size, screen_height))
			# Write Text (Col,Row) and Screen/World Coordinates
			'''text = "(" + str(delta_col + i) + "," + str(delta_row + 1) + ")"'''
			'''text = "(" + str(delta_col + i) +  ")"
			text_surface = my_font_S.render(text, True, WHITE)
			screen.blit(text_surface, (tile_size * i + test_indent, tile_size))
			i = i + 1'''





class Animal (pygame.sprite.Sprite):
	def __init__(self,  x, y, angle):
		super().__init__()

		self.size = 1
		self.x = x
		self.y = y
		self.angle = angle
		self.delta_x = math.cos(self.angle)
		self.delta_y = math.sin(self.angle) *-1

		# number of pixel per cycle
		self.speed = 10
		self.move = False

		# states : Hunting, Eating, Reproducing
		self.state = "Hunting"

		self.move_index = 0
		self.step = 40

		self.generation = 1

		self.vision_angle = 120
		self.vision_distance = 100
		self.vision_lock = False

		self.digestion_time  = 5
		self.digestion_step = 0

		self.energy_reserve = 10
		self.energy_per_move  = 0.5
		self.energy_per_cycle = 0.1

		self.reproduction_time= 10
		self.reproduction_step= 0

		self.age = 1
		self.life_expectancy = 70

		img = pygame.transform.scale(tmp_img, (tile_size, tile_size))

		self.image_org = pygame.transform.rotate(img, 0)
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.image_name = path_tmp

		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

	def rotate(self):
		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y


	def update(self):
		# the animal moves in the direction of its angle
		if self.move:
			self.delta_x = math.cos(self.angle * math.pi /180)
			self.delta_y = math.sin(self.angle * math.pi /180) *-1
			self.rect.x = self.rect.x + self.delta_x*self.speed
			self.rect.y = self.rect.y + self.delta_y*self.speed
			self.move_index = self.move_index + 1

			# bouncing
			if self.rect.x <0 :
				# we revert the angle
				self.angle = 180 -self.angle
				self.rect.x = 0

			elif self.rect.x>screen_width-tile_size:
				self.angle = 180 - self.angle
				self.rect.x = screen_width-tile_size

			if self.rect.y <tile_size:
				self.angle = 360- self.angle
				self.rect.y = tile_size

			elif self.rect.y>screen_height-2*tile_size:
				self.angle = 360 - self.angle
				self.rect.y = screen_height-2*tile_size

			# now we can set the proper S coordinates
			self.x = self.rect.x
			self.y = self.rect.y
			self.rotate()

			if self.move_index == self.step:
				self.move_index = 0
				self.move = False

				# now we can set the proper S coordinates
				self.x = self.rect.x
				self.y = self.rect.y


	def draw_vision_line (self,screen):
		# draw vision Line
		radtodeg =math.pi/180
		dist = self.vision_distance
		angle = self.angle

		if draw_vision_line and isinstance(self,Predator):

			x0,y0 = self.rect.centerx,self.rect.centery

			# center line of vision and two lines representing the angular vision cone
			xc,yc = x0+math.cos(angle*radtodeg)*dist,y0-math.sin(angle*radtodeg)*dist
			angle = self.angle + self.vision_angle/2
			xl,yl = x0+math.cos(angle*radtodeg)*dist,y0-math.sin(angle*radtodeg)*dist
			angle = self.angle - self.vision_angle/2
			xr,yr = x0+math.cos(angle*radtodeg)*dist,y0-math.sin(angle*radtodeg)*dist

			linec = ((x0,y0),(xc,yc))
			linel = ((x0,y0),(xl,yl))
			liner = ((x0,y0),(xr,yr))

			color = BLACK
			found = False

			animal_focus = m.find_closest_prey (self)

			if animal_focus is not None:
				# we compute the angle deviation to lock on target.
				color = RED
				xf, yf = animal_focus.rect.centerx, animal_focus.rect.centery
				if (xf-x0)==0 :
					angle = 90
				else:
					angle = math.atan2((y0-yf),(xf-x0))*180/math.pi
					self.angle = int(angle)
					'''print ("lock on angle",self.angle)'''
				self.vision_lock = True
				pygame.draw.line(screen, color, (x0, y0), (xc, yc), 2)
				pygame.draw.line(screen, color, (x0, y0), (xl, yl), 2)
				pygame.draw.line(screen, color, (x0, y0), (xr, yr), 2)
			else:
				color = BLACK
				self.vision_lock = False




			text_surface = my_font_S.render(str(self.energy_reserve), False,BLACK)
			screen.blit(text_surface, (x0, y0-tile_size))



class Predator(Animal):
	def __init__(self , x, y, angle):
		Animal.__init__(self, x, y, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(predator_img, (tile_size, tile_size))
		self.angle = angle
		self.vision_angle = 20
		self.vision_distance = 200
		self.speed = 3
		self.direction_change_angle = 20

		self.energy_reserve_max = 1500
		self.energy_reserve = 1000
		self.energy_reproduction= 1200
		self.energy_reproduction_cost= 400
		self.energy_per_move  = 5
		self.energy_per_cycle = 20

		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.image_name = path_predator
		self.rect = self.image.get_rect()

		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y


	def predator_action (self, game,energy,prey_avail,pop_count):

		# 3 inputs,
		# energy      [0,1] ratio of energy_reserve/energy_max
		energy = self.energy_reserve/self.energy_reserve_max
		# prey avail  [0,1] 1 if a prey can be killed and eaten, else 0
		prey_avail = False
		prey_avail, food = m.capture_food(self)
		# pop_count   [0,1] 0 is pop of predator is null, 1 if pop_predator > pop_prey
		pop_count = game.nb_predator/game.nb_prey
		if game.nb_predator > game.nb_prey:
			pop_count = 1


	def predator_state (self, game):

		# 3 inputs,
		# energy      [0,1] ratio of energy_reserve/energy_max
		energy = self.energy_reserve/self.energy_reserve_max
		# prey avail  [0,1] 1 if a prey can be killed and eaten, else 0
		prey_avail = False
		prey_avail, food = m.capture_food(self)
		# pop_count   [0,1] 0 is pop of predator is null, 1 if pop_predator > pop_prey
		pop_count = game.nb_predator/game.nb_prey
		if game.nb_predator > game.nb_prey:
			pop_count = 1


		# 4 parameters
		# Wait , saves energy towards Resilience
		# Move , requires energy , towards Resilience
		# Eat  , gains energy , towards Reproduction
		# Reproduce ,requires lots of energy , towards Resilience and Population
		# parameters for Energy, Prey, and Ratio
		n_p = [[0.1, 0.5 , 0.8,  0.5],
		       [0.1, 0.7 , 0.8,  0.1],
		       [0.3, 0.1 , 0.1,  0.5]]

		# hidden layer
		wait      = n_p[0][0] * energy      + n_p[1][0] * prey_avail +      n_p[2][0] * pop_count
		move      = n_p[0][1] * energy      + n_p[1][1] * (1-prey_avail) +      n_p[2][1] * pop_count
		eat       = n_p[0][2] * (1-energy)  + n_p[1][2] * prey_avail +      n_p[2][2] * pop_count
		reproduce = n_p[0][3] * energy      + n_p[1][3] * prey_avail +      n_p[2][3] * (1- pop_count)

		action_msg = "Wait"
		action = wait
		if move>action:
			action_msg = "Move"
			action = move
		if eat>action:
			action_msg = "Eat"
			action = eat
		if reproduce>action:
			action_msg = "Reproduce"
			action = reproduce

		return action_msg


class Prey(Animal):
	def __init__(self , x, y, angle):
		Animal.__init__(self, x, y, angle)
		self.size = 1
		self.image_org = pygame.transform.scale(prey_img, (tile_size, tile_size))
		self.angle = angle
		self.vision_angle = 180
		self.vision_distance = 150
		self.speed = 2
		self.direction_change_angle = 35

		self.energy_reserve_max = 1000
		self.energy_reserve = 700
		self.energy_reproduction= 800
		self.energy_reproduction_cost= 400
		self.energy_per_move  = 5
		self.energy_per_cycle = 1

		self.image = pygame.transform.rotate(self.image_org, self.angle)
		self.image_name = path_prey
		self.rect = self.image.get_rect()

		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y



class Plant (pygame.sprite.Sprite):
	def __init__(self , x, y,angle):
		super().__init__()

		self.size = 1
		self.angle = 0
		self.x = x
		self.y = y
		self.move = False
		self.state= "Alive"

		self.energy_reserve_max = 300
		self.energy_reserve = 300
		self.energy_per_cycle = 1

		self.regeneration_time= 25
		self.regeneration_step= 0


		img = pygame.transform.scale(plant_img, (tile_size, tile_size))
		self.image_org = pygame.transform.rotate(img, 0)
		self.image = pygame.transform.rotate(self.image_org, 0)
		self.rect = self.image.get_rect()
		self.image_name = path_plant

		# we intialize the sprite base on camera position
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		if self.energy_reserve  <=0:
			img = pygame.transform.scale(plant_dead_img, (tile_size, tile_size))
			self.image_name = path_plant_dead
		elif self.energy_reserve > 0:
			img = pygame.transform.scale(plant_img, (tile_size, tile_size))
			self.image_name = path_plant

		self.image_org = pygame.transform.rotate(img, 0)
		self.image = pygame.transform.rotate(self.image_org, 0)
		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

