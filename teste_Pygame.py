import pygame
pygame.init()

#Todo-list:
#	- Implementar uma função(matemática) para mudar o RPM do carro
#de modo em que ele tenha as curvas de aceleração
#	- Transformar as funções em classe

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

def mov_aparente(Display,background, vel, x, xl):
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
#Classes ----------------------------------- Classes

class player_car:
	def __init__(self,roda,chassi):
		self.roda = roda
		self.chassi = chassi
		self.rpm = 0
		self.gear = 0
	def speeder(self):
		self.gear_ratios = [2.77,1.97,1.53,1,0.75]
		self.speed = (self.rpm*(1/self.gear_ratios[self.gear-1]))/100	
		return self.speed

	def gas_pedal(self,espaco,brake): 
		if espaco and not brake:
			self.rpm += 5
		else:
			self.rpm -= 5

	def draw(self,display,x_displacement = 0):
		x = 170+x_displacement
		y = 380
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))



#pixel 30,84 e 173,84
#carro 170,380
#202,464;344,464



#Importando sprites-------------------------Importando Sprites
roda = pygame.image.load(r'.\Sprites\Roda011.png')

CarroAzul = pygame.image.load(r'.\Sprites\carro_azul.png')
background = pygame.image.load('Background - EP_Final.png')
background = pygame.transform.scale(background,(1280,720))
background_size = background.get_size()


#-------------------------------------------------------------#

rodando = True
x_bg = 0
x_bg1 = background_size[0]

carroP =  player_car(roda,CarroAzul)
carroP.rpm = 2000
carroP.gear = 5

while rodando:
	vel = carroP.speeder()
	x_bg, x_bg1 = mov_aparente(Display,background,vel,x_bg,x_bg1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False
	

	
	mouse = pygame.mouse.get_pos()
	
	carroP.draw(Display)
	Display.blit(roda,mouse)
	#roda = rot_center(roda,-80)
	

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
