import pygame
import math
import json
from random import choice


with open('data.json') as arquivo:	#Abre o save 
	data = json.load(arquivo)

pygame.init()	#Inicia o pygame

#Cores------------------------------------------Cores
preto = (0,0,0)
branco = (255,255,255)
azul = (0,255,0)
vermelho = (255,0,0)
verde = (0,0,255)
amarelo = (255,0,255)

#iniciando display-------------------------iniciando display
display_width = 302	#dimensões do display
display_heigh = 93

Display = pygame.display.set_mode((display_width,display_heigh)) #Criando display
pygame.display.set_caption('Evoracing') #Nome do display
clock = pygame.time.Clock() #Criando contador

#Funções úteis------------------------------Funções úteis

def rot_center(image, angle):	#Função de rotação de imagem
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image	

def mov_aparente(Display,background, vel, x, xl, chegada, dis): #Função de movimento de background
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

def TextoT(display, linha, Loc, cor, tam): #Função de printar texto na tela
	fonte = pygame.font.Font("DS-DIGI.ttf",tam)
	texto = fonte.render(str(linha), True, cor)
	display.blit(texto, Loc)

#Classes ----------------.------------------ Classes

class player_car:	#Classe jogador
	def __init__(self,roda,chassi, car_data):
		self.roda = roda
		self.chassi = chassi
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		self.size = self.chassi.get_size()
		self.counter = 0
		self.x_displacement = 0
		self.rpmap = 1
		self.rpmmax = car_data[1]
		self.gear_ratios = car_data[0]
		self.torque_multiplier = car_data[2]
		self.rpm_ideal_lista = [0, self.rpmmax-1000, self.rpmmax-900, self.rpmmax-800, self.rpmmax-500, self.rpmmax]
		self.rpm_idealvisor = 0

	def speeder(self): #Função velocidade do carro
		if(self.gear == 0 and self.speed > 0):
			self.speed -= 0.1
		elif(self.speed < 0):
			self.speed = 0
		else:
			self.speed = (self.rpm*self.gear_ratios[self.gear])/100	
		
		return self.speed

	def gas_pedal(self,espaco):	#Função aceleração

		if (self.rpm > self.rpmmax):
			self.rpm = self.rpmmax
		if (self.rpm < 0):
			self.rpm = 0
		
		if self.gear == 0: 
			self.torque = 100
			self.rpm -= 5
		
		if espaco:
			self.rpm += self.torque
		elif self.rpm > 0:
			self.rpm -= self.torque

		
		self.rpmp = (206/self.rpmmax)*self.rpm + 117

		if self.gear != 0:
			self.rpm_idealvisor = (206/self.rpmmax)*self.rpm_ideal + 50
		else:
			self.rpm_idealvisor = -500

	def gear_up(self):	#Função aumentar a marcha
		if(self.gear < 5):
			self.rpm_ideal = self.rpm_ideal_lista[self.gear]
			diferenca = abs(self.rpm - self.rpm_ideal)
		
			if not(self.gear == 0):
				if(self.rpm > self.rpm_ideal):
					self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação
					self.torque = 50 *((1/((diferenca/100)+0.3))+0.7)/(self.gear*2)
				else:	
					self.rpm = (self.speed/self.gear_ratios[self.gear+1])*100 #Mantém a relação
					self.torque = 30 *((1/((diferenca/100)+0.3))+0.7)/(self.gear*2)
			else:
				self.rpm = 0

			self.gear += 1
			self.rpm_ideal = self.rpm_ideal_lista[self.gear]
			

	def gear_down(self):	#Fu~ção diminuir a marcha
		if(self.gear > 0):
			self.torque = 75/abs(self.gear)
			if self.gear > 1:
				self.rpm = (self.speed/self.gear_ratios[self.gear-1])*100
			self.gear -= 1
			self.rpm_ideal = self.rpm_ideal_lista[self.gear]

	def draw(self,display,x_displacement = 0):	#Função que blita o carrinho na tela
		self.x = 170+x_displacement
		y = 380

		if(self.speed > 0):
			self.roda = rot_center(self.roda, -30)
		display.blit(self.chassi,(self.x,y))
		display.blit(self.roda,(self.x+32,y+84))
		display.blit(self.roda,(self.x+173,y+84))
		display.blit(rpmv, (120,47))
		display.blit(rpmc, (self.rpm_idealvisor,47))
		display.blit(velocimetro, (0, 0))
		display.blit(ponteiro, (self.rpmp,46))		
		TextoT(display,'marcha', (35,18), branco, 20)
		TextoT(display,self.gear, (45,35), branco, 60)
		TextoT(display,'velocidade', (333,18), branco, 20) 
		TextoT(display,int(self.speed), (340,35), branco, 60)
		return self.x + self.size[0]

	def drawStop(self, display): #Blita o carrinho parado
		x = 170
		y = 380
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))

	def restart(self):	#Zera todos os parametros do carrinho pra proxima corrida
		self.rpm = 0
		self.gear = 0
		self.speed = 0
		return 0

	def foward(self,display, vel):	#Faz com que o carrinho va em frente e saia da tela
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
		self.pos = (170,240)
		self.curvas = lista_dificuldades
		

		#Curva característica é uma lista com os coeficientes da função de velocidade Ex: [0.2,6,-2] -> (0.2)*x^2 + 6*x + (-2)*x
		#A lista de dificuldades é uma lista com curvas características Ex. [[0.2,6,2],[1.2,9,-7],[0.8,0,-1]]
		#O nível é o nível de dificuldade que a curva representa

	def draw(self,display,xi,vel,ticks,lvl):
		x = xi
		y = self.pos[1]
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
		y = self.pos[1]
		display.blit(self.chassi,(x,y))
		display.blit(self.roda,(x+32,y+84))
		display.blit(self.roda,(x+173,y+84))

