import pygame
from pygame import gfxdraw
import math
import numpy as np


def getAngle(p1, p2):
    angle = math.atan2(p1[1] - p2[1], p1[0] - p2[0])
    return np.interp(angle, [-math.pi, math.pi], [360, 0])

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def rotate(image, center, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=center)
    return new_image, rect

def pointDistance(p1,p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def drawLine2(X0,X1,window):
    center_L1 = ((X0[0] + X1[0])/2.,  (X1[1] + X0[1])/2.)
    length = pointDistance(X0,X1)  # Line size
    thickness = 20
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    c = math.cos(angle)
    s = math.sin(angle)
    UL = (center_L1[0] + (length / 2.) * c - (thickness / 2.) * s,
          center_L1[1] + (thickness / 2.) * c + (length / 2.) * s)
    UR = (center_L1[0] - (length / 2.) * c - (thickness / 2.) * s,
          center_L1[1] + (thickness / 2.) * c - (length / 2.) * s)
    BL = (center_L1[0] + (length / 2.) * c + (thickness / 2.) * s,
          center_L1[1] - (thickness / 2.) * c + (length / 2.) * s)
    BR = (center_L1[0] - (length / 2.) * c + (thickness / 2.) * s,
          center_L1[1] - (thickness / 2.) * c - (length / 2.) * s)
    pygame.gfxdraw.filled_polygon(window, (UL, UR, BR, BL), (0,0,0))
    pygame.gfxdraw.aapolygon(window, (UL, UR, BR, BL), (255,255,255))

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):

    if rect is None: rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom
    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
            )
            fn_line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
            )
            fn_line(surface, color, (col, y1), (col, y2))