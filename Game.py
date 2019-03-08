import pygame
import textures
from Graph import Graph
from Node import Node
import cfg
import utils
from Projectile import Projectile


class Game:
    def __init__(self, title, width, height):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWACCEL | pygame.DOUBLEBUF)
        pygame.display.set_caption(title)
        cfg.Font = pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf", 40)
        self.done = False
        self.clock = pygame.time.Clock()
        self.nodes = Graph()
        self.initBoard()
        self.edgeMotion = False
        self.edgeMotionV = None
        self.vertexMotion = False
        self.vertexMotionV = None
        self.BuildMode = True
        self.nodeToCopy = Node(self.WIDTH - 25, 25, textures.circlerot.copy(), 0)
        self.projectiles = []

    def initBoard(self):
        self.nodes.addVertex(Node(100, 200, textures.circlerot.copy(), 10))
        self.nodes.addVertex(Node(400, 300, textures.circlerot.copy(), -12))
        self.nodes.addVertex(Node(555, 234, textures.circlerot.copy(), 3))
        self.nodes.addVertex(Node(1000, 600, textures.circlerot.copy(), 0))
        self.nodes.joinVertices(1, 2)
        self.nodes.joinVertices(0, 2)
        self.nodes.joinVertices(3, 2)

    def drawEdges(self):
        for e in self.nodes.getEdges():
            utils.drawLine2((self.nodes[e[0]].x, self.nodes[e[0]].y), (self.nodes[e[1]].x,
                                 self.nodes[e[1]].y),self.window)
            # pygame.gfxdraw.line(self.window, self.nodes[e[0]].x, self.nodes[e[0]].y, self.nodes[e[1]].x,
            #                     self.nodes[e[1]].y, (255, 255, 255))
        if self.edgeMotion:
            pos = pygame.mouse.get_pos()
            node = self.nodes[self.edgeMotionV]
            #pygame.gfxdraw.line(self.window, node.x, node.y, *pos, (255, 255, 255))
            utils.drawLine2((node.x,node.y),pos,self.window)
            angle = utils.getAngle((node.x, node.y), pos)
            angle = cfg.Font.render(str(angle), True, (255, 255, 255))
            # size = cfg.Font.size(str(angle))
            self.window.blit(angle, (0, 0))

    def getIntersectingNode(self, pos):
        ret = -1
        for v in self.nodes:
            if self.nodes[v].intersects(pos):
                ret = v
                break
        return ret

    def moveVertex(self, rel):
        self.nodes[self.vertexMotionV].x += rel[0]
        self.nodes[self.vertexMotionV].y += rel[1]

    def donateMoney(self, vertex):
        for v in self.nodes.getNeighbors(vertex):
            n = self.nodes[v]
            nv = self.nodes[vertex]
            # n.changeVal(n.value + 1)
            nv.changeVal(nv.value - 1)
            self.projectiles.append(Projectile((nv.x, nv.y), (n.x, n.y), v, nv.color,textures.projectile_t.copy(), 9))

    def takeMoney(self, vertex):
        for v in self.nodes.getNeighbors(vertex):
            n = self.nodes[v]
            nv = self.nodes[vertex]
            n.changeVal(n.value - 1)
            # nv.changeVal(nv.value + 1)
            self.projectiles.append(Projectile((n.x, n.y), (nv.x, nv.y), vertex, n.color,textures.projectile_t.copy(), 9))

    def handleMouseEvents(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.BuildMode:
                if e.button == 1 and not self.vertexMotion:
                    v = self.getIntersectingNode(pygame.mouse.get_pos())
                    if v >= 0:
                        self.edgeMotion = True
                        self.edgeMotionV = v

                if e.button == 2 and not self.vertexMotion:
                    v = self.getIntersectingNode(pygame.mouse.get_pos())
                    if v >= 0:
                        self.nodes.delVertex(v)

                if e.button == 3:
                    v = self.getIntersectingNode(pygame.mouse.get_pos())
                    if v >= 0:
                        self.vertexMotion = True
                        self.vertexMotionV = v
                    elif self.nodeToCopy.intersects(pygame.mouse.get_pos()):
                        self.vertexMotion = True
                        self.vertexMotionV = self.nodes.addVertex(
                            Node(self.nodeToCopy.x, self.nodeToCopy.y, textures.circlerot, 0))

                if e.button == 4:
                    if self.vertexMotion:
                        self.nodes[self.vertexMotionV].changeVal(self.nodes[self.vertexMotionV].value + 1)
                    else:
                        v = self.getIntersectingNode(pygame.mouse.get_pos())
                        if v >= 0:
                            self.nodes[v].changeVal(self.nodes[v].value + 1)

                if e.button == 5:
                    if self.vertexMotion:
                        self.nodes[self.vertexMotionV].changeVal(self.nodes[self.vertexMotionV].value - 1)
                    else:
                        v = self.getIntersectingNode(pygame.mouse.get_pos())
                        if v >= 0:
                            self.nodes[v].changeVal(self.nodes[v].value - 1)
            else:
                if e.button == 1:
                    v = self.getIntersectingNode(pygame.mouse.get_pos())
                    if v >= 0:
                        self.donateMoney(v)

                if e.button == 3:
                    v = self.getIntersectingNode(pygame.mouse.get_pos())
                    if v >= 0:
                        self.takeMoney(v)

        if e.type == pygame.MOUSEBUTTONUP:
            if self.BuildMode:
                if e.button == 1:
                    if self.edgeMotion:
                        self.edgeMotion = False
                        v = self.getIntersectingNode(pygame.mouse.get_pos())
                        if v >= 0:
                            self.nodes.joinVertices(self.edgeMotionV, v)

                if e.button == 3:
                    if self.vertexMotion:
                        self.vertexMotion = False
            else:
                pass
        if e.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_rel()
            if self.BuildMode:
                if self.vertexMotion:
                    self.moveVertex(pos)

    def handleKeyboardEvents(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_TAB:
                self.BuildMode = not self.BuildMode
            if self.BuildMode:
                if e.key == pygame.K_SPACE:
                    self.nodes.addVertex(Node(*pygame.mouse.get_pos(), textures.circlerot.copy(), 0))
            else:
                pass

    def handleEvents(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.done = True
            self.handleKeyboardEvents(e)
            self.handleMouseEvents(e)
        # pressed = pygame.key.get_pressed()

    def mechanic(self):
        # self.moveVertex()
        for p in self.projectiles:
            p.move()
            if p.isReached():
                self.nodes[p.getDest()].blink()
                self.nodes[p.getDest()].changeVal(self.nodes[p.getDest()].value + 1)
                self.projectiles.remove(p)

        pass

    def display(self):
        self.window.fill((0, 0, 0))
        self.drawEdges()
        for p in self.projectiles:
            p.show(self.window)
        for v in self.nodes:
            self.nodes[v].show(self.window)
        self.nodeToCopy.show(self.window)
        pygame.display.flip()

    def run(self):
        while not self.done:
            self.handleEvents()
            self.mechanic()
            self.display()
            self.clock.tick(60)
        pygame.quit()
