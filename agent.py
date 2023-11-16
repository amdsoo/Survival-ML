
import torch
import numpy as np
from collections import deque
from game import SurvivalGameAI
from model import Linear_QNet, QTrainer
import declaration as d
from declaration import *
import simulation as simu
import classes as c
import method as m
'''import cProfile'''

from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0.001  # randomness
		self.gamma = 0.75  # discount rate
		self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
		self.model = Linear_QNet(4,128,4)
		self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

		# statistics
		self.nb_AI_action            = 0
		self.nb_AI_action_wait       = 0
		self.nb_AI_action_move       = 0
		self.nb_AI_action_eat        = 0
		self.nb_AI_action_reproduce  = 0
		self.nb_random_action        = 0

	def get_state (self, game, predator):

		# 4 inputs,
		# 1/energy for reproduction.
		energy =0
		if predator.energy_reserve >= predator.energy_reproduction:
			energy =1

		# 2/prey avail  [0,1] 1 if a prey can be killed and eaten, else 0
		prey_avail, food = m.capture_food (predator)
		if prey_avail:
			prey =1
		else:
			prey =0

		# 3/ratio of population. the target ratio for prey vs predator is 1/2
		pop_count =0
		'''if game.nb_prey !=0:
			pop_count = 2*game.nb_predator / game.nb_prey
		if pop_count >1 :
			pop_count = 1'''

		# 4/Vision Lock for Move
		move=0
		if predator.vision_lock and predator.state =="Hunting":
			move =1

		state = [energy,prey,pop_count,move]


		return np.array(state, dtype=int)

	def remember(self, state, action, reward, next_state):
		self.memory.append((state, action, reward, next_state))  # popleft if MAX_MEMORY is reached

	def train_long_memory(self):
		if len(self.memory) > BATCH_SIZE:
			mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
		else:
			mini_sample = self.memory

		states, actions, rewards, next_states = zip(*mini_sample)
		self.trainer.train_step(states, actions, rewards, next_states)

	def train_short_memory(self, state, action, reward, next_state):
		self.trainer.train_step(state, action, reward, next_state)

	def get_action(self, state):
		# random action
		# 0/wait 1/Move 2/Eat 3/Reproduce
		self.epsilon = 40 - self.n_games
		final_move = [0,0,0,0]

		if random.randint(0, 200) < self.epsilon:
			move = random.randint(0, 3)
			'''print("Get Action- from random",move)'''

			# this sets the action, in a form of a group of 4 values
			final_move [move] = 1
			# statistics
			self.nb_random_action +=1

		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.model(state0)
			move = torch.argmax(prediction).item()
			final_move[move] = 1

			# statistics
			if move==0:
				self.nb_AI_action_wait += 1
			elif move ==1:
				self.nb_AI_action_move += 1
			elif move==2:
				self.nb_AI_action_eat  += 1
			else:
				self.nb_AI_action_reproduce += 1

			self.nb_AI_action  +=1

		return final_move


