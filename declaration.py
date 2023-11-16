
import pygame
import random

draw_vision_line = True

# This is a list of every sprite. For Animals and Plants
all_sprites_animal_list = pygame.sprite.Group()
all_sprites_plant_list  = pygame.sprite.Group()

# This is a group to handle tmp object
all_sprites_tmp = pygame.sprite.Group()

# two lists to manage all objects
animal_list   = []
plant_list    = []

# simulation inputs
random.seed (2023)
number_max_cycles = 250
number_plants_ini = 250
number_preys_ini  = 150
number_predators_ini = 1
number_prey_limit = 500

# simulation reward
predator_reproduce_reward = 7
predator_eat_reward       = 2
predator_move_reward      = 1

# define game variables
tile_size = 25
screen_width = 1600
screen_height = 800

world_width = 1600
world_height = 800

scroll_step = tile_size

BLACK = (0  ,  0,  0)
WHITE = (255,255,255)

RED   = (255,  0,  0)
GREEN = (0  ,255,  0)
BLUE  = (0  ,0 , 255)

YELLOW  = (255,255,  0)
CYAN    = (0  ,255,255)
MAGENTA = (255,  0,255)

LIGHTSHADE = (170, 170, 170)
DARKSHADE = (100, 100, 100)

RUSTY = (99, 11, 27)
GREY = (126,132,140)

# mouse click index
LEFT = 1
RIGHT = 3

# initialisation of images paths
path_tmp = 'img/tmp.bmp'
tmp_img = pygame.image.load(path_tmp)

path_predator = 'img/predator_obj.png'
predator_img = pygame.image.load(path_predator)
predator_ns_img = pygame.image.load('img/predator_ns.png')

path_prey = 'img/prey_obj.png'
prey_img = pygame.image.load(path_prey)
prey_ns_img = pygame.image.load('img/prey_ns.png')

path_plant_dead = 'img/plant_obj_dead.png'
plant_dead_img = pygame.image.load(path_plant_dead)
path_plant = 'img/plant_obj.png'
plant_img = pygame.image.load(path_plant)
plant_ns_img = pygame.image.load('img/plant_ns.png')

simu_off_img = pygame.image.load('img/simulationOFF.bmp')
simu_on_img = pygame.image.load('img/simulationON.bmp')

delete_img = pygame.image.load('img/delete.bmp')
delete_ns_img = pygame.image.load('img/delete_ns.bmp')

save_img = pygame.image.load('img/save.png')
save_ns_img = pygame.image.load('img/save_ns.png')

open_img = pygame.image.load('img/open.png')
open_ns_img = pygame.image.load('img/open_ns.png')