class botao_comum: #Classe botão
	
	def __init__(self, imag, shadow, bloqueio, cos):
		self.ima = pygame.image.load(imag)
		self.dimen = self.ima.get_size()    
		self.shadow = pygame.image.load(shadow)
		self.block = bloqueio
		self.cos = cos


	def tela(self, display, pos, mpos): #Blita o botão na tela

		display.blit(self.ima, (pos[0], pos[1]))		
		self.ix = pos[0]
		self.fx = pos[0] + self.dimen[0]
		self.iy = pos[1]
		self.fy = pos[1] + self.dimen[1]

		if self.block == 0:
			display.blit(pygame.image.load(r'.\Sprites\botões\lock_mask.png'),(pos[0], pos[1]))
			if self.em_cima(mpos):
				TextoT(Display, 'Coins', (100 + self.ix, 12 + self.iy), azul, 41)
				TextoT(Display, self.cos, (130 + self.ix, 49 + self.iy), azul, 41)

		elif self.em_cima(mpos):
			display.blit(self.shadow, (self.ix,self.iy))

	def pressionadoE(self, mpos, mpres): #Verifica se o botão esta sendo pressionado 

		if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy and mpres[0] == 1:
			return True
		else:
			return False

	def em_cima(self, mpos):	#Verifica se o mouse esta em cima do botão
		if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy:
			return True
		else:
			return False  

#Importando sprites-------------------------Importando Sprites


chegada = pygame.image.load(r'.\Sprites\chegada.png')
evocoins = pygame.image.load(r'.\Sprites\New Piskel (3).png')

#Velocimetro
velocimetro = pygame.image.load(r'.\Sprites\velocimetro.png')
rpmv = pygame.image.load(r'.\Sprites\velocimetro_back_red.png')
rpmc = pygame.image.load(r'.\Sprites\velocimetro_background.png')
ponteiro = pygame.image.load(r'.\Sprites\velocimetro_bar.png')

#Rodas
roda_thunder = pygame.image.load(r'.\Sprites\Roda011.png')
roda_little = pygame.image.load(r'.\Sprites\Roda1800.png')
roda_x = pygame.image.load(r'.\Sprites\Roda_x.png')
roda_bmw = pygame.image.load(r'.\Sprites\Roda_bmw_8bits.png')
roda = roda_thunder

#Ganhar ou perder
you_lose = pygame.image.load(r'.\Sprites\you_lose_2.png')
you_win = pygame.image.load(r'.\Sprites\you_win_2.png')

#Backgrounds
street = pygame.image.load(r'.\Sprites\Background - EP_Final.png')
desert = pygame.image.load(r'.\Sprites\background_deserto.jpg')
nuvens = pygame.image.load(r'.\Sprites\Background - heavens_cove.png')
lunar = pygame.image.load(r'.\Sprites\Background_snow_point.png')
background = street
background_size = background.get_size()

