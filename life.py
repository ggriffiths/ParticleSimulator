# Author: Grant Griffiths
# Date: 11/9/13
import os
import Tkinter
import pygame	
import re
import random
import math
import sys
import copy

from pygame.locals import *


# Screen Initialization
screen_height = 600
screen_width = 800
background_color = (0,0,0)
(width, height) = (screen_width,screen_height)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Life Simulator')
screen.fill(background_color)

# params
delayEnabled = True
delayLength = 25


# write this later
def pointInsideRadius(radius,(oX,oY),(pX,pY)):
	dX = math.fabs(oX - pX)
	dY = math.fabs(oY - pY)

	if ((dX*dX) + (dY*dY)) <= radius*radius:
		return True

	else:
		return False


def particleDistance(p1,p2):

		dX = math.fabs(p1.x - p2.x) 
		dY = math.fabs(p1.y - p2.y)
		sq = math.sqrt(dX*dX + dY*dY)
		return sq

class Dir:
	UP, UR, R, DR, D, DL, L, UL, S = range(9)

class Particle:

	def __repr__(self):
		return "p" + str(self.pid)

	def __str__(self):
		return "p" + str(self.pid)

	def __init__(self,newX,newY,space,particle_count):
		self.x = newX
		self.y = newY
		self.size = 2
		self.pid = particle_count
		self.attackParticle = self
		particle_count+=1

		self.alive = True


		print "New Particle at (" + str(self.x) + "," + str(self.y) + ")"

	def move(self,direction):
		# update particle info
		if direction == Dir.UP:
			self.y-=1

		elif direction == Dir.UR:
			self.x+=1
			self.y-=1

		elif direction == Dir.R:
			self.x+=1

		elif direction == Dir.DR:
			self.x+=1
			self.y+=1

		elif direction == Dir.D:
			self.y+=1

		elif direction == Dir.DL:
			self.x-=1
			self.y+=1

		elif direction == Dir.L:
			self.x-=1

		elif direction == Dir.UL:
			self.x-=1
			self.y-=1

		elif direction == Dir.S:
			pass

	def hit(self,target):
		if pointInsideRadius(self.size,(self.x,self.y),(target.x,target.y)):
			return True
		else:
			return False


	def bestDirection(self,target):
		bestDir = Dir.UP
		minDist = sys.maxint

		for direction in range(8):
			tempSelf = copy.deepcopy(self)
			tempSelf.move(direction)
			tempDist = particleDistance(tempSelf,target)
			if minDist > tempDist:
				bestDir = direction
				minDist = tempDist

		return bestDir 


	def findNearestParticle(self,space):
		currentMinDist = sys.maxint
		

		for p in space:
			tempDist = particleDistance(self,p)
			if tempDist < currentMinDist:
				currentMinDist = tempDist

				currentMinParticle = p

		if len(space)>0:
			return currentMinParticle
		else:
			pass


	def step(self,space):
		# remove self from space for search purposes
		spaceTemp = copy.deepcopy(space)	
		selfId = self.pid
		for p in spaceTemp:
			if p.pid == selfId:
				spaceTemp.remove(p)

		# find which particle to go to
		target = self.findNearestParticle(spaceTemp)

		# find the best direction
		direction = self.bestDirection(target)

		# check collision
		if self.hit(target):
			self.attackParticle = target
			target.attackParticle = self

		# update particle info
		self.move(direction)

	def stronger(self,target):
		if self.size>=target.size:
			return True
		else:
			return False

	def eat(self,target):
		self.size+=target.size

	def battle(self,target,space):
		if self.stronger(target):
			self.eat(target)
			space  = removeById(space, target.pid)
			self.attackParticle = self

		else:
			target.eat(self)
			space = removeById(space, self.pid)
			target.attackParticle = target

		return space


def removeById(space,id):
	for p in range(len(space)):
		try:
			if space[p].pid == id:
				space.remove(space[p])
		except IndexError:
			print p
	return space


def handleCollisions(space):
	for pi in space:
		if pi.attackParticle != pi:
			space = pi.battle(pi.attackParticle,space)

	return space


def main():
	running = True
	particle_count = 0
	space = []

	# run until exit 
	while running:			
			for p in space:
				if(len(space)>1):
					p.step(space)
					space = handleCollisions(space)

				pygame.draw.circle(screen,(255,255,255), (p.x,p.y), p.size, 0)

		 	for event in pygame.event.get():
		 		if event.type == pygame.QUIT:
		 			running=False
		 		if event.type == pygame.MOUSEBUTTONUP:
		 			# Create particle at mouse position
		 			pos = pygame.mouse.get_pos()
		 			p_temp = Particle(pos[0],pos[1],space,particle_count)
		 			particle_count+=1
		 			
		 			# if possible to create particle at position, add to space
		 			if p_temp.alive:
		 				space.append(p_temp)

		 	pygame.display.flip()
		 	screen.fill((0,0,0))

		 	if(delayEnabled): pygame.time.delay(delayLength)

main()




