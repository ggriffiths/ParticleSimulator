# Author: Grant Griffiths
# Date: 11/13/13
import pygame	
import copy
import particleSound
import random
import particle
from particle import *
from pygame.locals import *

# Enum for different directions
class Dir:
	UP, UR, R, DR, D, DL, L, UL, S = range(9)

class Hostile(particle.Particle):
	# initializes a new particle on mouseclick
	def __init__(self,x,y,space):
		Particle.particle_count+=1
		self.x = x
		self.y = y
		self.size = 6
		self.pid = Particle.particle_count
		self.attackParticle = self
		self.alive = True
		self.speed = 5
		print "New Hostile Particle at (" + str(self.x) + "," + str(self.y) + ")"


	# finds particle's best direction to it's target 
	def bestDirection(self,target):
		bestDir = Dir.UP
		minDist = sys.maxint

		for direction in range(8):
			tempSelf = copy.deepcopy(self)
			tempSelf.move(direction)
			tempDist = Particle.distance(tempSelf,target)
			if minDist > tempDist:
				bestDir = direction
				minDist = tempDist

		return bestDir

	def render(self,screen):
		pygame.draw.circle(screen,(255,0,0), (self.x,self.y), self.size, 0)