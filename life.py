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
import particle

from pygame.locals import *


# Screen Initialization
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


def main():
	running = True
	particle_count = 0
	space = []

	# run until exit 
	while running:			
			for p in space:
				if(len(space)>1):
					p.step(space)
					space = particle.handleCollisions(space)

				pygame.draw.circle(screen,(255,255,255), (p.x,p.y), p.size, 0)

		 	for event in pygame.event.get():
		 		if event.type == pygame.QUIT:
		 			running=False
		 		if event.type == pygame.MOUSEBUTTONUP:
		 			# Create particle at mouse position
		 			pos = pygame.mouse.get_pos()
		 			p_temp = particle.Particle(pos[0],pos[1],space,particle_count)
		 			particle_count+=1
		 			
		 			# if possible to create particle at position, add to space
		 			if p_temp.alive:
		 				space.append(p_temp)

		 	pygame.display.flip()
		 	screen.fill((0,0,0))

		 	if(delayEnabled): pygame.time.delay(delayLength)

main()




