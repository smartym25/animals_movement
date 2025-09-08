import pygame
import math
import numpy as np 
import random

width = 1400
height = 700

rate = 120
number_bees = 60
factor_amplitude = 0.5
number_parent_flowers = 4

pygame.init()

centers = {
    1: (130, 120),
    2: (450, 560),
    3: (800, 200),
    4: (1260, 450)
}

colors = {
    1: [(5, 125, 173), (49, 189, 245)],   #light blue
    2: [(201, 91, 6), (237, 135, 57)],   #orange
    3: [(168, 8, 69), (235, 38, 113)],   #dark pink
    4: [(227, 176, 9), (240, 198, 62)]  #yellow   
}

features_flowers = {
    #   vertex, r, rip, rop
    1: [(8), (60), (40), (45)],   
    2: [(12), (65), (35),(40)],      
    3: [(15), (70), (50), (55)],  
    4: [(6), (75), (45), (50)] 
}

class Bee():
    def __init__(self, x, y = 700):
        self.x = x
        self.y = y
        self.direction = random.uniform(0, math.pi)
        self.has_first_pollen = False 
        self.speed = 3
        self.parents_flower = set()

    def move(self):

        self.direction += random.uniform(-0.4, 0.4)
                    
        self.x += math.cos(self.direction)
        self.y += math.sin(self.direction)

        for i in range(1,number_parent_flowers+1):
            d = math.sqrt((self.x - centers[i][0])**2 + (self.y - centers[i][1])**2)
            
            if self.has_first_pollen == False and any(d <= r for r in pollen_radius):

                # il movimento deve essere parabolico, voglio che il centro sia vertice della mia parabola

                a =  ((self.y-centers[i][1]) / (self.x**2 - 2 * centers[i][0] * self.x + centers[i][0]**2)) * factor_amplitude
                b = -2 * a * centers[i][0]

                dp = 2*a*self.x + b + random.uniform(-0.3, 0.3)

                self.parents_flower.add(i) # memorizza i fiori nella quale è stata l'ape

                self.direction = math.atan(dp)

        #walls 
        if self.x <= 0 or self.x >= 1400:
            self.direction = math.pi - self.direction  

        if self.y <= 0 or self.y >= 700:
            self.direction = -self.direction  

    def new_gen_flowers(self):

            p1_flower = list(self.parents_flower)[0]
            p2_flower = list(self.parents_flower)[1]
            
            new_R_cip = (colors[p1_flower][1][0] + colors[p2_flower][1][0]) * 0.5
            new_G_cip = (colors[p1_flower][1][1] + colors[p2_flower][1][1]) * 0.5
            new_B_cip = (colors[p1_flower][1][2] + colors[p2_flower][1][2]) * 0.5

            new_R_cop = (colors[p1_flower][0][0] + colors[p2_flower][0][0]) * 0.5
            new_G_cop = (colors[p1_flower][0][1] + colors[p2_flower][0][1]) * 0.5
            new_B_cop = (colors[p1_flower][0][2] + colors[p2_flower][0][2]) * 0.5
            
            cip_son = (new_R_cip, new_G_cip, new_B_cip)
            cop_son = (new_R_cop, new_G_cop, new_B_cop)

            vertex_count_son = (features_flowers[p1_flower][0] + features_flowers[p2_flower][0]) * 0.5

            r_son = (features_flowers[p1_flower][1] + features_flowers[p2_flower][1]) * 0.5

            rip_son = (features_flowers[p1_flower][2] + features_flowers[p2_flower][2]) * 0.5
            rop_son = (features_flowers[p1_flower][3] + features_flowers[p2_flower][3]) * 0.5

            center_x_son = (centers[p1_flower][0] + centers[p2_flower][0]) * 0.5
            self.x = center_x_son + random.uniform(-5,5)

            center_y_son = (centers[p1_flower][1] + centers[p2_flower][1]) * 0.5
            self.y = center_y_son + random.uniform(-5,5)

            new_gen = draw_flower_circle(screen, cip_son, cop_son, vertex_count_son, r_son, rip_son, rop_son, (center_x_son, center_y_son))
            return new_gen
    
def draw_flower_circle(screen, cip, cop, vertex_count, r, rip, rop, center_position):
    points_flower = []

    n = vertex_count
    x,y = center_position

    for i in range(1, int(n+1)):
        theta = (2 * math.pi * i) / n

        xf = x + r * math.cos(theta)
        yf = y + r * math.sin(theta)

        points_flower.append((xf, yf))

    for i in range(int(n)):
        pygame.draw.circle(screen, cip, (points_flower[i]), rip)
    for i in range(int(n)):
        pygame.draw.circle(screen, cop, (points_flower[i]), rop, 5)

    pygame.draw.polygon(screen, (209, 146, 63), points_flower, 6)

bees = [Bee(x=random.choice([0,1400]), y = random.choice([0,700])) for _ in range(number_bees)]  

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

radius = 60 
direction = 0.2
pollen_radius = []

running = True
while running:

    screen.fill((0, 0, 0))

    if radius < 160:
        radius += direction
    if radius >= 160:
        radius *= -direction

    pollen_radius = [radius]

    for i in range(1,number_parent_flowers+1):
        pygame.draw.circle(screen, colors[i][0], centers[i], radius, 3)
 
    draw_flower_circle(screen, colors[1][1], colors[1][0], 
                       features_flowers[1][0], features_flowers[1][1], features_flowers[1][2], features_flowers[1][3], centers[1])

    draw_flower_circle(screen, colors[2][1], colors[2][0], 
                       features_flowers[2][0], features_flowers[2][1], features_flowers[2][2], features_flowers[2][3], centers[2])

    draw_flower_circle(screen, colors[3][1], colors[3][0], 
                       features_flowers[3][0], features_flowers[3][1], features_flowers[3][2], features_flowers[3][3], centers[3])

    draw_flower_circle(screen, colors[4][1], colors[4][0], 
                       features_flowers[4][0], features_flowers[4][1], features_flowers[4][2], features_flowers[4][3], centers[4])

    for bee in bees:      

        if len(bee.parents_flower) == 2:
            bee.new_gen_flowers()
            pygame.draw.circle(screen, (255,255,0), (int(bee.x), int(bee.y)), 4)

        else:
            pygame.draw.circle(screen, (255,255,0), (int(bee.x), int(bee.y)), 4) 
            bee.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(rate)
    pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")
    pygame.display.flip()

pygame.quit()
