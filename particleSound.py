import os
import Tkinter
import pygame	
import re
import random
import math
import sys
import copy

from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

ding = pygame.mixer.Sound(os.path.join('data','ding.wav'))  
beep = pygame.mixer.Sound(os.path.join('data','beep.wav')) 

ding.set_volume(0.25)
beep.set_volume(0.25)