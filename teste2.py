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
display_width = 302
display_heigh = 93
Display = pygame.display.set_mode((display_width,display_heigh)) #Tamanho da janela
pygame.display.set_caption('Evoracing') #Nome da janela
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
		self.rpmap = 1
		self.rpmmax = 4000

	def speeder(self):
		self.gear_ratios = [0,0.75,1,1.5,1.9,2.77]
		if(self.gear == 0 and self.speed > 0):
			self.speed -= 0.1
		elif(self.speed < 0):
			self.speed = 0
		else:
			self.speed = (self.rpm*self.gear_ratios[self.gear])/100	
		
		return self.speed

	def gas_pedal(self,espaco,brake = False): 

		if (self.rpm > self.rpmmax):
			self.rpm = self.rpmmax
		if (self.rpm < 0):
			self.rpm = 0
		
		if self.gear == 0: 
			self.torque = 100
			self.rpm -= 5
		#else:
		#	self.torque = 25/abs(self.gear)
		
		if espaco and not brake:
			self.rpm += self.torque
		elif self.rpm > 0:
			self.rpm -= self.torque

		self.rpmp = (206/self.rpmmax)*self.rpm + 117

	def gear_up(self):
		if(self.gear < 5):
			rpm_ideal = 3500
			diferenca = abs(self.rpm - rpm_ideal)
		
			if not(self.gear == 0):
				if(self.rpm > rpm_ideal):
					self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação
					self.torque = 50 *((1/((diferenca/100)+0.3))+0.7)/(self.gear*2)
				else:	
					self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação
					self.torque = 30 *((1/((diferenca/100)+0.3))+0.7)/(self.gear*2)
			else:
				self.rpm = 0

			self.gear += 1

	def gear_down(self):
		if(self.gear > 0):
			self.torque = 75/abs(self.gear)
			if self.gear > 1:
				self.rpm = (self.speed/self.gear_ratios[self.gear-1])*100
			self.gear -= 1
		print(self.torque)

	def draw(self,display,x_displacement = 0):
		self.x = 170+x_displacement
		y = 380

		if(self.speed > 0):
			self.roda = rot_center(self.roda, -30)
		display.blit(self.chassi,(self.x,y))
		display.blit(self.roda,(self.x+32,y+84))
		display.blit(self.roda,(self.x+173,y+84))
		display.blit(rpmv, (120,47))
		display.blit(rpmc, (226,47))
		display.blit(velocimetro, (0, 0))
		display.blit(ponteiro, (self.rpmp,46))		
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
		v_adv = (2 + (6*tempo)+ (0.2*tempo)**2)  #V=V0 + at²/2
		self.speed = v_adv
		ticks+=1
		
		x += (v_adv - vel)
		
		if (x > -100 and x < (display_width-180)):
			if(self.speed > 0):
				self.roda = rot_center(self.roda,-30)
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
	
	def __init__(self, imag, shadow):
		self.ima = pygame.image.load(imag)
		self.dimen = self.ima.get_size()    
		self.shadow = pygame.image.load(shadow)

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

	def sombra(self,display):
		display.blit(self.shadow, (self.ix,self.iy))

#Importando sprites-------------------------Importando Sprites

roda = pygame.image.load(r'.\Sprites\Roda011.png')

velocimetro = pygame.image.load(r'.\Sprites\velocimetro.png')
chegada = pygame.image.load(r'.\Sprites\chegada.png')
menu = pygame.image.load(r'.\Sprites\main_menu.png')
you_lose = pygame.image.load(r'.\Sprites\you_lose_2.png')
simples = pygame.image.load(r'.\Sprites\tela_simples.png')
simples = pygame.transform.scale(simples,(1280,720))
rpmv = pygame.image.load(r'.\Sprites\velocimetro_back_red.png')
rpmc = pygame.image.load(r'.\Sprites\velocimetro_background.png')
ponteiro = pygame.image.load(r'.\Sprites\velocimetro_bar.png')

#Ganhar ou perder
you_lose = pygame.image.load(r'.\Sprites\you_lose_2.png')
you_win = pygame.image.load(r'.\Sprites\you_win_2.png')

#Planos de fundo
street = pygame.image.load(r'.\Sprites\Background - EP_Final.png')
desert = pygame.image.load(r'.\Sprites\background_deserto.jpg')
background = street
background_size = background.get_size()
menutosco = pygame.image.load(r'.\Sprites\main_menu.png')
menu_engrenagem = pygame.image.load(r'.\Sprites\menus\menu principal\LogoEvo2.png')
menu = menutosco
tela_engrenagem = pygame.image.load(r'.\Sprites\menus\store_background_2.png')
plano = tela_engrenagem    

