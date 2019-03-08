import utils
import math
import pygame


class Projectile:
    def __init__(self, source, destination,destvertex, color, texture,speed=1):
        self.x, self.y = source
        self.dest = destination
        self.speed = speed
        self.texture = texture
        self.angle = utils.getAngle(source, self.dest)
        self.vx = speed * math.cos((-self.angle) * math.pi / 180.)
        self.vy = speed * math.sin((-self.angle) * math.pi / 180.)
        self.color = color
        self.destVertex = destvertex
        self.texture.fill(color, None, pygame.BLEND_MULT)
        #self.texture = pygame.transform.rotate(self.texture,self.angle+90)
        self.texture,_ = utils.rotate(self.texture,(self.x,self.y),self.angle+90)
        self.rect = self.texture.get_rect()
        self.rect.center = (self.x,self.y)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x,self.y)

    def isReached(self):
        return abs(self.dest[0] - self.x) < 2*self.speed and abs(self.dest[1] - self.y) < 2*self.speed

    def show(self, window):
        #pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), 5)
        window.blit(self.texture,self.rect)

    def getDest(self):
        return self.destVertex
