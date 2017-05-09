# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:57:52 2017

@author: jhona
"""

import pygame
import sys
import pygame.sprite as sprite


background = pygame.image.load('uu.jpg')
background1 = pygame.image.load('uu.jpg')
background_size = background.get_size()
background_rect = background.get_rect()

screen = pygame.display.set_mode(background_size)
w,h = background_size
x = 0
y = 0
x1 = -w
y1 = 0

    x1 += 1
    x += 1
    screen.blit(background,(x,y))
    screen.blit(background1,(x1,y1))
    if x> w:
        x = -w
    if x1 > w:
        x1 = -w