#Carros
blue_jeep = pygame.image.load(r'.\Sprites\carro_azul.png')
black_suv = pygame.image.load(r'.\Sprites\jip_preto.png')
blue_rally_jeep = pygame.image.load(r'.\Sprites\blue_rally_jeep.png')
carro_vermelho = pygame.image.load(r'.\Sprites\Camaro_vermelho.png')


fundo = pygame.image.load(r'.\Sprites\botões\fundo_botão.png')

#-------------------------------------------------------------#

avanco = botao_comum(r'.\Sprites\botões\botão_incial.png',r'.\Sprites\botões\botão_incial.png')
up = botao_comum(r'.\Sprites\botões\botão_incial.png',r'.\Sprites\botões\botão_incial.png')

#Menu
play = botao_comum(r'.\Sprites\botões\set_azul\play_button.png',r'.\Sprites\botões\set_azul\play_button_blue_shadow.png')
opçoes = botao_comum(r'.\Sprites\botões\set_azul\settigns_button.png',r'.\Sprites\botões\set_azul\settings_button_shadow.png')
upgrade = botao_comum(r'.\Sprites\botões\set_azul\upgrade_button.png',r'.\Sprites\botões\set_azul\upgrade_button_shadow.png')
voltar = botao_comum(r'.\Sprites\botões\set_azul\back_button.png',r'.\Sprites\botões\set_azul\back_button.png')

#Tier 1
tier_1 = botao_comum(r'.\Sprites\botões\set_azul\tier_1.png',r'.\Sprites\botões\set_azul\tier_1.png')
blue_jeepb = botao_comum(r'.\Sprites\botões\set_azul\blue_jeep.png',r'.\Sprites\botões\set_azul\blue_jeep.png')
black_suvb = botao_comum(r'.\Sprites\botões\set_azul\black_suv.png',r'.\Sprites\botões\set_azul\black_suv.png')
streetb = botao_comum(r'.\Sprites\botões\set_azul\street.png',r'.\Sprites\botões\set_azul\street.png')
desertb = botao_comum(r'.\Sprites\botões\set_azul\desert.png',r'.\Sprites\botões\set_azul\desert.png')

#Tier 2
tier_2 = botao_comum(r'.\Sprites\botões\set_verde\tier_2.png',r'.\Sprites\botões\set_verde\tier_2.png')

#Tier 3
tier_3 = botao_comum(r'.\Sprites\botões\set_rosa\tier_3.png',r'.\Sprites\botões\set_rosa\tier_3.png')

#-------------------------------------------------------------#


rodando = True
inicio = False
acelerando = False
x_bg = 0
x_bg1 = background_size[0]
tela = 0
rola = 0
tier = 0

carroP =  player_car(roda,blue_rally_jeep)
carroP.rpm = 0
carroP.gear = 0

carroadv = other_car(roda,blue_jeep)
xi = carroadv.pos[0]

coins = 0  
passo = 0
dis_total = dis = 38400 #Da linha até a origem 
ticks = 0
posicao = 414 #Da linha ao carro

