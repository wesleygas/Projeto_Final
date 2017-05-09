import pygame
import sys

def mov_aparente(back, vel, x,xl):
	backl = back
	back_size = back.get_size()
	x -= vel
	xl -= vel

	Display.blit(back,(x,0))
	Display.blit(backl,(xl,0))
	if x + back_size[0]  < 0:
		x = back_size[0]
	if xl + back_size[0]  < 0:
		xl = back_size[0]
	return x,xl