#Menus
menutosco = pygame.image.load(r'.\Sprites\main_menu.png')
menu_engrenagem = pygame.image.load(r'.\Sprites\menus\menu principal\LogoEvo2.png')
menu = menutosco

#Telas
tela_azul = pygame.image.load(r'.\Sprites\menus\tela\tela_simples.png')
tela_engrenagem = pygame.image.load(r'.\Sprites\menus\tela\tela_engrenagem.png')
plano = tela_azul
pause_azul = pygame.image.load(r'.\Sprites\menus\tela\pause_azul.png')
pause_engrenagem = pygame.image.load(r'.\Sprites\menus\tela\pause_engrenagens.png')
pause_imagem = pause_azul

#Carros
blue_jeep_chassi = pygame.image.load(r'.\Sprites\carro_azul.png')
black_suv_chassi = pygame.image.load(r'.\Sprites\jip_preto.png')
blue_rally_jeep_chassi = pygame.image.load(r'.\Sprites\blue_rally_jeep.png')
camaro_vermelho_chassi = pygame.image.load(r'.\Sprites\Camaro_vermelho.png')

#----Objetos Carro player:

blue_rally_jeep = player_car(roda,blue_rally_jeep_chassi,data[2]["carros_player"]["blue_rally_jeep"])
blue_jeep = player_car(roda,blue_jeep_chassi,data[2]["carros_player"]["blue_jeep"])
black_suv = player_car(roda,black_suv_chassi,data[2]["carros_player"]["black_suv"])
camaro_vermelho = player_car(roda,camaro_vermelho_chassi,data[2]["carros_player"]["camaro_vermelho"])



#----Objetos Carro adversário:
blue_jeep_adv = other_car(roda,blue_jeep_chassi,data[2]["carros_adversarios"]["blue_jeep"])
black_suv_adv = other_car(roda,black_suv_chassi,data[2]["carros_adversarios"]["blue_jeep"])
blue_rally_jeep_adv = other_car(roda,blue_rally_jeep_chassi,data[2]["carros_adversarios"]["blue_jeep"])
camaro_vermelho_adv = other_car(roda,camaro_vermelho_chassi,data[2]["carros_adversarios"]["blue_jeep"])

lista_adversarios = [blue_jeep_adv,black_suv_adv,blue_rally_jeep_adv,camaro_vermelho_adv]

#na hora de correr, o jogo escolherá um adversário aleatório dentro dessa lista 
#e escolherá a dificuldade conforme a tier que o jogador está desbloqueando


#-----Musicas

pygame.mixer.music.load(r'.\Sounds\top_gear.mp3') #Central theme

fundo = pygame.image.load(r'.\Sprites\botões\fundo_botão.png')

#-------------------------Botões do menu---------------------------#

avanco = botao_comum(r'.\Sprites\botões\botão_incial.png',r'.\Sprites\botões\botão_incial.png', 1, 0)
up = botao_comum(r'.\Sprites\botões\botão_incial.png',r'.\Sprites\botões\botão_incial.png', 1, 0)

#Menu
play = botao_comum(r'.\Sprites\botões\set_transparente\play_button_gray.png',r'.\Sprites\botões\set_transparente\play_button_gray_shadow.png',0, 0)
upgrade = botao_comum(r'.\Sprites\botões\set_transparente\upgrade_button_gray.png',r'.\Sprites\botões\set_transparente\upgrade_button_gray_shadow.png',0, 0)
voltar = botao_comum(r'.\Sprites\botões\set_transparente\back_button.png',r'.\Sprites\botões\set_transparente\back_button_shadow.png',1, 0)
pauseb = botao_comum(r'.\Sprites\botões\set_transparente\pause_button_gray.png',r'.\Sprites\botões\set_transparente\pause_button_gray_shadow.png',1, 0)
continueb = botao_comum(r'.\Sprites\botões\set_transparente\continue_button.png',r'.\Sprites\botões\set_transparente\continue_button_shadow.png',1, 0)
voloffb = botao_comum(r'.\Sprites\botões\volume-off.png',r'.\Sprites\botões\volume-off.png',1, 0)
voloonb = botao_comum(r'.\Sprites\botões\volume-512.png',r'.\Sprites\botões\volume-512.png',1, 0)
recomecarb = botao_comum(r'.\Sprites\botões\Reset-Button.png',r'.\Sprites\botões\Reset-Button.png',1, 0)

