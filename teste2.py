import pygame
from classe_b import *
pygame.init()

#Todo-list:
#   - Implementar uma função(matemática) para mudar o RPM do carro
#de modo em que ele tenha as curvas de aceleração
#   - Transformar as funções em classe

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
    
class player_car:
    def __init__(self,roda,chassi):
        self.roda = roda
        self.chassi = chassi
        self.rpm = 0
        self.gear = 0
    def speeder(self,brake):
        self.gear_ratios = [2.77,1.97,1.53,1,0.75]
        self.speed = (self.rpm*(1/self.gear_ratios[self.gear-1]))/100   
        return self.speed

    def gas_pedal(self,espaco,brake): 
        if espaco and not brake:
            self.rpm += 5
        else:
            self.rpm -= 5





#Importando sprites-------------------------Importando Sprites
roda = pygame.image.load(r'.\Sprites\Tire.png')
roda = pygame.transform.scale(roda,(80,80))
CarroAzul = pygame.image.load(r'.\Sprites\carro_azul.png')
background = pygame.image.load('Background - EP_Final.png')
background = pygame.transform.scale(background,(1280,720))
background1 = background
background_size = background.get_size()
menu = pygame.image.load('ioio.png')
menu = pygame.transform.scale(menu,(1280,720))
#-------------------------------------------------------------#

rodando = True
x_bg = 0
x_bg1 = background_size[0]

carroP =  player_car(roda,CarroAzul)
carroP.rpm = 500
carroP.gear = 3
janela = 0

while rodando:
	mousepos = pygame.mouse.get_pos()
	mousepres = pygame.mouse.get_pressed()

	if janela == 0:

		Display.blit(menu,(0,0))
		play = botao_comum(Display, (350,300), '.\Sprites\play.png')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False

			if play.precionadoE(mousepos, mousepres):
				janela = 1

	if janela == 1:

		vel = carroP.speeder(False)
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
		Display.blit(roda,mousepos)
		roda = rot_center(roda,-40)
    

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()