# Author: Grant Griffiths
# Date: 11/9/13
import os
import pygame	
import re
import math
import sys
import copy
import particle
import particleSound
import generator
from pygame.locals import *


# Screen Initialization
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
screen_height = 600
screen_width = 800
background_color = (0,0,0)
(width, height) = (screen_width,screen_height)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Particle Simulator')
screen.fill(background_color)


# params
delayEnabled = True
delayLength = 50
soundEnabled= False



# main method
def main():
	running = True
	space = []
	generators = []
	cycles = 0

	# run until exit 
	while running:

		# 1 particle does not move by itself 
		for p in space:
			if(len(space)>1):
				p.step(space)
			space = particle.handleCollisions(space)
			pygame.draw.circle(screen,(255,255,255), (p.x,p.y), p.size, 0)

	 	for event in pygame.event.get():
	 		if event.type == pygame.QUIT:
	 			running=False
	 		if event.type == pygame.MOUSEBUTTONUP:
	 			if event.button == 1:
		 			# Create particle at mouse position
		 			pos = pygame.mouse.get_pos()
		 			p_temp = particle.Particle(pos[0],pos[1],space)
		 			if soundEnabled: particleSound.ding.play() # play the jump sound effect once

		 			# if possible to create particle at position, add to space
		 			if p_temp.alive:
		 				space.append(p_temp)
		 		else:
		 			pos = pygame.mouse.get_pos()
		 			gen = generator.Generator(pos[0],pos[1],50)
		 			generators.append(gen)



	 	pygame.display.flip()
	 	screen.fill((0,0,0))

	 	if(delayEnabled):
	 		pygame.time.delay(delayLength)
	 		cycles+=1
	 		generator.Generator.totalTicks+=1

 		for gen in generators:
 			gen.spawnCheck(space)
 			gen.show(screen)


main()




