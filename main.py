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
import hostile
import generator
import passive
from pygame.locals import *


# Screen Initialization
pygame.mixer.pre_init(44100, -16, 2, 2048)
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
delayLength = 25
soundEnabled= False



# main method
def main():
	running = True
	space = []
	generators = []
	cycles = 0
	pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

	# run until exit 
	while running:

		# 1 particle does not move by itself 
		for p in space:
			if(len(space)>1):
				p.step(space)
			p.render(screen)
			space = particle.handleCollisions(space)

	 	for event in pygame.event.get():
	 		if event.type == pygame.QUIT:
	 			running=False
	 		if event.type == pygame.MOUSEBUTTONUP:
	 			if event.button == 1:
		 			# Create particle at mouse position
		 			pos = pygame.mouse.get_pos()
		 			p_temp = hostile.Hostile(pos[0],pos[1],space)
		 			if soundEnabled: particleSound.ding.play() # play the jump sound effect once

		 			# if possible to create particle at position, add to space
		 			if p_temp.alive:
		 				space.append(p_temp)
		 		else:
		 			pos = pygame.mouse.get_pos()
		 			gen = generator.Generator(pos[0],pos[1],50,generator.Generator.totalTicks)
		 			generators.append(gen)

		 	if event.type == pygame.KEYUP:
		 		running=False



	 	pygame.display.flip()
	 	screen.fill((0,0,0))

	 	if(delayEnabled):
	 		pygame.time.delay(delayLength)
	 		cycles+=1
	 		generator.Generator.totalTicks+=1

 		for gen in generators:
 			gen.spawnCheck(space)
 			gen.render(screen)


main()




