import pygame
import sys

def mov_aparente(background, vel):
	if vel == 0:
	background1 = background
	background_size = background.get_size()
	x_bg -= vel
	x_bg1 -= vel

	Display.blit(background,(x_bg,0))
	Display.blit(background1,(x_bg1,0))
	if x_bg + background_size[0]  < 0:
		x_bg = background_size[0]
	if x_bg1 +  background_size[0]  < 0:
		x_bg1 = background_size[0]