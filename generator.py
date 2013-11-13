# Author: Grant Griffiths
# Date: 11/12/13
import os
import pygame	
import re
import math
import sys
import copy
import particle
import particleSound
from pygame.locals import *

# creates particles every so often
class Generator:
	totalTicks = 0

	def __init__(self,x,y,ticks,creationTime):
		self.creationTime = creationTime
		self.x = x
		self.y = y
		self.ticksInCycle = ticks

	def spawn(self,space):
		p_temp = particle.Particle(self.x,self.y,space)
		space.append(p_temp)

	def spawnCheck(self,space):
		if (self.totalTicks-self.creationTime)%self.ticksInCycle==0:
			self.spawn(space)

	def show(self,screen):
		pygame.draw.circle(screen,(0,255,0), (self.x,self.y), 3, 0)