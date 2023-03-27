import pygame
import pyivp
import json
from random import choice

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)


class Brick():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.poly = pyivp.string_to_poly(
            "x = " + str(x) + ", y = " + str(y) + ", format = radial, radius = " + str(radius) + ", pts = 4")
        self.get_vertex()

    def get_vertex(self):
        self.vertex = []
        self.seg = self.poly.export_seglist()
        for i in range(self.seg.size()):
            self.vertex.append((self.seg.get_vx(i), self.seg.get_vy(i)))

    def draw(self, screen):
        pygame.draw.lines(screen, WHITE, True, self.vertex)

    def dis_to_brick(self, x, y):
        return self.poly.dist_to_poly(x, y)

class Pad(Brick):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.poly = pyivp.string_to_poly(
            "x = " + str(x) + ", y = " + str(y) + ", format = radial, radius = " + str(radius) + ", pts = 4")
        self.get_vertex()
    def moveright(self):
        self.x += 2
    def moveleft(self):
        self.x -= 2

class Ball():
    def __init__(self, x, y, radius):
        self.x = 300
        self.y = 400
        self.x_direction = choice((-3, 3))
        self.y_direction = -3
        self.radius = 10

    def move(self):
        self.x += self.x_direction
        self.y += self.y_direction
        self.contact_detect_wall()

    def bounce(self, brick):
        if self.x < brick.x - (brick.radius / 1.414):
            self.x_direction = -3
        elif self.x > brick.x + (brick.radius / 1.414):
            self.x_direction = 3
        elif self.y < brick.y - (brick.radius / 1.414):
            self.y_direction = -3
        elif self.y > brick.y + (brick.radius / 1.414):
            self.y_direction = 3

    def contact_detect_wall(self):
        if self.x + self.radius >= SCREEN_WIDTH or\
                self.x - self.radius <= 0:
            self.x_direction = -self.x_direction

        if self.y + self.radius >= SCREEN_HEIGHT or self.y - self.radius <= 0:
            self.y_direction = -self.y_direction
        
        if self.y + self.radius >= SCREEN_HEIGHT:
            self.x_direction = 0
            self.y_direction = 0

    def contact_detect_brick(self, brick):
        if (brick.dis_to_brick(self.x, self.y) - self.radius <= 0):
            self.bounce(brick)
            return 1

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Brick')

# load config
with open('./config/20230327_demo3.json', 'r') as f:
    config = json.load(f)

ball = Ball(config["ball_x"], config["ball_y"], config["ball_radius"])
brick_list = []
for brick_config in config["bricks"]:
    brick_list.append(
        Brick(brick_config['x'], brick_config['y'], brick_config['radius'])
    )
pad = Pad(config["pad_x"], config["pad_y"], config["pad_radius"])
x_value = config["pad_x"]


#brick1 = Brick(config["bricks"][0]["x"], config["bricks"][0]["y"], config["bricks"][0]["radius"])
#brick2 = Brick(config["bricks"][1]["x"], config["bricks"][1]["y"], config["bricks"][1]["radius"])
#brick3 = Brick(config["bricks"][2]["x"], config["bricks"][2]["y"], config["bricks"][2]["radius"])

# game loop
is_running = True
while is_running:
    screen.fill((0, 0, 0))
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        Pad.moveright()
        pad.draw(screen)
        # x_value += 2
        # pad = Pad(x_value, config["pad_y"], config["pad_radius"])
    if key[pygame.K_LEFT]:
        Pad.moveleft()
        pad.draw(screen)
        # x_value -= 2
        # pad = Pad(x_value, config["pad_y"], config["pad_radius"])
    
    ball.contact_detect_brick(pad)
    
    # for brick in brick_list:
    #     brick.draw(screen)
    #     ball.contact_detect_brick(brick)
    #     brick_list[brick] = Brick(0,1,1)
    pad.draw(screen)

    for i in range(len(brick_list)):
        try:
            brick_list[i].draw(screen)
        except:
            continue

        if ball.contact_detect_brick(brick_list[i]) == 1:
            brick_list[i] = Brick(0,0,0)
    
    ball.move()
    ball.draw(screen)

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            is_running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
