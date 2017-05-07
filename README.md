# Projeto_Final
Dragster UpgradeTotal

Para o dia 09/05/2017:
	- Interface gráfica "intermediária" funcionando
		- Sprites da corrida:
			- Pista, background, carros, start and finish lines
	- Corrida básica(voltada para um ponto(que será substituído pelo carro))
		- Lógica de aceleração e troca de marchas

- Lógica gráfica da corrida: 'x' refere-se à coordenada x na tela; velocidade seria igual a "dx"
	- O carro ficará parado na tela e a posição 'x' dele mudará apenas de acordo com a aceleração (Vf-Vi)/(Tf-Ti)
	-  O backgroud(e a pista) pode ser dividido entre 2 ou mais partes, se movendo para trás à velocidade 'x' do carro
	Quando uma parte sair da tela, esta é apagada e outra igual é renderizada no começo da fila, fora da tela
	para que, no final, fique uma esteira, rodando as mesmas partes.
	- O carro dos inimigos terá a velocidade 'x' igual à velocidade "teórica" menos a velocidade 'x' do carro do jogador
	ou seja, dx_real_oponente = dx_teorica_oponente - dx_teorica_player

- Problemas e soluções para um jogo local split-screen:
	http://stackoverflow.com/questions/20403675/how-to-create-a-4-way-split-screen-in-pygame
- Sprite sources:
	http://unity3diy.blogspot.com.br/2014/11/Free-Sprites-Download-For-YourGames.html