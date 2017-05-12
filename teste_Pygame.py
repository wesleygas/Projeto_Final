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
		self.speed = 0

	def speeder(self):
		self.gear_ratios = [0,0.75,1,1.5,1.9,2.77]
		if(self.gear == 0 and self.speed > 0):
			self.speed -= 0.01
		elif(self.speed < 0):
			self.speed = 0
		else:
			self.speed = (self.rpm*self.gear_ratios[self.gear])/100	
		
		return self.speed

	def gas_pedal(self,espaco,brake = False): 
		if (self.rpm < 0):
				self.rpm = 0
		if self.gear == 0: 
			torque = 5
		else:
			torque = 25/abs(self.gear)
		if espaco and not brake:
			self.rpm += torque
		elif self.rpm > 0:
			self.rpm -= torque

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
acelerando = False
x_bg = 0
x_bg1 = background_size[0]

carroP =  player_car(roda,CarroAzul)
carroP.rpm = 0
carroP.gear = 0

while rodando:
	vel = carroP.speeder()
	x_bg, x_bg1 = mov_aparente(Display,background,vel,x_bg,x_bg1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			rodando = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				acelerando = True
			if event.key == pygame.K_UP:
				if(carroP.gear < 5):
					carroP.gear += 1
			if event.key == pygame.K_DOWN:
				if(carroP.gear > 0):
					carroP.gear -= 1
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				acelerando = False

	

	print(carroP.rpm,carroP.gear,vel)
	mouse = pygame.mouse.get_pos()
	carroP.gas_pedal(acelerando)
	carroP.draw(Display)

	

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