def train():
	plot_scores = []
	plot_predator = []
	plot_mean_scores = []
	total_score = 0
	score  = 0
	record = 0
	agent  = Agent()

	filename = "savefolder/statistic"+"-M"+str(predator_move_reward)+"-E"+str(predator_eat_reward)+"-B"+\
	           str(predator_reproduce_reward)+'.txt'
	'''file = open(os.path.join(filepath, filename+suffix), 'wt')'''
	file = open(filename, 'wt')

	msg = 'Simulation Cycles' + "," + str(number_max_cycles) + "," + "\n"
	file.write(msg)
	msg = 'Reward Move:' + "," + str(predator_move_reward) + "," + "\n"
	file.write(msg)
	msg = 'Reward Eat:'  + "," + str(predator_eat_reward)  + "," + "\n"
	file.write(msg)
	msg = 'Reward Birth:' + "," + str(predator_reproduce_reward) + "," + "\n"
	file.write(msg)

	# output to file statistics in column
	msg = "Game," + 'Score,' + 'Total number of actions,'+"% correct prediction move," + "% correct prediction eat," + \
	      "% correct prediction birth," + "Number of Predator,"  + "\n"
	file.write(msg)



	# statistics

	# intialization of a game/world
	game   = SurvivalGameAI()
	game_over = False

	# track of game cycle done =in Game.reset ()

	while True:

		# we must loop over game cycle
		# and we must loop over each predator
		game.world.cycle +=1

		# UI and world refresh, plants and animals move
		# refresh and run the animations / we store the statistic for this game
		game.update_ui ()

		# 1 collect user action
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# 2 every world.interation, we must run the simulation on each predator only (plant get simulated using std method)
		if game.world.iteration_index == game.world.iteration:

			# 1/ we deal with each predator as individuals
			for animal in d.animal_list:

				game.world.iteration_index = 0

				if isinstance(animal,c.Predator):
					# get old state
					state_old = agent.get_state(game, animal)

					# get actions
					final_move = agent.get_action(state_old)

					# perform actions and get rewards
					reward, score_partial = simu.gameupdate_action(game, animal, final_move)
					game.score = game.score +  score_partial

					# get new state
					state_new = agent.get_state(game,animal)

					# train short memory
					agent.train_short_memory(state_old, final_move, reward, state_new)

					# remember
					agent.remember(state_old, final_move, reward, state_new)

			# 2/ we deal with plants and preys, all at once
			simu.gameupdate_refresh(game)

		game.world.iteration_index = game.world.iteration_index + 1

		if game.nb_predator == 0 :
			game_over = True
			reward = -1000
			print ("game ",agent.n_games, "finished because no predators left")
			score = reward

		if game.world.cycle == number_max_cycles:
			game_over = True
			score = game.score

		# refresh and run the animations / we store the statistic for this game
		'''game.update_ui()'''

		if game_over:
			# when the game finished, we record if we progress or digress
			# train long memory, plot result
			agent.n_games += 1
			agent.train_long_memory()

			if score > record:
				record = score
				agent.model.save()

			game_over = False

			print ('-------------------------------------------------------------------------------------------')
			print('Game', agent.n_games, '/Score', score, '/Record:', record)
			print("Number of Predator max",game.nb_predator_max, "/Nb Predator at the end",game.nb_predator)
			print("Number of Prey max", game.nb_prey_max, "/Nb Prey at the end",game.nb_prey)
			if game.prediction_move !=0:
				nb_stat_pred_move = round(game.prediction_move_ok*100/game.prediction_move,2)
			else:
				nb_stat_pred_move =0
			print("number prediction move  ok", nb_stat_pred_move, "%")

			if game.prediction_eat!=0:
				nb_stat_pred_eat = round(game.prediction_eat_ok*100/game.prediction_eat,2)
			else:
				nb_stat_pred_eat = 0
			print("number prediction Eat ok", nb_stat_pred_eat, "%")

			if game.prediction_reproduce !=0:
				nb_stat_pred_birth = round(game.prediction_reproduce_ok*100/game.prediction_reproduce,2)
			else:
				nb_stat_pred_birth = 0
			print("number prediction birth ok", nb_stat_pred_birth, "%")

			total_action = agent.nb_random_action + agent.nb_AI_action
			total_action_ai = agent.nb_AI_action_wait + agent.nb_AI_action_move + agent.nb_AI_action_eat + \
				agent.nb_AI_action_reproduce

			print("total number of actions :", agent.nb_AI_action)
			print("% Action- from AI", round(agent.nb_AI_action * 100 / total_action, 2), " %")
			print("% Action distribution  /Wait ", round(agent.nb_AI_action_wait * 100 / total_action_ai, 2), "%",
			      "Count/", agent.nb_AI_action_wait,
			      " /Move ", round(agent.nb_AI_action_move * 100 / total_action_ai, 2), "%", "Count/",
			      agent.nb_AI_action_move,
			      " /Eat  ", round(agent.nb_AI_action_eat * 100 / total_action_ai, 2), "%", "Count/",
			      agent.nb_AI_action_eat,
			      " /Repro", round(agent.nb_AI_action_reproduce * 100 / total_action_ai, 2), "%", "Count/",
			      agent.nb_AI_action_reproduce, )


			# output to file statistics (excel like)
			msg=        str(agent.n_games) + ','
			msg=  msg + str(score) + ','
			msg=  msg + str(agent.nb_AI_action) + ','
			msg = msg + str(nb_stat_pred_move) + "%" + ','
			msg = msg + str(nb_stat_pred_eat) + "%" + ','
			msg = msg + str(nb_stat_pred_birth) + "%" + ','
			msg = msg + str(game.nb_predator) + ',' + "\n"
			file.write (msg)

			agent.nb_AI_action           = 0
			agent.nb_random_action       = 0
			agent.nb_AI_action_wait      = 0
			agent.nb_AI_action_move      = 0
			agent.nb_AI_action_eat       = 0
			agent.nb_AI_action_reproduce = 0

			# draw plot
			plot_scores.append(score)
			plot_predator.append (game.nb_predator)
			total_score += score
			mean_score = total_score / agent.n_games
			plot_mean_scores.append(mean_score)
			plot(plot_scores, plot_mean_scores,plot_predator)

			game.reset()


if __name__ == '__main__':
	train()
