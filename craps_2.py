import random
import math
from Tkinter import *
import csv

class Night_of_Gaming:

	def __init__(self):
		self.pBank = 500 #Personal Bank Account going into simulation
		self.pGoal = 100000 #Amount we want to win, based on total in the bank account
		self.bGoal = 100000 #Amount we wish to win in the jackpot round
		self.tLimit = 0 #Amount of time we want to spend at the table
		self.bRule = 0 #How long is the break after a loss?
		self.tMin = 5 #What is the table minimum bet?
		self.tMax = 10000 #What is the table maximum bet?
		self.c_rounds_played = 0 #Counter of how many rounds played
		self.c_rolls_played = 0 #Counter of how many rolls played
		self.c_max_amount = 0 #Counter for seeing the highest amount the player achieves in a night
		self.c_roll_at_max = 0 #What roll were you at when you got ot your max
		self.c_time = 0 #Factor of Randomly generated times to play each round
	
	
	
	def start_night_normal(self):
		self.c_max_amount = self.pBank
		while self.pBank >= self.tMin and self.pGoal > self.pBank:
			if self.pBank < (self.tMin * 4):
				self.pBank = self.pBank - self.tMin
				play = Craps(self.tMin, 0)
			else:
				self.pBank = self.pBank - (self.tMin * 4)
				play = Craps(self.tMin, (self.tMin * 3))
			amount_won, i_rolls_played = play.round_bet()
			self.pBank = self.pBank + amount_won
			self.c_rounds_played = self.c_rounds_played + 1
			self.c_rolls_played = self.c_rolls_played + i_rolls_played
			if self.pBank > self.c_max_amount:
				self.c_max_amount = self.pBank
				self.c_roll_at_max = self.c_rolls_played
		result = {'RoundsPlayed': self.c_rounds_played, 'RollsPlayed': self.c_rolls_played, 'MaxAmount': self.c_max_amount}
		return result
			
	
	def start_night_jackpot(self):
		jackpot = False
		while self.pBank >= self.tMin and jackpot == False:
			self.pBank = self.pBank - self.tMin
			jackpot_hope = self.tMin
			while jackpot_hope > 0 and jackpot == False:
				if jackpot_hope == self.tMin:
					play = Craps(self.tMin, 0)
				else:
					play = Craps((jackpot_hope/2),(jackpot_hope/2))
				amount_won, i_rolls_played = play.round_bet()
				jackpot_hope = amount_won
				extra = jackpot_hope % self.tMin
				if jackpot_hope > self.bGoal:
					jackpot = True
					self.pBank = self.pBank + jackpot_hope
				if extra != 0:
					jackpot_hope = jackpot_hope - extra
					self.pBank = self.pBank + extra
				self.c_rounds_played = self.c_rounds_played + 1
				self.c_rolls_played = self.c_rolls_played + i_rolls_played
		result = {'RoundsPlayed': self.c_rounds_played, 'RollsPlayed': self.c_rolls_played, 'Jackpot': jackpot, 'BankAccount': self.pBank}
		return result		
		

class Craps:

	def __init__(self, bAmount, oAmount):
		self.bAmount = bAmount
		self.oAmount = oAmount
		self.natural = [7, 11]
		self.craps = [2, 3, 12]
	
	def round_bet(self): ##START HERE FOR ROUND
		result, rolls_played = self.come_out()
		round_earnings = int((self.bAmount * result[0]) + math.floor(self.oAmount * result[1]))
		return round_earnings, rolls_played
	
	def roll(self):
		roll_1 = random.randint(1,6)
		roll_2 = random.randint(1,6)
		roll_total = roll_1 + roll_2
		return roll_total
	
	def come_out(self): 
		roll_total = self.roll()
		rolls_played = 0
		if roll_total in self.natural:
			result = [2, 1]
		elif roll_total in self.craps:
			result = [0, 1]
		else:
			result, rolls_played = self.point(roll_total)
		rolls_played = rolls_played + 1
		return result, rolls_played
	
	def point(self, point_goal):
		rolling = True
		rolls_played = 0
		while rolling == True:
			roll_total = self.roll()
			if roll_total == point_goal:
				rolling = False	
				result = [2, self.oMulti(point_goal)]
			elif roll_total == 7:
				rolling = False
				result = [0, 0]
			rolls_played = rolls_played + 1
		return result, rolls_played
				
	def oMulti(self, come_out):
		if come_out in [4, 10]:
			return 3
		elif come_out in [5, 9]:
			return 2.5
		elif come_out in [6, 8]:
			return 2.2

def simulation_1():
	simulations = 1000
	win = 0
	lose = 0	
	rolls_played = []
	total_rolls = 0
	for i in range(0,simulations):
		play1 = Night_of_Gaming()
		result = play1.start_night_jackpot()
		if result['Jackpot'] == True:
			win = win + 1
		else:
			lose = lose + 1
			rolls_played.append(result['RollsPlayed'])
	for i in rolls_played:
		total_rolls = total_rolls + i
	avg_rolls = total_rolls/simulations
	print "YOU WON THE JACKPOT A TOTAL OF " + str(win) + " TIMES."
	print "YOU DIDN'T WIN THE JACKPOT A TOTAL OF " + str(lose) + " TIMES."
	print "YOU PLAYED AN AVERAGE OF " + str(avg_rolls) + " ROLLS WHEN YOU LOST."

def simulation_2():
	simulations = 1000	
	rolls_played = []
	max_amount = []
	for i in range(0,simulations):
		play1 = Night_of_Gaming()
		result = play1.start_night_normal()
		rolls_played.append(result['RollsPlayed'])
		max_amount.append(result['MaxAmount'])
	csvfile = open('C:\Users\Schuster\Documents\Test\craps_results.csv', 'wb')
	csvfile.write('Round, Max Amount, Rolls Played\n')
	round = 1
	for i in range(0, simulations):
		csvfile.write(str(round) + ', ' + str(max_amount[i]) + ', ' + str(rolls_played[i]) + ',\n')
		round = round + 1
	csvfile.close()

	
simulation_2()
		



