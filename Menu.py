import pygame

class Menu:
    def __init__(self, posX, posY, font, color, text, yOffset=0,width=260, height=70):
        self.posX = posX
        self.posY = posY
        self.text = text
        self.font = font
        self.color = color
        self.width = width
        self.height = height
        self.yOffset = yOffset

    def draw(self, surface):
        if self.text != None:
            for text in self.text:
                pygame.draw.rect(surface, self.color, (self.posX - int(self.width/2), self.posY + self.yOffset - int(self.height/2), self.width, self.height), 2)
                menuText = pygame.font.Font(self.font, 32)
                menuText = menuText.render(str(text), True, self.color)
                menuTextRect = menuText.get_rect()
                menuTextRect.center = (self.posX, self.posY + self.yOffset)            

                self.yOffset += 80

                surface.blit(menuText, menuTextRect) 


    def menuSelect(self, surface, offset):        
        selectSurface = pygame.Surface((self.width, self.height))
        selectSurface.set_alpha(128)
        selectSurface.fill((0, 0, 0))
        
        surface.blit(selectSurface, (self.posX - int(self.width/2), self.posY + offset - int(self.height/2)))
