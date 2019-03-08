import pygame
import utils


def loadTexture(path):
    bitmap = pygame.image.load(path)
    surface = pygame.Surface(bitmap.get_rect().size, flags=pygame.HWACCEL | pygame.SRCALPHA)
    surface.blit(bitmap, (0, 0))
    return surface


def makeProjectileT():
    s = pygame.Surface((19, 25))
    utils.fill_gradient(s, (0, 0, 0), (200, 200, 200))
    s2 = pygame.transform.rotate(s, 180)
    final = pygame.Surface((19, 50), flags=pygame.HWACCEL | pygame.SRCALPHA)
    final.blit(s, (0, 0))
    final.blit(s2, (0, 25))
    return final


circlerot = loadTexture('graphics\\circlerot2.png')
circlerot = pygame.transform.scale(circlerot, (100, 100))
blinkFrames = [pygame.transform.scale(loadTexture('graphics\\blink{}.png'.format(i + 1)), (100, 100)) for i in
               range(10)]
projectile_t = makeProjectileT()