#Tiers
tier_1 = botao_comum(r'.\Sprites\botões\set_azul\tier_1.png',r'.\Sprites\botões\set_azul\tier_1_blue_shadow.png',0, 20)
tier_1b = botao_comum(r'.\Sprites\botões\set_azul\tier_1.png',r'.\Sprites\botões\set_azul\tier_1_blue_shadow.png',0, 20)
tier_2 = botao_comum(r'.\Sprites\botões\set_verde\tier_2.png',r'.\Sprites\botões\set_verde\tier_2.png',0, 40)
tier_2b = botao_comum(r'.\Sprites\botões\set_verde\tier_2.png',r'.\Sprites\botões\set_verde\tier_2.png',0, 50)

#Carros
blue_jeepb = botao_comum(r'.\Sprites\botões\set_azul\blue_jeep.png',r'.\Sprites\botões\set_azul\blue_jeep_shadow.png',0, 10)
blue_rally_jeepb = botao_comum(r'.\Sprites\botões\set_azul\blue_rally_fiesta.png',r'.\Sprites\botões\set_azul\blue_rally_fiesta_shadow.png',1 ,0)
black_suvb = botao_comum(r'.\Sprites\botões\set_verde\black_suv.png',r'.\Sprites\botões\set_verde\black_suv_shadow.png',1, 40)
red_camarob = botao_comum(r'.\Sprites\botões\set_verde\red_camaro.png',r'.\Sprites\botões\set_verde\red_camaro_shadow.png',1, 60)

#Rodas
little_rodab = botao_comum(r'.\Sprites\botões\set_azul\roda_little.png',r'.\Sprites\botões\set_azul\roda_little_shadow.png',1, 0)
roda_thunderb = botao_comum(r'.\Sprites\botões\set_azul\roda_thunder.png',r'.\Sprites\botões\set_azul\roda_thunder_shadow.png',0, 10)
roda_xb = botao_comum(r'.\Sprites\botões\set_verde\x_wheels_button.png',r'.\Sprites\botões\set_verde\x_wheels_button_shadow.png',0, 40)
roda_bmwb = botao_comum(r'.\Sprites\botões\set_verde\bmw_wheels_button.png',r'.\Sprites\botões\set_verde\bmw_wheels_button_shadow.png',0, 60)

#Backgrounds
streetb = botao_comum(r'.\Sprites\botões\set_azul\street.png',r'.\Sprites\botões\set_azul\street_shadow.png',1, 0)
desertb = botao_comum(r'.\Sprites\botões\set_azul\desert.png',r'.\Sprites\botões\set_azul\desert_shadow.png',0, 10)
nuvensb = botao_comum(r'.\Sprites\botões\set_verde\lunar_green.png',r'.\Sprites\botões\set_verde\lunar_green_shadow.png',0, 40)
lunarb = botao_comum(r'.\Sprites\botões\set_verde\clouds.png',r'.\Sprites\botões\set_verde\clouds_shadow.png',0, 60)

#--------------------Parametros iniciais------------------------------#

rodando = True
inicio = bool(data[1]["inicio"])
acelerando = False
x_bg = 0
x_bg1 = background_size[0]
tela = 0
rola = 0

carroP =  blue_rally_jeep
carroP.rpm = 0
carroP.gear = 0


coins = data[0]["coins"]
passo = 0
data[1]["passo"] = 0
dis_total = dis = 38400 #Da linha até a origem 
ticks = 0
posicao = 414 #Da linha ao carro
musica_aux = False #Variável auxiliar para a escolha das músicas
musica_on = bool(data[1]["musica_on"]) #Escolha do player se ele quer música ou não


while inicio: #Loop primeira parte do jogo

	mouse = pygame.mouse.get_pos() #Pega os dados do mouse
	mouse1 = pygame.mouse.get_pressed()

	if passo >= 5: #Blita o menu
		Display.blit(menu,(0,0))

	avanco.tela(Display, (display_width/2 - 151, display_heigh/2 - 47), mouse) #Blita o menu de click
	TextoT(Display, 'click', (106 + avanco.ix, 12 + avanco.iy), preto, 41)

	if coins != 0:	#Blita a quantidade de moedas possuidas
		TextoT(Display, 'coins: {0}'.format(coins), (76 + avanco.ix, 49 + avanco.iy), preto, 41)

