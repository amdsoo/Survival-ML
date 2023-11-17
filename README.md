# Survival-ML introduction  
this game is the same game as Survival-Manual, but this time the user doesnt play himself, instead the system goes thru machine learning. 
This game is to observe how predators adopts strategy to eat prey.   
There are three objects   
  a/ Plants who grow, die and reborn every X iterations , they hold calories   
  b/ Prey who are not smart, they randomly move and eat plant if they meet them, Prey die if no food, or too old, or eaten by predators  
  c/ Predators : they can see thru a cone of vision, move or not, and eat or not preys. They reproduce if enough energy, and die if no more energy  


# edit declaration.py to change some of the parameters  
simulation inputs  
random.seed (2023)  / comment this if you want full ramdomness   
number_max_cycles = 250  / change to 500 or 1000 to train on longer periods  
number_plants_ini = 250  / starting number of plants randomly located  
number_preys_ini  = 150  / starting number of prey randomly located  
number_predators_ini = 1 / number of predator to start (randomly located unless 1 is used and placed at the center of the grid)   
number_prey_limit = 500  / max number of prey , you can decide to put a very large number  

simulation reward  
predator_reproduce_reward = 7  / the gain if the predator can reproduce. Inversely, if the predator decides to reproduce but not enough energy, the reward is -7  
predator_eat_reward       = 2  / the gain if the predator can eat something. Inversely, if the predator decides to eat, but there is no prey, the reward is -2  
predator_move_reward      = 1  / Moving is reward to 1, but only if the move is towards a locked prey, else it is -1  


in the agent.py, you can also edit some of the torch parameters  
self.n_games = 0   
self.epsilon = 0.001  # randomness  
self.gamma = 0.75  # discount rate  
self.memory = deque(maxlen=MAX_MEMORY)  # popleft() 
self.model = Linear_QNet(4,128,4)  
self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  

# edit classes.py to modfy the animal parameters    
/for predators    
		vision_angle = 20 / degrees   
		vision_distance = 200  / in pixels, the max distance the predator can see  
		speed = 3  /pixel per iteration  
		direction_change_angle = 20 / when making a turn, the predator turns by this amount of degrees  
		energy_reserve_max = 1500  / the max energy stored  
		energy_reserve = 600  / the initial amount at birth  
		energy_reproduction= 1200 / the energy level needed to reproduce  
		energy_reproduction_cost= 400 / the cost of reproduction  
		energy_per_move  = 30  / the cost to move  
		energy_per_cycle = 2  / the cost to breathe  
/for prey  
		vision_angle = 180  / not used  
		vision_distance = 150   / not used  
		speed = 2   /pixel per iteration  
		direction_change_angle = 35  / when making a turn, the predator turns by this amount of degrees   
		energy_reserve_max = 1000 / the max energy stored  
		energy_reserve = 700  / the initial amount at birth  
		energy_reproduction= 800  / the energy level needed to reproduce  
		energy_reproduction_cost= 400  / the cost of reproduction  
		energy_per_move  = 5  / the cost to move  
		energy_per_cycle = 1  / the cost to breathe  
/for plant  
		energy_reserve_max = 300    / the max energy stored    
		energy_reserve = 300   / the initial amount at birth    
		energy_per_cycle = 1   / the cost to breathe  
		regeneration_time= 25  / the time it takes to reborn  
		regeneration_step= 0   / internal variable  

  # run agent to launch the game  
 
