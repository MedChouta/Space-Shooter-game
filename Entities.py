import pygame
import time
import random

"""
this module contains every game Entity including the PLAYER, the BULLET, and the ENEMY

"""

class Entity:
    def __init__(self, posX, posY, width, height, speed, path):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.speed = speed
        self.path = path
        #self.img = self.img.convert_alpha()
        
    def move(self, speedX, speedY):
        self.posX += speedX
        self.posY += speedY

    def Rect(self):
        return pygame.Rect((self.posX, self.posY), (self.width, self.height))
    
    def draw(self, surface):
        surface.blit(self.img, self.Rect())
    
    def delete(self, entitiesList, element):
        index = entitiesList.index(element)
        entitiesList.pop(index)

    def collision(self, entity, *callback):
        if (((self.posX >= entity.posX and self.posX <= entity.posX + entity.width)
            or (self.posX + self.width/1.25 >= entity.posX and self.posX + self.width/1.25 <= entity.posX + entity.width))
            and ((self.posY >= entity.posY and self.posY <= entity.posY + entity.height)
            or (self.posY + entity.height/1.25 >= entity.posY and self.posY + entity.height/1.25 <= entity.posY + entity.height))):
            for func in callback:
                func()

    def load(self):
        self.img = pygame.image.load("assets/" + self.path + ".png")
        self.img = pygame.transform.scale(self.img, self.Rect().size)



"""
    Main character class

"""

class Player(Entity):
    
    def __init__(self, posX, posY, width, height, path, speed = 7):
        super().__init__(posX, posY, width, height, speed, path)
        self.load()

    def shoot(self):
        Bullet.bullets.append(Bullet(self.posX + self.width - 10, self.posY + int(self.height/4) - 3, 30, 7))

    def Boundaries(self, size):
        if self.posX <= 0:
            self.posX = 0
        elif self.posX >= int(size[0]/4) - self.width:
            self.posX = int(size[0]/4) - self.width
        if self.posY <= 0:
            self.posY = 0
        elif self.posY >= size[1] - self.height:
            self.posY = size[1] - self.height


"""

    Enemies class

"""
class Enemy(Entity):

    enemies = list()

    def __init__(self, posX, posY, width, height, img, speed = -3, path=None):
        super().__init__(posX, posY, width, height, speed, path)
        self.img = img
        self.transform()

    def collisionWithBullet(self, bullet, enemy, score):
        if (((self.posX >= bullet.posX and self.posX <= bullet.posX + bullet.width)
            or (self.posX + self.width >= bullet.posX and self.posX <= bullet.posX + bullet.width))
            and ((self.posY >= bullet.posY and self.posY <= bullet.posY + bullet.height)
            or (self.posY + self.height >= bullet.posY and self.posY <= bullet.posY + bullet.height))):

            self.delete(Enemy.enemies, enemy)
            self.delete(Bullet.bullets, bullet)
            score.addScore(100)

    def draw(self, surface):
        surface.blit(self.img, self.Rect())
            
    @staticmethod
    def generate(img, size, number):
        i = 0
        while i <= number:
            i+=1
            Enemy.enemies.append(Enemy(random.randrange(size[0], 2*size[0]), random.randrange(0, size[1] - 100), 120, 80, img))

    def Boundaries(self, enemy, width):
        if self.posX < width:
            self.delete(Enemies.enemies, enemy)

    def transform(self):
        self.img = pygame.transform.scale(self.img, self.Rect().size)



"""

    Bullets class

"""
class Bullet(Entity):
    bullets = list()

    def __init__(self, posX, posY, width, height, speed = 8, path="bullet"):
        super().__init__(posX, posY, width, height, speed, path)
        self.load()

    def Boundaries(self, bullet, width):
        if self.posX > width:
            self.delete(Bullet.bullets, bullet)
       