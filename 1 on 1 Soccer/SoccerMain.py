#Import and Initialize
import pygame, SoccerSprite
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1004,631))

def menu():
    '''This function defines the main menu for our game
    It displays the instructions and a key to start'''
    #Display
    pygame.display.set_caption("1 on 1 Soccer Menu")
    
    #Entities
    background = pygame.image.load("Background/Soccer background.png")
    screen.blit(background,(0,0))
    
    #Assign
    clock = pygame.time.Clock()
    menuGoing = True
    font = pygame.font.SysFont("Arial",30)
    pygame.mouse.set_visible(True)
    message = "Welcome to 1 on 1 Soccer. 1 on 1 soccer is a 2 Dimensional soccer game.\n Each player is allowed to move left and right, or jump. (Becareful because it takes a long time to land if you jump. Do it at your own risk). \n Player 1 moves with \" WAD\" while Player 2 uses arrow keys.\n The objective of the game is to score as many points as possible within 3 minutes in the opponents net. \n Good luck and have fun!"
    
    #Loop
    while menuGoing:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    menuGoing = False
                    
        text = font.render(message,1,(0,255,255))
        textrect = text.get_rect()
        textrect.centerx ,textrect.centery = screen.get_width()/2,screen.get_height()/2 - 200
        screen.blit(text,textrect)
                          
        pygame.display.flip()
    pygame.quit()


def main():
    '''This function defines the 'mainline logic' for our 1 on 1
    soccer game'''
    
    #Display
    pygame.display.set_caption("1 on 1 Soccer")
    
    #Entities
    background = pygame.image.load("Background/Soccer background.png")
    screen.blit(background,(0,0))
    
    #Sprites for: End Zones, Bricks, Player, and Ball
    player1 = SoccerSprite.Player(screen,1)
    player2 = SoccerSprite.Player(screen,2)
    soccer_ball = SoccerSprite.Ball(screen)
    player1_net = SoccerSprite.Net(screen,1)
    player2_net = SoccerSprite.Net(screen,2)
    goalzone1 = SoccerSprite.Goal_Zone(screen,1)
    goalzone2 = SoccerSprite.Goal_Zone(screen,2)
    scorekeeper = SoccerSprite.ScoreKeeper()
    
    #Group
    Endzone = pygame.sprite.Group(goalzone1,goalzone2)
    ballGroup = pygame.sprite.Group(soccer_ball)
    allSprites = pygame.sprite.Group(player1,player2,soccer_ball,player1_net,player2_net,goalzone1,goalzone2,scorekeeper)
    
    #Music 
    pygame.mixer.music.load("Music/BGM.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    #Sound Effects
    goalsfx = pygame.mixer.Sound ("Music/Goalsfx.wav")
    goalsfx.set_volume(0.5)
    hit = pygame.mixer.Sound ("Music/Hit.wav")
    hit.set_volume(0.4)
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True
    t =0
    font = pygame.font.SysFont("Arial", 50)
    
    pygame.mouse.set_visible(False)
    
    #Loop
    while keepGoing:
        #Time
        clock.tick(30)
        t += 1
        if t % 30 == 0:
            time = t/30
            scorekeeper.timer(time)
            
        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        #Direction Change
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player1.change_direction((-1,0),1)
        if keys[pygame.K_d]:
            player1.change_direction((1,0),1)
        if keys[pygame.K_w]:
            player1.jump(1)
        #Player 2 movements
        if keys[pygame.K_UP]:
            player2.jump(2)
        if keys [pygame.K_LEFT]:
            player2.change_direction((-1,0),2)
        if keys [pygame.K_RIGHT]:
            player2.change_direction((1,0),2)
        #Ball Collision
        if soccer_ball.rect.colliderect(player1):
            hit.play()
            soccer_ball.collisionHelper(soccer_ball,player1)
        if soccer_ball.rect.colliderect(player2):
            hit.play()
            soccer_ball.collisionHelper(soccer_ball,player2)
        #Player collsiion
        if player1.rect.colliderect(soccer_ball):
            hit.play()
            soccer_ball.collisionHelper(soccer_ball,player1)
        if player2.rect.colliderect (soccer_ball):
            hit.play()
            soccer_ball.collisionHelper(soccer_ball,player2)
        #Player Scored
        if soccer_ball.rect.colliderect(goalzone1):
            goalsfx.play()
            soccer_ball.ball_reset()
            scorekeeper.p2_scored()
        if soccer_ball.rect.colliderect(goalzone2):
            goalsfx.play()
            soccer_ball.ball_reset()
            scorekeeper.p1_scored()
        #Players collide
        if player1.rect.colliderect(player2) or player2.rect.colliderect(player1):
            player1.change_direction((0,0),1)
            player2.change_direction((0,0),2)
        
        #Winner
        if t/30 == 120:
            if scorekeeper.winner() == 1:
                text = font.render("Player 1 Wins!",1,(0,255,255))
                textrect = text.get_rect()
                textrect.centerx ,textrect.centery = screen.get_width()/2,screen.get_height()/2
                screen.blit(text,textrect)
            elif scorekeeper.winner() == 2:
                text = font.render("Player 2 Wins!",1,(0,255,255))
                textrect = text.get_rect()
                textrect.centerx ,textrect.centery = screen.get_width()/2,screen.get_height()/2
                screen.blit(text,textrect)
            else:
                text = font.render("T%si%se"%(" "*3," "*3),1,(0,255,255))
                textrect = text.get_rect()
                textrect.centerx ,textrect.centery = screen.get_width()/2,screen.get_height()/2
                screen.blit(text,textrect)
            keepGoing = True
                
        
                
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    pygame.quit()
menu()
            