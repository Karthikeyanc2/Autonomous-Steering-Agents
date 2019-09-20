import pygame
import random
import math
pygame.init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

width = 1200
height = 800

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Autonomous agents")
clock = pygame.time.Clock()


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, new):
        self.x += new.x
        self.y += new.y

    def limit(self, max_):
        if self.mag() > max_:
            self.set_mag(max_)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def set_mag(self, value):
        self.x, self.y = value*self.x/self.mag(), value*self.y/self.mag()

    def distance(self, dish):
        return math.sqrt((self.x - dish.pos.x) * (self.x - dish.pos.x) + (self.y - dish.pos.y) * (self.y - dish.pos.y))


class Food:
    def __init__(self, x, y, color=RED, size=6):
        self.pos = Vec2d(x, y)
        self.color = color
        self.size = size

    def show(self):
        pygame.draw.ellipse(screen, self.color, [self.pos.x - self.size/2, self.pos.y - self.size/2, self.size, self.size])


class Vehicle:
    def __init__(self, x, y, size=15):
        self.pos = Vec2d(x, y)
        self.vel = Vec2d(random.randrange(-5, 6), random.randrange(-5, 6))
        self.acc = Vec2d(0, 0)
        self.health = 1
        self.size = size
        self.theta = 0
        self.max_speed = 8
        self.max_force = 0.8
        self.range = 200

    def update(self):
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.vel.limit(self.max_speed)

    def show(self):
        self.theta = math.atan2(self.vel.y, self.vel.x)
        pygame.draw.polygon(screen, GREEN, [self.translate(Vec2d(self.size, 0)), self.translate(Vec2d(-self.size/3, self.size/2)), self.translate(Vec2d(0, 0)), self.translate(Vec2d(-self.size/3, -self.size/2))])

    def translate(self, point):
        x = self.pos.x + point.x * math.cos(self.theta) - point.y * math.sin(self.theta)
        y = self.pos.y + point.x * math.sin(self.theta) + point.y * math.cos(self.theta)
        return [x, y]

    def eat(self, list_):
        closest_dist = width * height
        if len(list_):
            closest = list_[0]
            for dish in list_:
                if self.pos.distance(dish) < closest_dist and self.pos.distance(dish) < self.range:
                    closest = dish
                    closest_dist = self.pos.distance(dish)
        else:
            closest = list_[0]
            for dish in list_:
                if self.pos.distance(dish) < closest_dist:
                    closest = dish
                    closest_dist = self.pos.distance(dish)
        self.seek(closest)
        if closest_dist < 10:
            list_.remove(closest)

    def seek(self, dish):
        desired = Vec2d(dish.pos.x - self.pos.x, dish.pos.y - self.pos.y)
        desired.set_mag(self.max_speed)
        steering_force = Vec2d(desired.x - self.vel.x, desired.y - self.vel.y)
        if steering_force.mag() > self.max_force:
            steering_force.set_mag(self.max_force)
        self.acc = steering_force


food_array = [Food(random.randrange(width), random.randrange(height)) for i in range(20)]
vehicles = [Vehicle(random.randrange(width), random.randrange(height)) for i in range(5)]

while not done:
    clock.tick(30)
    screen.fill(BLACK)
    if random.randrange(100) < 20:
        food_array.append(Food(random.randrange(width), random.randrange(height)))
    for food in food_array:
        food.show()
    for vehicle in vehicles:
        vehicle.update()
        vehicle.eat(food_array)
        vehicle.show()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
