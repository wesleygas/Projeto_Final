import pygame
import sys

def mov_aparente(background, vel, x, xl):
	background1 = background
	background_size = background.get_size()
	x -= vel
	xl -= vel

	Display.blit(background,(x,0))
	Display.blit(background1,(xl,0))
	if x + background_size[0]  < 0:
		x = background_size[0]
	if xl +  background_size[0]  < 0:
		xl = background_size[0]
	return x,xl