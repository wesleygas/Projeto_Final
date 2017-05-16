# -*- coding: utf-8 -*-
"""
Created on Thu May  4 10:51:24 2017

@author: jhona
"""

import pygame
from pygame.locals import *

class botao_comum:
    
    def __init__(self, janela, pos, imag):
        self.ima = pygame.image.load(imag)
        self.dimen = self.ima.get_size()    
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