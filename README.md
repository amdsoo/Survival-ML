# Survival-ML introduction
this game is the same game as Survival-Manual, but this time the user doesnt play himself, instead the system goes thru machine learning. 
This game is to observe how predators adopts strategy to eat prey.   
There are three objects   
  a/ Plants who grow, die and reborn every X iterations , they hold calories   
  b/ Prey who are not smart, they randomly move and eat plant if they meet them, Prey die if no food, or too old, or eaten by predators  
  c/ Predators : they can see thru a cone of vision, move or not, and eat or not preys. They reproduce if enough energy, and die if no more energy  

# edit declaration.py to change some of the parameters
simulation inputs
random.seed (2023)  
number_max_cycles = 250  
number_plants_ini = 250  
number_preys_ini  = 150  
number_predators_ini = 1  
number_prey_limit = 500  

simulation reward  
predator_reproduce_reward = 7  
predator_eat_reward       = 2  
predator_move_reward      = 1  

in the agent.py, you can also edit some of the torch parameters  
self.n_games = 0   
self.epsilon = 0.001  # randomness  
self.gamma = 0.75  # discount rate  
self.memory = deque(maxlen=MAX_MEMORY)  # popleft() 
self.model = Linear_QNet(4,128,4)  
self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  

# edit classes.py to modfy the animal parameters  
/for predators    
		self.vision_angle = 20  
		self.vision_distance = 200  
		self.speed = 3  
		self.direction_change_angle = 20  
		self.energy_reserve_max = 1500  
		self.energy_reserve = 600  
		self.energy_reproduction= 1200  
		self.energy_reproduction_cost= 400  
		self.energy_per_move  = 30  
		self.energy_per_cycle = 2  
/for prey  
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
/for plant  
		self.energy_reserve_max = 300  
		self.energy_reserve = 300  
		self.energy_per_cycle = 1  
		self.regeneration_time= 25  
		self.regeneration_step= 0  

  # run agent to launch the game  
 
