import pygame
import cfg
import numpy as np
import utils
import textures
MAX = 20


class Node:
    def __init__(self, x, y, texture, val=0):
        self.value = val
        self.x = x
        self.y = y
        self.r = 50
        self.texture = texture
        self.OGtexture = texture
        self.number = val
        self.size = None
        self.angle = 0
        self.changeVal(val)
        self.color = (255, 255, 255)
        self.Blink = False
        self.blinkFrames = [t.copy() for t in textures.blinkFrames]
        self.frame = 0
        self.seq = [i for i in range(len(self.blinkFrames))] + [9-i for i in range(len(self.blinkFrames))]
        self.animdir = 1

    def changeTexture(self, texture):
        self.texture = texture
        self.OGtexture = texture

    def changeTextureColor(self, color):
        self.texture = self.OGtexture.copy()
        self.texture.fill(color, None, pygame.BLEND_MULT)
        self.blinkFrames = [t.copy() for t in textures.blinkFrames]
        for t in self.blinkFrames:
            t.fill(color, None, pygame.BLEND_MULT)
        self.color = color

    def changeVal(self, val):
        self.value = val
        inter = np.interp(abs(self.value), [0, MAX], [255, 0])
        if self.value < 0:
            color = (255, inter, inter)
        else:
            color = (inter, 255, inter)
        self.changeTextureColor(color)
        self.number = cfg.Font.render(str(self.value), True, (255, 255, 255))
        self.size = cfg.Font.size(str(self.value))

    def show(self, window):

        # pygame.gfxdraw.aacircle(window, self.x, self.y, self.r, color)
        # pygame.gfxdraw.filled_circle(window, self.x, self.y, self.r, color)
        if self.Blink:
            window.blit(utils.rot_center(self.blinkFrames[self.seq[self.frame]], self.angle), (self.x - self.r, self.y - self.r))
            self.frame+=self.animdir
            if self.frame >= len(self.seq) or self.frame <= 0:
                self.frame = 0
                self.Blink = False
        else:
            window.blit(utils.rot_center(self.texture, self.angle), (self.x - self.r, self.y - self.r))
        window.blit(self.number, (self.x - self.size[0] / 2, self.y - self.size[1] / 2))
        self.angle -= 5

    def intersects(self, pos):
        return (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2 < self.r ** 2

    def blink(self):
        self.Blink = True
        if self.frame > len(self.seq)/2:
            self.animdir = -1
        else:
            self.animdir = 1