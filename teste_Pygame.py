import pygame
pygame.init()
#iniciando display-------------------------iniciando display

Display = pygame.display.set_mode((1280,720)) #Tamanho da janela
pygame.display.set_caption('Boravê') #Nome da janela


clock = pygame.time.Clock()
#Funções úteis------------------------------Funções úteis
	
def check_quit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	

rodando = True
while rodando:
	eventos = pygame.event.get()
	rodando = check_quit()
	

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()
