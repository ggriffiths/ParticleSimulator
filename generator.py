# Author: Grant Griffiths
# Date: 11/12/13
import os
import pygame	
import hostile
import particleSound
import passive
from pygame.locals import *

# creates particles every so often
class Generator:
	totalTicks = 0

	# Creates a new particle generator
	def __init__(self,x,y,ticks,creationTime):
		self.creationTime = creationTime
		self.x = x
		self.y = y
		self.ticksInCycle = ticks

	# Creates a new particle at generator location
	def spawn(self,space):
		p_temp = passive.Passive(self.x,self.y,space)
		space.append(p_temp)

	# Check if correct time to spawn		
	def spawnCheck(self,space):
		if (self.totalTicks-self.creationTime)%self.ticksInCycle==0:
			self.spawn(space)

	# Render the generator
	def render(self,screen):
		pygame.draw.circle(screen,(0,255,0), (self.x,self.y), 5, 0)