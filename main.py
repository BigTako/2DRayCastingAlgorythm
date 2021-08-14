import math
import time

import pygame
import sys

pygame.init()

pygame.display.set_caption('DOOM')
dw = 1400
dh = 750
speed = 4
clock = pygame.time.Clock()
win = pygame.display.set_mode((dw, dh))

# <--FIRST LINE COORDINATES-->
x_c = dw // 2  # 125
y_c = dh // 2  # 125
x_e = dw - 200
y_e = dh // 2
# <--SECOND LINE COORDINATES-->
x_c2 = dw // 2  # 125d
y_c2 = dh // 2  # 125
x_e2 = x_e + 350
y_e2 = dh // 2

# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)


class Scene:
    def __init__(self, surface):
        self.objects = []
        self.surface = surface

    def add(self, object):
        self.objects.append([object.type, object.color, object.points, object.params, object.display])

    def show(self):
        for i in range(len(self.objects)):
            type = self.objects[i][0]
            color = self.objects[i][1]
            points = self.objects[i][2]
            params = self.objects[i][-2]
            display = self.objects[i][-1]
            try:
                if display:
                    if type == "rect":
                        pygame.draw.rect(self.surface, color, [points[0][0], points[0][1], params[0], params[1]])
                    if type == "circle":
                        pygame.draw.circle(self.surface, color, *points, params)
                    if type == "line":
                        pygame.draw.line(self.surface, color, *points, params)
                    if type == "aaline":
                        pygame.draw.aaline(self.surface, color, *points)
                    if type == "lines(closed)":
                        pygame.draw.lines(self.surface, color, True, points, params)
                    if type == "aalines(closed)":
                        pygame.draw.lines(self.surface, color, True, points)
                    if type == "lines":
                        pygame.draw.lines(self.surface, color, False, points, params)
                    if type == "aalines":
                        pygame.draw.lines(self.surface, color, False, points)
                    if type == "polygon":
                        pygame.draw.polygon(self.surface, color, points)
                    if type == "ellipse":
                        pygame.draw.ellipse(self.surface, color, [points[0][0], points[0][1], params[0], params[1]])
                    if type == "arc":
                        pygame.draw.arc(self.surface, color, [points[0][0], points[0][1], params[0], params[1]],
                                        params[2], params[3])
            except Exception:
                print("Please, check object data!")
                print(sys.exc_info()[1])




class GameObject:
    def __init__(self, type, color, points, params, display):
        self.type = type
        self.color = color
        self.points = points
        self.params = params
        self.display = display
        self.border = []
    def calculate_border(self):
        if self.type == "rect":
            w = self.params[0]
            h = self.params[1]
            x = self.points[0][0]
            y = self.points[0][1]
            for i in range(w):
                self.border.append((x + i, y))
                self.border.append((x + i, y + h))
            for e in range(h):
                self.border.append((x, y + e))
                self.border.append((x + w, y + e))

        if self.type == "circle":
            color = self.color
            xc = self.points[0][0]
            yc = self.points[0][1]
            r = self.params
            C = 2 * math.pi * r
            alpha = 360 / C
            for i in range(int(C)):
                x = round(xc - (r * math.cos(math.radians(alpha))))
                y = round(yc - (r * math.sin(math.radians(alpha))))
                alpha += alpha
                self.border.append((x, y))

        return self.border

class Ray(GameObject):
    def __init__(self, color, points, params, display):
        super().__init__(type, color, points, params, display)
        self.type = "line"



# <----------MAIN CYCLE ----------------->

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    main_scene = Scene(win)

    #<------MAIN GAME SCENE--------->
    obs1 = GameObject("rect", WHITE, [[800, 200]], [300, 50], True)
    obs2 = GameObject("rect", WHITE, [[800, 400]], [50, 200], True)
    obs3 = GameObject("rect", WHITE, [[1300, 200]], [50, 400], True)
    obs4 = GameObject("rect", WHITE, [[200, 800]], [600, 50], True)
    obs5 = GameObject("rect", WHITE, [[400, 400]], [50, 300], True)
    obs6 = GameObject("rect", WHITE, [[400, 100]], [200, 50], True)
    obs7 = GameObject("circle", WHITE, [[200, 300]], 80, True)
    # <------MAIN GAME SCENE--------->

    # <----------GAME CONTROLS ----------------->
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and y_c >= 15:  # move up
        y_c -= speed
        y_e -= speed

    if keys[pygame.K_s] and y_c <= (dh - 15):  # move down
        y_c += speed
        y_e += speed

    if keys[pygame.K_a] and x_c >= 15:  # move left
        x_c -= speed
        x_e -= speed

    if keys[pygame.K_d] and x_c <= (dw - 15):  # move left
        x_c += speed
        x_e += speed

    # <----------GAME CONTROLS ----------------->

    center = [x_c, y_c]

    user = GameObject("circle", YELLOW, [[center[0], center[1]]], 15, True)
    objects = [obs1, obs2, obs3, obs4, obs5, obs6, obs7, user]

    for i in objects:
        main_scene.add(i)
    main_scene.compare(objects)
    main_scene.show()
    pygame.display.update()
    win.fill((0, 0, 0))


