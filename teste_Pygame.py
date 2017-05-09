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
def vel_carro(rpm,marcha):
	gear_ratios = [2.77,1.97,1.53,1,0.75]
	return (rpm*(1/gear_ratios[marcha-1]))/100
#def check_quit():
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			return False

#Importando sprites-------------------------Importando Sprites
roda = pygame.image.load(r'.\Sprites\tire.png')
roda = pygame.transform.scale(roda,(80,80))
background = pygame.image.load('Background - EP_Final.png')
background = pygame.transform.scale(background,(1280,720))
background1 = background
background_size = background.get_size()

rodando = True
x_bg = 0
x_bg1 = background_size[0]


while rodando:
	vel = vel_carro(500,5)
	x_bg -= vel
	x_bg1 -= vel

	Display.blit(background,(x_bg,0))
	Display.blit(background1,(x_bg1,0))
	if x_bg + background_size[0]  < 0:
		x_bg = background_size[0]
	if x_bg1 +  background_size[0]  < 0:
		x_bg1 = background_size[0]

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False
	

	
	mouse = pygame.mouse.get_pos()
	Display.blit(roda,mouse)
	roda = rot_center(roda,-40)
	

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
