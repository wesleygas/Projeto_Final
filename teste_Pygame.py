import pygame
pygame.init()
#iniciando display-------------------------iniciando display

Display = pygame.display.set_mode((1280,720)) #Tamanho da janela
pygame.display.set_caption('Boravê') #Nome da janela


clock = pygame.time.Clock()
#Funções úteis------------------------------Funções úteis

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image	

#def check_quit():
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			return False

#Importando sprites-------------------------Importando Sprites
roda = pygame.image.load(r'.\Sprites\tire.png')
back = pygame.image.load('Background - EP_Final.png')	
back = pygame.transform.scale(back,(1280,720))
rodando = True


while rodando:

	Display.blit(back,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False
	mouse = pygame.mouse.get_pos()
	Display.blit(roda,mouse)
	roda = rot_center(roda,-1)
	pygame.event.get
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
