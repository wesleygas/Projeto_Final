# Projeto_Final
Dragster UpgradeTotal




- Problemas e soluções para um jogo local split-screen:
	http://stackoverflow.com/questions/20403675/how-to-create-a-4-way-split-screen-in-pygame
- Sprite sources:
	http://unity3diy.blogspot.com.br/2014/11/Free-Sprites-Download-For-YourGames.html

- Lógica de controle de velocidade dos carros:
	- Velocidade é igual a uma multiplicação do RPM do motor do carro pela marcha 
	
Carro(sprite): [        gear ratios       ] / max rpm / torque multiplier || Curva do inimigo


Carro azul   : [0,0.75,1.00,1.50,1.90,2.77] / 4000    /50		  || [[2,6,0.2],[2,9,0],[2,15,1]]



Black SUV    : [0,0.81,0.96,1.31,1.90,3.16] / 4000    /60		  || [[ ],[ ],[ ]]

Outro carro  : [0,0.85,1.16,1.55,2.37,4.06] / 4500    /60		  || [[ ],[ ],[ ]]




Lógica json: Guardar as tiers e os upgrades ativos como booleanas, assim como o número de moedas, RECORDES DE TEMPO, curvas de velocidade

o json será carregado como uma lista: "data":
	O primeiro item dessa lista são as informações de posse: Quantas moedas o player tem, os melhores tempos dele, qual tier ele desbloqueou, quais carros e pistas ele tem.
	O segundo item são as settings: Música on/off e algo mais
	O terceiro é o database: As potências e as curvas de cada carro do player e da IA
