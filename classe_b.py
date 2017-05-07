# -*- coding: utf-8 -*-
"""
Created on Thu May  4 10:51:24 2017

@author: jhona
"""

import pygame
from pygame.locals import *

class botao_comum:
    
    def __init__(self, janela, pos, imag, l, a):
        janela.blit(pygame.image.load(imag), (pos[0], pos[1]))
        self.ix = pos[0]
        self.fx = pos[0] + l
        self.iy = pos[1]
        self.fy = pos[1] + a

    def precionadoE(self, mpos, mpres):
        if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy and mpres[0] == 1:
            return True
    
    def precionadoR(self, mpos, mpres):
        if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy and mpres[0] == 2:
            return True
        
    def precionadoD(self, mpos, mpres):
        if self.ix < mpos[0] < self.fx and self.iy < mpres[1] < self.fy and mpres[0] == 3:
            return True
    
    def em_cima(self, mpos):
        if self.ix < mpos[0] < self.fx and self.iy < mpos[1] < self.fy:
            return True