while inicio:

	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

	if passo >= 7:
		Display.blit(menu,(0,0))

	avanco.tela(Display, (display_width/2 - 151, display_heigh/2 - 47))
	TextoT(Display, 'click', (106 + avanco.ix, 12 + avanco.iy), preto, 41)

	if coins != 0:
		TextoT(Display, 'coins: {0}'.format(coins), (76 + avanco.ix, 49 + avanco.iy), preto, 41)

	if passo == 0 and coins >= 10:
		Display = pygame.display.set_mode((604,93))
		up.tela(Display,(303,0))
		TextoT(Display, 'Big screen', (61 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '10 coins', (84 + up.ix, 49 + up.iy), preto, 41)
		passo = 1

	elif coins >= 10 and passo == 1:
		up.tela(Display,(303,0))
		TextoT(Display, 'Big screen', (61 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '10 coins', (84 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 20 and passo == 2:
		up.tela(Display,(display_width/2 - 151,590))
		TextoT(Display, 'Progress bar', (36 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '20 coins', (79 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 3:
		up.tela(Display,(display_width/2 - 151,500))
		TextoT(Display, 'Play button', (46 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 4:
		up.tela(Display,(300, 600))
		TextoT(Display, 'Settings button', (10 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 5:
		up.tela(Display,(690, 600))
		TextoT(Display, 'Upgrade button', (15 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 6:
		up.tela(Display, (display_width/2 - 151, 0))
		TextoT(Display, 'Menu screen', (45 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)		

	elif coins >= 25 and passo == 7:
		up.tela(Display, (display_width/2 - 151, display_heigh/2 - 47))
		TextoT(Display, 'Buttons work', (45 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '25 coins', (80 + up.ix, 49 + up.iy), preto, 41)			

	if passo >= 4:
		play.tela(Display, (display_width/2 - 151,500))

	if passo >= 5:
		opçoes.tela(Display, (300, 600))

	if passo >= 6:
		upgrade.tela(Display, (690, 600))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			inicio = False
			rodando = False

		if avanco.pressionadoE(mouse, mouse1):
			coins += 1

		if passo != 0:
			if up.pressionadoE(mouse, mouse1):
				if passo == 1:
					display_width = 1280
					display_heigh = 720
					Display = pygame.display.set_mode((display_width ,display_heigh))
					passo = 2
					coins -= 10

				elif passo == 2:
					Display.blit(fundo, (display_width/2 - 151,590,))
					passo = 3
					coins -= 20

				elif passo == 3:
					Display.blit(fundo, (display_width/2 - 151,500))
					passo = 4
					coins -= 5

				elif passo == 4:
					Display.blit(fundo, (300, 600))
					passo = 5
					coins -= 5

				elif passo == 5:
					Display.blit(fundo, (690, 600))
					passo = 6
					coins -= 5

				elif passo == 6:
					Display.blit(fundo, (display_width/2 - 151, 0))
					passo = 7
					coins -= 5

				elif passo == 7:
					coins -= 25
					inicio = False


	pygame.display.update()
	clock.tick(60)

display_width = 1280
display_heigh = 720
Display = pygame.display.set_mode((display_width ,display_heigh))

while rodando:
	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

	if tela == 0:
		Display.blit(menu,(0,0))
		play.tela(Display, (display_width/2 - 151, 500))
		opçoes.tela(Display, (300, 600))
		upgrade.tela(Display, (690, 600))

		if opçoes.em_cima(mouse):
			opçoes.sombra(Display)

		if upgrade.em_cima(mouse):
			upgrade.sombra(Display)

		if play.em_cima(mouse):
			play.sombra(Display)

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

			if upgrade.pressionadoE(mouse, mouse1):
				tela = 2

	if tela == 1:
		if inicio_corrida != 0:


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					rodando = False

			Display.blit(background, (0,0))
			carroadv.drawStop(Display)
			carroP.drawStop(Display)
			TextoT(Display, contagem, (500, 250), preto, 60)
			rola += 1
			if rola == 30:
				rola = 0
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
						carroP.rpmap = carroP.rpmmax - carroP.rpm
						carroP.rpmapp = carroP.rpm
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

				else:

					xmensagem = 500
					ymensagem = 730
					mensagem = 1

					while mensagem != 0:

						Display.blit(background, (0,0))
						carroP.foward(Display,vel)
						Display.blit(you_win, (xmensagem,ymensagem))
						ymensagem -= 5

						pygame.display.update()
						clock.tick(60)

						if ymensagem < 0:
							mensagem = 0


	if tela == 2:

		Display.blit(plano, (0,0))

		if tier == 0:

			tier_1.tela(Display, (443, 124))
			tier_2.tela(Display, (443, 315))
			tier_3.tela(Display, (443, 506))
			voltar.tela(Display, (950,600))


			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					rodando = False

				if tier_1.pressionadoE(mouse, mouse1):

					tier = 1

				if voltar.pressionadoE(mouse, mouse1):
					tela = 0

		elif tier == 1:

			blue_jeepb.tela(Display, (267,228))
			black_suvb.tela(Display, (267,408))
			streetb.tela(Display, (718,228))
			desertb.tela(Display, (718,408))
			voltar.tela(Display, (950,600))

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					rodando = False

				if blue_jeepb.pressionadoE(mouse, mouse1):
					carroP = player_car(roda,blue_jeep)

				if black_suvb.pressionadoE(mouse, mouse1):
					carroP = player_car(roda,black_suv)

				if streetb.pressionadoE(mouse, mouse1):
					background = street

				if desertb.pressionadoE(mouse, mouse1):
					background = desert

				if voltar.pressionadoE(mouse, mouse1):
					tier = 0



	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()