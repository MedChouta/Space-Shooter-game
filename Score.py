import pygame

class Score:

    score = 0

    def __init__(self, posX, posY, text, font, score=0, color=(0, 0, 0)):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.font = font
        self.color = color
        self.score = score

    def addScore(self, points):
        self.score += points
        Score.score = self.score

    def display(self, surface, scoreType=None):
        
        score2show = 0

        if not scoreType:
            score2show = self.score
        else:
            score2show = self.bestScore()

        score = pygame.font.Font(self.font, 32)
        score = score.render(self.text + str(score2show), True, self.color)

        scoreRect = score.get_rect()
        scoreRect.center = (self.posX, self.posY)
        
        surface.blit(score, scoreRect)

    def saveScore(self):
        with open("Score", "a+") as scoreFile:
            scoreFile.seek(0, 0)
            score = scoreFile.readline()
            if score == "":
                scoreFile.write(str(Score.score))
            elif int(score) < self.score:
                scoreFile.seek(0, 0)
                scoreFile.truncate(0)
                scoreFile.write(str(Score.score)) 
    def bestScore(self):
        best = 0

        with open("Score", "a+") as scoreFile:
            scoreFile.seek(0, 0)
            score = scoreFile.readline()
            if score == "":
                return best
            else:
                best = score

        return best
