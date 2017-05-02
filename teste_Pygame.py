import pygame

pygame.init()
Display = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Boravê')
clock = pygame.time.Clock()
rodando = True
while rodando:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False
	print(event)

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
