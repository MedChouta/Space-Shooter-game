#!/usr/bin/python3

from Entities import *
from Score import *
from Menu import *
import threading, time


pygame.init()

music = pygame.mixer.music
music.load('assets/blazerRail.mp3')
music.set_volume(0.3)
music.play(-1)

musicPlaying = True

#pygame.mixer.music.set_volume(0.3)
#pygame.mixer.music.play(-1)

WIDTH = 1280
HEIGHT = 720

size = (WIDTH, HEIGHT)



enemyImg = pygame.image.load('assets/shouts.png')

pygame.display.set_icon(enemyImg)



screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shooter Galactica")

backToMenu = True

background = pygame.image.load("assets/bg.jpg").convert()

backgroundMenu = pygame.image.load("assets/background.jpg")
backgroundMenu = pygame.transform.scale(backgroundMenu, size)

backgroundMenuBlurred = pygame.image.load("assets/background_blurred.jpg")
backgroundMenuMenuBlurred = pygame.transform.scale(backgroundMenuBlurred, size)

while backToMenu:
    
    Enemy.enemies.clear()
    Bullet.bullets.clear()

    clock = pygame.time.Clock()

    carryOn = False

    cursorOffset = 0
    selectorOffset = 0


    pause = False

    menuStart = True

    selection = False

    gameOver = False

    retry = False

    character = "daoui"

    playerSelection = ["daoui", "abid", "jiji"] 
    players = list()
    pWidth = 150
    pHeight = 120

    while menuStart:

        playerOffset = 0

        moveBy = 80
        menuChoices = {1: 0, 2: moveBy, 3: moveBy*2, 4: moveBy*3}

        playerMoveBy = 200
        playerChoices = {1: 0, 2: playerMoveBy, 3: playerMoveBy*2}

        screen.blit(backgroundMenu, (0, 0))
        menu = Menu(300, HEIGHT/2,"assets/Anton.ttf", (150, 150, 150), ["PLAY", "SELECT PLAYER" , "TOGGLE MUSIC","QUIT GAME"])    
        menu.draw(screen)

        Score(WIDTH - 150, HEIGHT - 100, "Best Score: ", "assets/Anton.ttf").display(screen, scoreType=1)
        Player(300 - pWidth/2 + 20, HEIGHT/2 - pHeight - moveBy/2 + 5, 150, 120, character).draw(screen) 

        maxOffset = moveBy * len(menu.text) - moveBy # 80 being the pixel number of the selector's movement



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuStart = False
                backToMenu = False
            if event.type == pygame.KEYDOWN:
                if selection == False:
                    if event.key == pygame.K_DOWN:
                        if cursorOffset != menuChoices[4]:
                            cursorOffset += moveBy
                    elif event.key == pygame.K_UP:
                        if cursorOffset != menuChoices[1]:
                            cursorOffset -= moveBy
                    elif event.key == pygame.K_RETURN:
                        if cursorOffset == menuChoices[1]:
                            menuStart = False
                            carryOn = True
                            retry = True
                        elif cursorOffset == menuChoices[2]:
                            selection = True
                        elif cursorOffset == menuChoices[3]:
                            if musicPlaying:
                                music.pause()
                                musicPlaying = False
                            else:
                                musicPlaying = True
                                music.rewind()
                                music.unpause()
                        elif cursorOffset == menuChoices[4]: #QUIT
                            menuStart = False
                            backToMenu = False
                
                else:
                    if event.key == pygame.K_RIGHT:
                        if selectorOffset != playerChoices[3]:
                            selectorOffset += playerMoveBy
                    elif event.key == pygame.K_LEFT:
                        if selectorOffset != playerChoices[1]:
                            selectorOffset -= playerMoveBy
                    elif event.key == pygame.K_RETURN:
                        for key, value in playerChoices.items():
                            if value == selectorOffset:
                                character = playerSelection[key - 1]
                        selection = False

        menu.menuSelect(screen, cursorOffset)        

        if selection:

            screen.blit(backgroundMenuBlurred, (0, 0))

            selectorRect = pygame.draw.rect(screen, (150, 150, 150), (350 - 20 + selectorOffset, HEIGHT/2 - 20 - pHeight/2, pWidth + 40, pHeight + 40), 2)

            for player in playerSelection:
                playerObj = Player(350 + playerOffset, HEIGHT/2 - pHeight/2, 150, 120, player).draw(screen) 
                playerOffset += 200
    

        pygame.display.flip()
        

    while retry:
        player = Player(0, HEIGHT/2 - 150/2, 150, 120, character)
    
        gameOver = False
        eSpeed = 0

        numberOfEnemies = 0
        score = Score(WIDTH - 150, HEIGHT - 100, "Actual score: ", "assets/Anton.ttf")

        speedUpEvent = pygame.USEREVENT + 1        
        moreEnemiesEvent = pygame.USEREVENT + 2
        
        pygame.time.set_timer(pygame.USEREVENT, 800)
        pygame.time.set_timer(speedUpEvent, 1000)
        pygame.time.set_timer(moreEnemiesEvent, 10000)

        carryOn = True
        Enemy.enemies.clear()
        Bullet.bullets.clear()

        while carryOn:
            
            screen.blit(background, (0, 0))
            background = pygame.transform.scale(background, size)

            playerX = 0
            playerY = 0

            keys_pressed = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
                    backToMenu = False
                    retry = False
                if pause == False or gameOver == False:
                    if event.type == pygame.USEREVENT:
                        Enemy.generate(enemyImg, size, numberOfEnemies)
                    elif event.type == speedUpEvent:
                        eSpeed += 0.142857143
                    elif event.type == moreEnemiesEvent:
                        numberOfEnemies += 1
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            player.shoot()

                if event.type == pygame.KEYDOWN:
                    if pause or gameOver:
                        if event.key == pygame.K_DOWN:
                            if cursorOffset == 0:
                                cursorOffset += 80
                        elif event.key == pygame.K_UP:
                            if cursorOffset == 80:
                                cursorOffset -= 80
                        elif event.key == pygame.K_RETURN:
                            if cursorOffset == 0: #RESUME
                                if pause:
                                    pause = False
                                else:
                                    gameOver = False
                                    carryOn = False
                            else: #QUIT
                                carryOn = False
                                retry = False
                    if event.key == pygame.K_ESCAPE and gameOver == False:
                        if pause:
                            pause = False
                        else:
                            pause = True

            if pause == False and gameOver == False:
                if keys_pressed[pygame.K_LEFT]:
                    playerX -= player.speed
                elif keys_pressed[pygame.K_RIGHT]:
                    playerX += player.speed
                elif keys_pressed[pygame.K_UP]:
                    playerY -= player.speed
                elif keys_pressed[pygame.K_DOWN]:
                    playerY += player.speed

                #Enemies
            for enemy in Enemy.enemies:
                if pause == False and gameOver == False:
                    def stop():
                        global gameOver
                        gameOver = True
                        global score
                        score.saveScore()
                    enemy.move(enemy.speed - eSpeed, 0)
                    player.collision(enemy, stop)
                    try:
                        enemy.Boundaries(enemy, 0 - enemy.width)
                    except:
                        pass
                enemy.draw(screen)


                #BULLETS
            for bullet in Bullet.bullets:
                if pause == False and gameOver == False:
                    bullet.move(bullet.speed, 0)
                    bullet.draw(screen)
                bullet.Boundaries(bullet, WIDTH)
                
            #PLAYER
            player.draw(screen)
            if pause == False and gameOver == False:
                player.move(playerX, playerY)
                player.Boundaries(size)

                #Checking collision between Bullet and Enemy
            if pause == False and gameOver == False:
                for enemy in Enemy.enemies:
                    for bullet in Bullet.bullets:
                        def cleanMemory(bullet=bullet, enemy=enemy, score=score):
                            bullet.delete(Bullet.bullets, bullet)
                            enemy.delete(Enemy.enemies, enemy)
                            score.addScore(100)
                        bullet.collision(enemy, cleanMemory)
            
            if pause and gameOver == False:
                menu = Menu(WIDTH/2, HEIGHT/2,"assets/Anton.ttf", (0, 0, 0), ["RESUME", "MAIN MENU"])
                bg = pygame.Surface(size)
                bg.set_alpha(128)
                bg.fill((255, 255, 255))
                screen.blit(bg, (0, 0))
                menu.draw(screen)
                menu.menuSelect(screen, cursorOffset)        
            elif pause == False and gameOver:
                menu = Menu(WIDTH/2, HEIGHT/2,"assets/Anton.ttf", (0, 0, 0), ["RETRY", "MAIN MENU"])
                bg = pygame.Surface(size)
                bg.set_alpha(128)
                bg.fill((255, 255, 255))
                screen.blit(bg, (0, 0))
                menu.draw(screen)
                menu.menuSelect(screen, cursorOffset)
                score.posX = WIDTH/2
                score.posY = HEIGHT/1.3
                Score(WIDTH/2, HEIGHT/1.3 + 40, "Best Score: ", "assets/Anton.ttf").display(screen, scoreType=1)     
            

            score.display(screen)

            pygame.display.flip()
            
            clock.tick(60)

pygame.quit()