#--------------------Sequencia de botões a serem blitados------------------------------#

	if passo == 0 and coins >= 10:
		Display = pygame.display.set_mode((604,93))
		up.tela(Display,(303,0), mouse)
		TextoT(Display, 'Big screen', (61 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '10 coins', (84 + up.ix, 49 + up.iy), preto, 41)
		passo = 1

	elif coins >= 10 and passo == 1:
		up.tela(Display,(303,0), mouse)
		TextoT(Display, 'Big screen', (61 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '10 coins', (84 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 2:
		up.tela(Display,(display_width/2 - 151,500), mouse)
		TextoT(Display, 'Play button', (46 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 3:
		up.tela(Display,(display_width/2 - 151, 600), mouse)
		TextoT(Display, 'Upgrade button', (15 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)

	elif coins >= 5 and passo == 4:
		up.tela(Display, (display_width/2 - 151, 0), mouse)
		TextoT(Display, 'Menu screen', (45 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '5 coins', (89 + up.ix, 49 + up.iy), preto, 41)		

	elif coins >= 25 and passo == 5:
		up.tela(Display, (display_width/2 - 151, display_heigh/2 - 47), mouse)
		TextoT(Display, 'Buttons work', (45 + up.ix, 12 + up.iy), preto, 41)
		TextoT(Display, '25 coins', (80 + up.ix, 49 + up.iy), preto, 41)			

#--------------------Ações a serem realizados pelos botões------------------------------#

	if passo >= 3:
		play.tela(Display, (display_width/2 - 151,500), mouse)

	if passo >= 4:
		upgrade.tela(Display, (display_width/2 - 151, 600), mouse)

#--------------------Interações do jogador------------------------------#

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			inicio = False
			rodando = False

		if avanco.pressionadoE(mouse, mouse1):
			coins += 1

		if passo != 0:
			if up.pressionadoE(mouse, mouse1):
				if passo == 1 and coins >= 10:
					display_width = 1280
					display_heigh = 720
					Display = pygame.display.set_mode((display_width ,display_heigh))
					passo = 2
					coins -= 10

				elif passo == 2 and coins >= 5:
					Display.blit(fundo, (display_width/2 - 151,500))
					passo = 3
					coins -= 5

				elif passo == 3 and coins >= 5:
					Display.blit(fundo, (display_width/2 - 151, 600))
					passo = 4
					coins -= 5

				elif passo == 4 and coins >= 5:
					Display.blit(fundo, (display_width/2 - 151, 0))
					passo = 5
					coins -= 5

				elif passo == 5 and coins >= 25:
					coins -= 25
					inicio = False


	pygame.display.update()
	clock.tick(60)




if(rodando):	#Quando o jogo é iniciado por um save carrega a tela maior
	display_width = 1280
	display_heigh = 720
	Display = pygame.display.set_mode((display_width ,display_heigh))
	play.block = 1
	upgrade.block = 1


while rodando: #Jogo principal
	mouse = pygame.mouse.get_pos()
	mouse1 = pygame.mouse.get_pressed()

#--------------------Menu------------------------------#

	if tela == 0:
		if not musica_aux:
			if(musica_on):
				pygame.mixer.music.load(r'.\Sounds\top_gear.mp3')
				pygame.mixer.music.play(-1)

			musica_aux = True
		Display.blit(menu,(0,0))
		play.tela(Display, (display_width/2 - 151, 500), mouse)
		upgrade.tela(Display, (display_width/2 - 151, 600), mouse)
		Display.blit(evocoins, (1129,7))
		TextoT(Display, coins, (1030, 11), branco, 41)
		recomecarb.tela(Display, (131,0), mouse)

#--------------------Interações com o jogador------------------------------#

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				rodando = False

			if play.pressionadoE(mouse, mouse1):
				carroadv = choice(lista_adversarios) #Escolhe um adversário randômico
				xi = carroadv.pos[0]
				tela = 1
				x_bg = 0
				x_bg1 = background_size[0]
				dis = 38400
				posicao = 414
				contagem = 3
				inicio_corrida = 1
				carroP.restart()
				ticks = 0

			if recomecarb.pressionadoE(mouse, mouse1):
				with open('data_Copia.json') as arquivo: #Abre o save 
					data = json.load(arquivo)

				with open('data.json','w') as arquivo: #Guarda o save
					json.dump(data,arquivo)

				pygame.quit()
				quit()
				
			if upgrade.pressionadoE(mouse, mouse1):
				tela = 2
				tier = 0

#--------------------Corrida contagem regressiva---------------------------#

	if tela == 1:
		
		if inicio_corrida != 0:
			if musica_aux:	
				pygame.mixer.music.stop()
				if musica_on:
					pygame.mixer.music.load(r'.\Sounds\race.ogg')
					pygame.mixer.music.play(-1)

				musica_aux = False

			Display.blit(background, (0,0))
			carroadv.drawStop(Display)
			carroP.drawStop(Display)
			TextoT(Display, contagem, (500, 250), verde, 60)
			pauseb.tela(Display, (1085, 12), mouse)
			TextoT(Display, "Espaco acelera", (550, 250), preto, 70)
			TextoT(Display, "Setas: cima e baixo", (450, 350), preto, 70)
			TextoT(Display, "para mudar a marcha", (450, 450), preto, 70)

#--------------------Interações com o jogador------------------------------#

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					rodando = False

				if pauseb.pressionadoE(mouse, mouse1):

					menupausa = True

					while menupausa:

						mouse = pygame.mouse.get_pos()
						mouse1 = pygame.mouse.get_pressed()


						Display.blit(pause_imagem, (320, 0))
						continueb.tela(Display, (491,105), mouse)
						voltar.tela(Display, (491,542), mouse)

						for event in pygame.event.get():

							if event.type == pygame.QUIT:
								rodando = False
								menupausa = False

							if continueb.pressionadoE(mouse,mouse1):
								menupausa = False

							if voltar.pressionadoE(mouse,mouse1):
								menupausa = False
								tela = 0

						pygame.display.update()
						clock.tick(60)



			rola += 1
			if rola == 30:
				rola = 0
				contagem -= 1
				if contagem < 0:
					inicio_corrida = 0

#--------------------Corrida em sí------------------------------#

		else:

			vel = carroP.speeder()
			x_bg, x_bg1, dis = mov_aparente(Display,background,vel,x_bg,x_bg1,chegada,dis)
			pauseb.tela(Display, (1085, 12), mouse)

#--------------------Interações com o jogador------------------------------#

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

				if pauseb.pressionadoE(mouse, mouse1):

					menupausa = True

					while menupausa:

						mouse = pygame.mouse.get_pos()
						mouse1 = pygame.mouse.get_pressed()

						Display.blit(pause_azul, (320, 0))
						continueb.tela(Display, (491,105), mouse)
						voltar.tela(Display, (491,542), mouse)

						for event in pygame.event.get():

							if event.type == pygame.QUIT:
								rodando = False
								menupausa = False

							if continueb.pressionadoE(mouse,mouse1):
								menupausa = False

							if voltar.pressionadoE(mouse,mouse1):
								menupausa = False
								tela = 0

						pygame.display.update()
						clock.tick(60)

			carroP.gas_pedal(acelerando)
			xi,ticks = carroadv.draw(Display,xi,vel,ticks,choice(range(3)))
			posicao = carroP.draw(Display)
		
#--------------------Veirifica quando a corrida acaba e quem ganhou------------------------------#

			if dis < posicao:

				tela = 0


				if posicao < xi:

					coins += 20

					ymensagem = 730

					while ymensagem > 0:

						Display.blit(background, (0,0))
						carroP.foward(Display,vel)
						Display.blit(you_lose, (500,ymensagem))
						ymensagem -= 5

						pygame.display.update()
						clock.tick(60)

				else:

					coins += 100
					ymensagem = 730

					while ymensagem > 0:

						Display.blit(background, (0,0))
						carroP.foward(Display,vel)
						Display.blit(you_win, (500,ymensagem))
						ymensagem -= 5

						pygame.display.update()
						clock.tick(60)

#--------------------Menu de upgrades------------------------------#

	if tela == 2:
		if not musica_aux:
			if(musica_on):
				pygame.mixer.music.load(r'.\Sounds\top_gear.mp3')
				pygame.mixer.music.play(-1)

			musica_aux = True
		Display.blit(plano, (0,0))
		Display.blit(evocoins, (1129,7))
		TextoT(Display, coins, (1030, 11), branco, 41)
		voltar.tela(Display, (950,600), mouse)

#--------------------Escolha de tier------------------------------#

		if tier == 0:

			tier_1.tela(Display, (443, 124), mouse)
			tier_2.tela(Display, (443, 315), mouse)

#--------------------Interações com o jogador------------------------------#

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					rodando = False

				if tier_1.pressionadoE(mouse, mouse1):
					if tier_1.block == 0 and coins >= tier_1.cos:
						tier_1.block = 1
						coins -= tier_1.cos

					elif tier_1.block == 1:
						tier = 1

				if tier_2.pressionadoE(mouse, mouse1):
					if tier_2.block == 0 and coins >= tier_2.cos:
						tier_2.block = 1
						coins -= tier_2.cos

					elif tier_2.block == 1:
						tier = 2

				if voltar.pressionadoE(mouse, mouse1):
					tela = 0

#--------------------Upgrades tier 1------------------------------#

		elif tier == 1:

			tier_1b.tela(Display, (display_width/2 - 151, 47), mouse)

			little_rodab.tela(Display, (194,313), mouse)
			blue_rally_jeepb.tela(Display, (194,160), mouse)
			streetb.tela(Display, (194,466), mouse)

			blue_jeepb.tela(Display, (788,160), mouse)
			roda_thunderb.tela(Display, (788,313), mouse)
			desertb.tela(Display, (788,466), mouse)

#--------------------Interações com o jogador------------------------------#

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					rodando = False

				if blue_jeepb.pressionadoE(mouse, mouse1):

					if blue_jeepb.block == 0 and coins >= blue_jeepb.cos:
						blue_jeepb.block = 1
						coins -= blue_jeepb.cos

					elif blue_jeepb.block == 1:
						carroP = blue_jeep

				if blue_rally_jeepb.pressionadoE(mouse, mouse1):

					if blue_rally_jeepb.block == 0 and coins >= blue_rally_jeepb.cos:
						blue_rally_jeepb.block = 1
						coins -= blue_rally_jeepb.cos

					elif blue_rally_jeepb.block == 1:
						carroP = blue_rally_jeep

				if streetb.pressionadoE(mouse, mouse1):

					if streetb.block == 0 and coins >= streetb.cos:
						streetb.block = 1
						coins -= streetb.cos

					elif streetb.block == 1:

						background = street

				if desertb.pressionadoE(mouse, mouse1):

					if desertb.block == 0 and coins >= desertb.cos:
						desertb.block = 1
						coins -= desertb.cos

					elif desertb.block == 1:
						background = desert

				if roda_thunderb.pressionadoE(mouse, mouse1):

					if roda_thunderb.block == 0 and coins >= roda_thunderb.cos:
						roda_thunderb.block = 1
						coins -= roda_thunderb.cos

					elif roda_thunderb.block == 1:

						carroP.roda = roda_thunder	

				if little_rodab.pressionadoE(mouse, mouse1):

					if little_rodab.block == 0 and coins >= little_rodab.cos:
						little_rodab.block = 1
						coins -= little_rodab.cos

					elif little_rodab.block == 1:
						carroP.roda = roda_little

				if voltar.pressionadoE(mouse, mouse1):
					tier = 0

				if tier_1b.pressionadoE(mouse, mouse1):

					if tier_1b.block == 0 and coins >= tier_1b.cos:
						tier_1b.block = 1
						coins -= tier_1b.cos

					elif tier_1b.block == 1:
						play = botao_comum(r'.\Sprites\botões\set_azul\play_button.png',r'.\Sprites\botões\set_azul\play_button_blue_shadow.png',1, 0)
						upgrade = botao_comum(r'.\Sprites\botões\set_azul\upgrade_button.png',r'.\Sprites\botões\set_azul\upgrade_button_shadow.png',1, 0)
						voltar = botao_comum(r'.\Sprites\botões\set_azul\back_button.png',r'.\Sprites\botões\set_azul\back_button_shadow.png',1, 0)
						pauseb = botao_comum(r'.\Sprites\botões\set_azul\pause_button_blue.png',r'.\Sprites\botões\set_azul\pause_button_blue_shadow.png',1, 0)
						continueb = botao_comum(r'.\Sprites\botões\set_azul\continue_button.png',r'.\Sprites\botões\set_azul\continue_button_shadow.png',1, 0)

#--------------------IUpgrade tier 2------------------------------#

		elif tier == 2:

			tier_2b.tela(Display, (display_width/2 - 151, 47), mouse)

			black_suvb.tela(Display, (194,160), mouse)
			roda_xb.tela(Display, (194,313), mouse)
			lunarb.tela(Display, (194,466), mouse)

			red_camarob.tela(Display, (788,160), mouse)
			roda_bmwb.tela(Display, (788,313), mouse)
			nuvensb.tela(Display, (788,466), mouse)

#--------------------Interações com o jogador------------------------------#

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					rodando = False

				if black_suvb.pressionadoE(mouse, mouse1):

					if black_suvb.block == 0 and coins >= black_suvb.cos:
						black_suvb.block = 1
						coins -= black_suvb.cos

					elif black_suvb.block == 1:
						carroP = black_suv

				if red_camarob.pressionadoE(mouse, mouse1):

					if red_camarob.block == 0 and coins >= red_camarob.cos:
						red_camarob.block = 1
						coins -= red_camarob.cos

					elif red_camarob.block == 1:
						carroP = camaro_vermelho

				if lunarb.pressionadoE(mouse, mouse1):

					if lunarb.block == 0 and coins >= lunarb.cos:
						lunarb.block = 1
						coins -= lunarb.cos

					elif lunarb.block == 1:
						background = lunar

				if nuvensb.pressionadoE(mouse, mouse1):

					if nuvensb.block == 0 and coins >= nuvensb.cos:
						nuvensb.block = 1
						coins -= nuvensb.cos

					elif nuvensb.block == 1:
						background = nuvens

				if roda_xb.pressionadoE(mouse, mouse1):

					if roda_xb.block == 0 and coins >= roda_xb.cos:
						roda_xb.block = 1
						coins -= roda_xb.cos

					elif roda_xb.block == 1:

						carroP.roda = roda_x	

				if roda_bmwb.pressionadoE(mouse, mouse1):

					if roda_bmwb.block == 0 and coins >= roda_bmwb.cos:
						roda_bmwb.block = 1
						coins -= roda_bmwb.cos

					elif roda_bmwb.block == 1:
						carroP.roda = roda_bmw

				if voltar.pressionadoE(mouse, mouse1):
					tier = 0

				if tier_2b.pressionadoE(mouse, mouse1):

					if tier_2b.block == 0 and coins >= tier_2b.cos:
						tier_2b.block = 1
						coins -= tier_2b.cos

					elif tier_2b.block == 1:
						play = botao_comum(r'.\Sprites\botões\set_verde\play_button_green.png',r'.\Sprites\botões\set_verde\play_button_green_shadow.png',1, 0)
						upgrade = botao_comum(r'.\Sprites\botões\set_verde\upgrade_button_green.png',r'.\Sprites\botões\set_verde\upgrade_button_green_shadow.png',1, 0)
						voltar = botao_comum(r'.\Sprites\botões\set_verde\back_button.png',r'.\Sprites\botões\set_verde\back_button_shadow.png',1, 0)
						pauseb = botao_comum(r'.\Sprites\botões\set_verde\pause_button_green.png',r'.\Sprites\botões\set_verde\pause_button_green_shadow.png',1, 0)
						continueb = botao_comum(r'.\Sprites\botões\set_verde\continue_button.png',r'.\Sprites\botões\set_verde\continue_button_shadow.png',1, 0)
						menu = menu_engrenagem
						plano = tela_engrenagem
						voltar.tela(Display, (950,600), mouse)


	pygame.display.update()
	clock.tick(60)

#--------------------Salvando estado atual------------------------------#
data[0]["coins"] = coins 
data[1]["inicio"] = int(inicio)
data[1]["musica_on"] = int(musica_on)

with open('data.json','w') as arquivo: #Guarda o save
	json.dump(data,arquivo)

pygame.quit() #Encerra o pygame e salva o jogo
quit()