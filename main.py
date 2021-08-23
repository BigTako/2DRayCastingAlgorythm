import pygame
import math
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

def shift(lst, steps):
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            lst.append(lst.pop(0))
    else:
        for i in range(steps):
            lst.insert(0, lst.pop())

running = True
while running:
    clock.tick(30)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

    def calculate_rays(cos, sin , r, center):
        arc_points = []
        for i in range(len(cos)):
            x = center[0] + r * cos[i]
            y = center[1] - r * sin[i]
            points = [center, [x, y]]
            for rect in rects:
                clip_line = rect.clipline(center[0], center[1], x, y)
                if len(clip_line) != 0:
                    start, end = clip_line
                    points = [center, start]

            if i == 0 or i == len(cosinuses) - 1:
                ray = Ray(WHITE, points, 1, True)
            else:
                ray = Ray(WHITE, points, 1, True)
            arc_points.append(points[1])
            objects.append(ray)
        return arc_points

    #<------MAIN GAME SCENE--------->
    # <------MAIN GAME SCENE--------->
    rect1 = pygame.Rect(800, 200, 300, 50)
    rect2 = pygame.Rect(800, 500, 50, 200)
    rect3 = pygame.Rect(1300, 200, 50, 200)
    rect4 = pygame.Rect(200, 800, 300, 50)
    rect5 = pygame.Rect(400, 400, 50, 300)
    rect6 = pygame.Rect(400, 100, 200, 50)
    rect7 = pygame.Rect(200, 300, (math.sqrt(2) * 80) / 2, (math.sqrt(2) * 80) / 2)

    rects = [rect1, rect2, rect3, rect4, rect5,rect7, rect6]

    obs1 = GameObject("rect", WHITE, [[rect1.x, rect1.y]], [rect1.w, rect1.h], True)
    obs2 = GameObject("rect", RED, [[rect2.x, rect2.y]], [rect2.w, rect2.h], True)
    obs3 = GameObject("rect", YELLOW, [[rect3.x, rect3.y]], [rect3.w, rect3.h], True)
    obs4 = GameObject("rect", GREEN, [[rect4.x, rect4.y]], [rect4.w, rect4.h], True)
    obs5 = GameObject("rect", GRAY, [[rect5.x, rect5.y]], [rect5.w, rect5.h], True)
    obs6 = GameObject("rect", LIGHT_BLUE, [[rect6.x, rect6.y]], [rect6.w, rect6.h], True)
    obs7 = GameObject("circle", WHITE, [[rect7.x, rect7.y]], 80, True)
    # <------MAIN GAME SCENE--------->

    # <----------GAME CONTROLS ----------------->

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and y_c >= 15:  # move up
        y_c -= speed
    if keys[pygame.K_s] and y_c <= (dh - 15):
        y_c += speed
    if keys[pygame.K_a] and x_c >= 15:  # move left
        x_c -= speed
    if keys[pygame.K_d] and x_c <= (dw - 15):  # move left
        x_c += speed

    # <----------GAME CONTROLS ----------------->\a
    objects = [obs7, obs1, obs2, obs4, obs5, obs6, obs3]

    A = pygame.mouse.get_pos()
    O = [x_c, y_c]

    OA = math.sqrt((A[0] - O[0]) ** 2 + (A[1] - O[1]) ** 2)
    AB = O[1] - A[1]
    OB = A[0] - O[0]
    sin = AB / OA
    cos = OB / OA

    view_angle = 100  # degrees
    ray_len = 700

    # <--+--> first ray
    cos_1 = (cos * math.cos(math.radians(view_angle / 2))) - (sin * math.sin(math.radians(view_angle / 2)))
    sin_1 = (sin * math.cos(math.radians(view_angle / 2))) + (cos * math.sin(math.radians(view_angle / 2)))
    # <--+-->
    cosinuses = [cos_1]
    sinuses = [sin_1]

    for i in range(1, view_angle):
        cos = (cos_1 * math.cos(math.radians(i)) + sin_1 * math.sin(math.radians(i)))
        sin = (sin_1 * math.cos(math.radians(i)) - math.sin(math.radians(i)) * cos_1)
        cosinuses.append(cos)
        sinuses.append(sin)

    cos_2 = (cos * math.cos(math.radians(view_angle / 2))) + (sin * math.sin(math.radians(view_angle / 2)))
    sin_2 = (sin * math.cos(math.radians(view_angle / 2))) - (cos * math.sin(math.radians(view_angle / 2)))



    arc_points = calculate_rays(cosinuses, sinuses, ray_len, O)
    pygame.draw.aalines(win, RED, False,arc_points, 5)

    main_scene = Scene(win)
    user = GameObject("circle", YELLOW, [O], 15, True)
    objects.append(user)
    for i in objects:
        main_scene.add(i)
    main_scene.show()
    pygame.display.update()
    win.fill((0, 0, 0))


