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
	def __init__(self,roda,chassi, gear_ratios, rpmmax):
		self.roda = roda
		self.chassi = chassi
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		self.size = chassi.get_size()
		self.counter = 0
		self.x_displacement = 0
		self.rpmap = 1
		self.rpmmax = rpmmax
		self.gear_ratios = gear_ratios

	def speeder(self):
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
			self.rpm -= torque

	def draw(self,display):
		x_displacement = 0
		self.counter += 1
		if self.counter == 1:
			self.previous_speed = self.speed
		if self.counter == 2:
			self.counter = 0
			self.x_displacement = (self.speed-self.previous_speed)*400
			
		if self.x_displacement < 0:
			self.x_displacement = 0
		
		x = 170+self.x_displacement

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


class player2_car:
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
			torque = 25/abs(self.gear)
		
		if espaco and not brake:
			self.rpm += torque
		elif self.rpm > 0:
			self.rpm -= torque

	def draw(self,display):
		x_displacement = 0
		self.counter += 1
		if self.counter == 1:
			self.previous_speed = self.speed
		if self.counter == 2:
			self.counter = 0
			self.x_displacement = (self.speed-self.previous_speed)*400
			
		if self.x_displacement < 0:
			self.x_displacement = 0
		
		x = 170+self.x_displacement
		y = 250

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


	def foward(self,display, vel):
		y = 380
		display.blit(self.roda,(self.x+32,y+84))
		display.blit(self.roda,(self.x+173,y+84))
		display.blit(self.chassi,(self.x,y))
		self.x += vel


class other_car: 
	def __init__(self,roda,chassi,lista_dificuldades): 
		self.roda = roda
		self.chassi = chassi
		self.speed = 0
		self.pos = (170,280)
		self.curvas = lista_dificuldades
		

		#Curva característica é uma lista com os coeficientes da função de velocidade Ex: [0.2,6,-2] -> (0.2)*x^2 + 6*x + (-2)*x
		#A lista de dificuldades é uma lista com curvas características Ex. [[0.2,6,2],[1.2,9,-7],[0.8,0,-1]]
		#O nível é o nível de dificuldade que a curva representa


	def draw(self,display,xi,vel,ticks,lvl):
		x = xi
		y = 250
		tempo = ticks/60
		v_adv = (self.curvas[lvl-1][0] + tempo*self.curvas[lvl-1][1] + (tempo*self.curvas[lvl-1][2])**2 )   #(2 + (6*tempo)+ (0.2*tempo)**2)  #V=V0 + at²/2
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
you_lose = pygame.image.load(r'.\Sprites\you_lose.png')
simples = pygame.image.load(r'.\Sprites\tela_simples.png')
simples = pygame.transform.scale(simples,(1280,720))
rpmv = pygame.image.load(r'.\Sprites\velocimetro_back_red.png')
rpmc = pygame.image.load(r'.\Sprites\velocimetro_background.png')
ponteiro = pygame.image.load(r'.\Sprites\velocimetro_bar.png')

#----Planos de fundo
street = pygame.image.load(r'.\Sprites\Background - EP_Final.png')
desert = pygame.image.load(r'.\Sprites\background_deserto.jpg')
background = street
background_size = background.get_size()
menutosco = pygame.image.load(r'.\Sprites\main_menu.png')
menu_engrenagem = pygame.image.load(r'.\Sprites\menus\menu principal\LogoEvo2.png')
menu = menu_engrenagem
tela_engrenagem = pygame.image.load(r'.\Sprites\menus\store_background_2.png')
plano = tela_engrenagem    

#-----Carros
blue_jeep = pygame.image.load(r'.\Sprites\carro_azul.png')
black_suv = pygame.image.load(r'.\Sprites\jip_preto.png')
carro_vermelho = pygame.image.load(r'.\Sprites\Camaro_vermelho.png')

#-----Musicas

pygame.mixer.music.load(r'top_gear.wav') #Central theme

#-------------------------------------------------------------#

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
acelerando = False
x_bg = 0
x_bg1 = background_size[0]
tela = 0
rola = 0
tier = 0

carroP =  player_car(roda,blue_jeep,[0,0.75,1,1.5,1.9,2.77],4000)
carroP.rpm = 0
carroP.gear = 0

carroadv = other_car(roda,blue_jeep,[[2,6,0.2],[2,9,0],[2,15,1]])
xi = carroadv.pos[0]

dis_total = dis = 38400 #Da linha até a origem 
ticks = 0
posicao = 414 #Da linha ao carro
musica_on = False

while rodando:
	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

	if tela == 0:
		if not musica_on:
			pygame.mixer.music.play(-1)
			musica_on = True
		Display.blit(menu,(0,0))
		play.tela(Display, (489, 500))
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
		pygame.mixer.music.stop()
		musica_on = False
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
			xi,ticks = carroadv.draw(Display,xi,vel,ticks,2)
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
		if not musica_on:
			pygame.mixer.music.play(-1)
			musica_on = True
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