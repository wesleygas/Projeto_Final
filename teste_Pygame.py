import pygame
import math
import time
import json
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
		self.counter = 0
		self.x_displacement = 0

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
			torque = 25/2**(self.gear/1.5)
		
		if espaco and not brake:
			self.rpm += torque
		elif self.rpm > 0:
			self.rpm -= torque
	def gear_up(self):
		if(self.gear < 5):
			if not(self.gear == 0):
<<<<<<< HEAD
				self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação 
=======
				self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação
			else:
				self.rpm = 0 
>>>>>>> origin/master
			self.gear += 1
	def gear_down(self):
		if(self.gear > 0):
			if self.gear > 1:
				self.rpm = (self.speed/self.gear_ratios[self.gear-1])*100
<<<<<<< HEAD
		self.gear -= 1
=======
			self.gear -= 1

>>>>>>> origin/master

	def draw(self,display,x_displacement = 0):
		self.x = 170+x_displacement
		y = 380

		if(self.speed > 0):
			self.roda = rot_center(self.roda, -30)
		display.blit(self.chassi,(self.x,y))
		display.blit(self.roda,(self.x+32,y+84))
		display.blit(self.roda,(self.x+173,y+84))
		display.blit(rpmv, (120,47))
		display.blit(rpmc, (150,47))
		display.blit(velocimetro, (0, 0))
		TextoT(display,'marcha', (35,18), branco, 20)
		TextoT(display,self.gear, (45,35), branco, 60)
		TextoT(display,'velocidade', (333,18), branco, 20)
		TextoT(display,int(self.speed), (340,35), branco, 60)
		return self.x + self.size[0]

	def drawStop(self, display):
		x = 170
		y = 380
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))

	def restart(self):
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		return 0

	def foward(self,display, vel):
		y = 380
		display.blit(self.roda,(self.x+32,y+84))
		display.blit(self.roda,(self.x+173,y+84))
		display.blit(self.chassi,(self.x,y))
		self.x += vel

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
		v_adv = (3 + (7*tempo)+ (0.2*tempo)**2 - (0.25*tempo)**3) #V=V0 + at
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

	def drawStop(self,display):
		x = 170
		y = 280
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))

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
you_lose = pygame.image.load(r'.\Sprites\you_lose.png')
simples = pygame.image.load(r'.\Sprites\tela_simples.png')
simples = pygame.transform.scale(simples,(1280,720))
rpmv = pygame.image.load(r'.\Sprites\velocimetro_back_red.png')
rpmc = pygame.image.load(r'.\Sprites\velocimetro_background.png')

#-------------------------------------------------------------#
rodando = True
acelerando = False
x_bg = 0
x_bg1 = background_size[0]
tela = 0

play = botao_comum(r'.\Sprites\playgame_button.png')
exit = botao_comum(r'.\Sprites\quit_button.png')
bot = botao_comum(r'.\Sprites\ot.png')

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
		bot.tela(Display, (489, 600))

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				rodando = False

			if play.pressionadoE(mouse, mouse1):
				tela = 1
				x_bg = 0
				x_bg1 = background_size[0]
				dis = 38400
				posicao = 414
				contagem = 3
				inicio_corrida = 1
				carroP.restart()
				ticks = 0
				xi = carroadv.pos[0]

			if exit.pressionadoE(mouse,mouse1):
				rodando = False

			if bot.pressionadoE(mouse, mouse1):
				tela = 2

	if tela == 1:

		if inicio_corrida != 0:

			Display.blit(background, (0,0))
			carroadv.drawStop(Display)
			carroP.drawStop(Display)
			TextoT(Display, contagem, (500, 250), preto, 60)
			time.sleep(1)
			contagem -= 1
			if contagem < 0:
				inicio_corrida = 0

		else:

			vel = carroP.speeder()
			x_bg, x_bg1, dis = mov_aparente(Display,background,vel,x_bg,x_bg1,chegada,dis)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					rodando = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						acelerando = True
					if event.key == pygame.K_UP:
						carroP.gear_up()
					if event.key == pygame.K_DOWN:
						carroP.gear_down()
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						acelerando = False

			carroP.gas_pedal(acelerando)
			xi,ticks = carroadv.draw(Display,xi,vel,ticks)
			posicao = carroP.draw(Display)
			
			if dis < posicao:

				tela = 0

				if posicao < xi:

					xmensagem = 500
					ymensagem = 730
					mensagem = 1

					while mensagem != 0:

						Display.blit(background, (0,0))
						carroP.foward(Display,vel)
						Display.blit(you_lose, (xmensagem,ymensagem))
						ymensagem -= 5

						pygame.display.update()
						clock.tick(60)

						if ymensagem < 0:
							mensagem = 0

	if tela == 2:

		Display.blit(simples, (0,0))
		bot.tela(Display, (300,300))
		play.tela(Display, (600,300))
		exit.tela(Display, (600,600))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False
			if bot.pressionadoE(mouse, mouse1):
				background = pygame.image.load(r'.\Sprites\background_deserto.jpg')
				background = pygame.transform.scale(background,(1280,720))
			if play.pressionadoE(mouse,mouse1):
				background = pygame.image.load('Background - EP_Final.png')
				background = pygame.transform.scale(background,(1280,720))
			if exit.pressionadoE(mouse,mouse1):
				tela = 0
	
	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()