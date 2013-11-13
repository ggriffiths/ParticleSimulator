# Author: Grant Griffiths
# Date: 11/9/13
import os
import pygame	
import re
import math
import sys
import copy
import particleSound
import random
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

soundEnabled = False


# Enum for different directions
class Dir:
	UP, UR, R, DR, D, DL, L, UL, S = range(9)


# removes particle in space through it's PID
def removeById(space,id):
	for p in range(len(space)):
		try:
			if space[p].pid == id:
				space.remove(space[p])
		except IndexError:
			pass

	return space

# checks for collisions in space
def handleCollisions(space):
	for pi in space:
		if pi.attackParticle != pi:
			space = pi.battle(pi.attackParticle,space)

	return space


# PARTICLE CLASS
# --- x ............... position in space     
# --- y ............... y position in space
# --- size ............ how big the particle is (radius)
# --- pid ............. particle ID
# --- attackParticle .. when a collision occurs, a particles will battle. Attack particle keeps track of this
# --- alive ........... if a particle is alive
class Particle:
	# total number of particles
	particle_count = 0


	# Checks if a point is inside a circle
	def particleCollision(self,tar):
		if self.distance(tar) <= self.size + tar.size:
			return True
		else:
			return False

	# finds distance between two particles
	def distance(p1,p2):
		dX = math.fabs(p1.x - p2.x) 
		dY = math.fabs(p1.y - p2.y)
		sq = math.sqrt(dX*dX + dY*dY)
		return sq

	# for string representation of particle
	def __repr__(self):
		return "p" + str(self.pid)
	
	# for string representation of particle
	def __str__(self):
		return "p" + str(self.pid)

	# initializes a new particle on mouseclick
	def __init__(self,x,y,space):
		Particle.particle_count+=1
		self.x = x
		self.y = y
		self.size = 2
		self.pid = Particle.particle_count
		self.attackParticle = self
		self.alive = True
		self.speed = random.randrange(5)+1
		print "New Particle at (" + str(self.x) + "," + str(self.y) + ")"

	# moves a particle in a certain direction
	def move(self,direction):
		# update particle info
		if direction == Dir.UP:
			self.y-=self.speed

		elif direction == Dir.UR:
			self.x+=self.speed
			self.y-=self.speed

		elif direction == Dir.R:
			self.x+=self.speed

		elif direction == Dir.DR:
			self.x+=self.speed
			self.y+=self.speed

		elif direction == Dir.D:
			self.y+=self.speed

		elif direction == Dir.DL:
			self.x-=self.speed
			self.y+=self.speed

		elif direction == Dir.L:
			self.x-=self.speed

		elif direction == Dir.UL:
			self.x-=self.speed
			self.y-=self.speed

		elif direction == Dir.S:
			pass

	# checks if a particle has hit another
	def hit(self,target):
		if self.particleCollision(target):
			return True
		else:
			return False


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

	# find nearest particle to head towards
	def findNearestParticle(self,space):
		currentMinDist = sys.maxint
		

		for p in space:
			tempDist = Particle.distance(self,p)
			if tempDist < currentMinDist:
				currentMinDist = tempDist

				currentMinParticle = p

		if len(space)>0:
			return currentMinParticle
		else:
			pass

	# update particle position in space
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

	# checks if self size is larger than target
	def stronger(self,target):
		if self.size>=target.size:
			return True
		else:
			return False

	# self consumes target size
	def eat(self,target):
		self.size+=target.size

	# two particles fight in space, larger one wins.
	def battle(self,target,space):
		if soundEnabled: sound.beep.play()
		if self.stronger(target):
			self.eat(target)
			space  = removeById(space, target.pid)
			self.attackParticle = self

		else:
			target.eat(self)
			space = removeById(space, self.pid)
			target.attackParticle = target

		return space

