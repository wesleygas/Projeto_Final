import pygame
pygame.init()
from classe_b import botao_comum

#Todo-list:
#   - Implementar uma função(matemática) para mudar o RPM do carro
#de modo em que ele tenha as curvas de aceleração
#   - Transformar as funções em classe

#iniciando display-------------------------iniciando display

Display = pygame.display.set_mode((1280,720)) #Tamanho da janela

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

def mov_aparente(Display,background, vel, x, xl, chegada, dis):
	background1 = background
	background_size = background.get_size()
	x -= vel
	xl -= vel
	dis -= vel

	Display.blit(background,(x,0))
	Display.blit(background1,(xl,0))
	if dis <= background_size[0]:
		Display.blit(chegada,(dis,0))
	if x + background_size[0]  < 0:
		x = background_size[0]
	if xl +  background_size[0]  < 0:
		xl = background_size[0]
	return x,xl,dis

def TextoT(display, linha, Loc, cor, tam):
	fonte = pygame.font.Font("DS-DIGI.ttf",tam)
	texto = fonte.render(str(linha), True, cor)
	display.blit(texto, Loc)

#Classes ----------------.------------------ Classes

class player_car:
	def __init__(self,roda,chassi):
		self.roda = roda
		self.chassi = chassi
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		self.size = chassi.get_size()

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

	def draw(self,display, velocimetro, x_displacement = 0):
		x = 170+x_displacement
		y = 380

		preto = (255,255,255)
		self.roda = rot_center(self.roda, -30)
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))
		Display.blit(velocimetro, (0, 0))
		TextoT(display,'marcha', (30,18), preto, 20)
		TextoT(display,self.gear, (40,35), preto, 60)
		TextoT(display,'velocidade', (123,18), preto, 20)
		TextoT(display,int(self.speed), (130,35), preto, 60)
		return x + self.size[0]

#Importando sprites-------------------------Importando Sprites

roda = pygame.image.load(r'.\Sprites\Roda011.png')
CarroAzul = pygame.image.load(r'.\Sprites\carro_azul.png')
background = pygame.image.load('Background - EP_Final.png')
background = pygame.transform.scale(background,(1280,720))
background_size = background.get_size()
velocimetro = pygame.image.load(r'.\Sprites\velocimetro.png')
pv= pygame.image.load(r'.\Sprites\pv.png')
pv = pygame.transform.scale(pv,(73,25))
chegada = pygame.image.load(r'.\Sprites\chegada.png')
menu = pygame.image.load('menu.png')
menu = pygame.transform.scale(menu,(1280,720))
#-------------------------------------------------------------#
inicio = False
rodando = True
acelerando = False
x_bg = 0
x_bg1 = background_size[0]


carroP =  player_car(roda,CarroAzul)
carroP.rpm = 0
carroP.gear = 0
dis = 38400
posicao = 40000
janela = 0
preto = (0,0,0)
play = botao_comum(r'.\Sprites\play.png')
tutorial = 0
#Procedimentos------------------------------------Procedimentos

while inicio:

	if tutorial == 0:
		usu = input('''Desculpe mas você perdeu a corrida!!!

Como eu sei disso? É obvio, por que você não tem o que é preciso pra correr

But don't worry, eu vou te ajudar, primeiro você precisa cavar algumas moedas

É a vida é dura, faz parte, agora digite "cavar"''')
		if usu == 'cavar':
			usu = input('''Boa filhão, escavar te rende moedas, infelizmente apenas uma por vez

pra uma ajuda inicial eu preciso que você escave no minimo 10 moedas!

Continue a escavar, nos falamos de novo quando você conseguir as 10! 
''')



pygame.display.set_caption('Boravê')

while rodando:

	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

	if janela == 0:
		Display.blit(menu,(0,0))
		play.tela(Display, (460, 340))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False
			if play.pressionadoE(mouse, mouse1):
				janela = 1

	if janela == 1:
		vel = carroP.speeder()
		x_bg, x_bg1,dis = mov_aparente(Display,background,vel,x_bg,x_bg1,chegada, dis)

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

		carroP.gas_pedal(acelerando)
		posicao = carroP.draw(Display, velocimetro)
		
		if dis < posicao:
			janela = 0

	print(mouse)
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()