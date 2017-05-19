import pygame
import math
pygame.init()

#Todo-list:
#	- Implementar uma função(matemática) para mudar o RPM do carro
#de modo em que ele tenha as curvas de aceleração
#	- Transformar as funções em classe
#Cores------------------------------------------Cores
preto = (0,0,0)
branco = (255,255,255)
azul = (0,255,0)
vermelho = (255,0,0)
verde = (0,0,255)
amarelo = (255,0,255)

#iniciando display-------------------------iniciando display
display_width = 1280
display_heigh = 720
Display = pygame.display.set_mode((display_width,display_heigh)) #Tamanho da janela
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
		if (self.rpm > 4000):
			self.rpm = 4000
		if (self.rpm < 0):
			self.rpm = 0
		
		if self.gear == 0: 
			torque = 5
			self.rpm -= 5
		else:
			torque = 25/abs(self.gear)
		
		if espaco and not brake:
			self.rpm += torque
		elif self.rpm > 0:
			self.rpm -= torque

	def draw(self,display,x_displacement = 0):
		x = 170+x_displacement
		y = 380

		if(self.speed > 0):
			self.roda = rot_center(self.roda, -30)
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))
		Display.blit(velocimetro, (0, 0))
		TextoT(display,'marcha', (30,18), branco, 20)
		TextoT(display,self.gear, (40,35), branco, 60)
		TextoT(display,'velocidade', (123,18), branco, 20)
		TextoT(display,int(self.speed), (130,35), branco, 60)
		return x + self.size[0]
	def restart(self):
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		return 0

class other_car: 
	def __init__(self,roda,chassi, curva_caracteristica= 0):
		self.roda = roda
		self.chassi = chassi
		self.speed = 0
		self.pos = (170,280)
		self.curve = curva_caracteristica
	
	def draw(self,display,xi,vel,ticks):
		x = xi
		y = 280
		tempo = ticks/60
		v_adv = (2 + (10*tempo)+ (1*tempo)**2 - (0.3*tempo)**3) #V=V0 + at²/2
		self.speed = v_adv
		ticks+=1
		x += (v_adv - vel)
		if (x > 0 and x < (display_width-180)):
			if(self.speed > 0):
				self.roda = rot_center(self.roda, -30)
			display.blit(self.chassi,(x,y))
			display.blit(self.roda,(x+32,y+84))
			display.blit(self.roda,(x+173,y+84))
		return x,ticks



class botao_comum:
	
	def __init__(self, imag):
		self.ima = pygame.image.load(imag)
		self.dimen = self.ima.get_size()    

	def tela(self, janela, pos):
		janela.blit(self.ima, (pos[0], pos[1]))
		self.ix = pos[0]
		self.fx = pos[0] + self.dimen[0]
		self.iy = pos[1]
		self.fy = pos[1] + self.dimen[1]

	def pressionadoE(self, mpos, mpres):
		if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy and mpres[0] == 1:
			return True
		else:
			return False    
	
	def pressionadoR(self, mpos, mpres):
		if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy and mpres[0] == 2:
			return True
		else:
			return False  

	def pressionadoD(self, mpos, mpres):
		if self.ix < mpos[0] < self.fx and self.iy < mpres[1] < self.fy and mpres[0] == 3:
			return True
		else:
			return False  

	def em_cima(self, mpos):
		if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy:
			return True
		else:
			return False  

#Importando sprites-------------------------Importando Sprites

roda = pygame.image.load(r'.\Sprites\Roda011.png')
CarroAzul = pygame.image.load(r'.\Sprites\carro_azul.png')
background = pygame.image.load('Background - EP_Final.png')
background = pygame.transform.scale(background,(1280,720))
background_size = background.get_size()
velocimetro = pygame.image.load(r'.\Sprites\velocimetro.png')
chegada = pygame.image.load(r'.\Sprites\chegada.png')
menu = pygame.image.load(r'.\Sprites\main_menu.png')

#-------------------------------------------------------------#
rodando = True
acelerando = False
x_bg = 0
x_bg1 = background_size[0]
tela = 0

play = botao_comum(r'.\Sprites\playgame_button.png')
exit = botao_comum(r'.\Sprites\quit_button.png')

carroP =  player_car(roda,CarroAzul)
carroP.rpm = 0
carroP.gear = 0

carroadv = other_car(roda,CarroAzul)
xi = carroadv.pos[0]

dis_total = dis = 38400 #Da linha até a origem 
ticks = 0
posicao = 414 #Da linha ao carro


while rodando:
	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

	if tela == 0:
		Display.blit(menu,(0,0))
		play.tela(Display, (489, 450))
		exit.tela(Display, (1100, 650))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False
			if play.pressionadoE(mouse, mouse1):
				tela = 1
			if exit.pressionadoE(mouse,mouse1):
				rodando = False

	if tela == 1:

		vel = carroP.speeder()
		x_bg, x_bg1, dis = mov_aparente(Display,background,vel,x_bg,x_bg1,chegada, dis)

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
		xi,ticks = carroadv.draw(Display,xi,vel,ticks)
		posicao = carroP.draw(Display)
		

		if dis < posicao:
			tela = 0 #Quando a tela mudar para o menu, fazer o seguinte:
			xi = carroadv.pos[0]
			carroP.restart()
			ticks = 0
			x_bg = 0
			x_bg1 = background_size[0]
			dis = 38400
			posicao = 414

			if posicao < xi:
				Display.blit

		
	
	

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()