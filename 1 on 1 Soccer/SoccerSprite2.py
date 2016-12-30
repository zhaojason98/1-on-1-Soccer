import pygame,math

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for Player 1 and Player 2'''
    def __init__(self,screen,player_num):
        '''This initializer takes the screen surface and the player number as
        parameters. It loads 2 seperate images for player 1 and player 2 along
        with different positions.'''
        
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Set Attributes
        self.__p1 = pygame.image.load("Player_1.png")
        self.__p2 = pygame.image.load("Player_2.png")
        self.__p1_jump = pygame.image.load("Player1_Jump2.png")
        self.__screen = screen
        self.__change_y =0
        self.__player_num = player_num
        self.__running = 1
        self.__run_factor = 10

        
        #Initialize Player1
        if player_num == 1:
            self.image = self.__p1
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 200
            self.rect.left = 250
        #Initialize Player 2
        else:
            self.image = self.__p2
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 200
            self.rect.left = screen.get_width() - 250
            
    def change_direction(self, xy_change):
        '''This method is called when the user presses a left or right direction
        it allows the player to move along the x axis'''
        self.rect.right += (xy_change[0] * 10)
        
        if self.__running == self.__run_factor:
            self.__p1 = pygame.image.load("Player1_running0.png")
        elif self.__running == self.__run_factor/2 :
            self.__p1 = pygame.image.load("Player1_running1.png")
        self.__running += 1
        if self.__running > self.__run_factor:
            self.__running = 0
            
        
        
    def jump (self):
        '''This method is called when the user presses a jump button. It allows
        the player to go up in a negative y-direction'''
        self.rect.bottom += 2
        if self.__player_num == 1:
            self.image = self.__p1_jump
        else:
            self.image = self.__p2
        if self.rect.top == self.__screen.get_height() / 2:
            self.rect.bottom -= 2
 
        if self.rect.bottom >= self.__screen.get_height()/2+100:
            self.__change_y = -10
            
    def gravity(self):
        '''THis method is called when the balll reaches a certain rate, it will slowly
        increase the y-value in a positive direction'''
        if self.__change_y == 0:
            self.__change_y = 1
        else:
            self.__change_y += .35
 
        if self.rect.y >= self.__screen.get_height()/2+100 - self.rect.height and self.__change_y >= 0:
            self.__change_y = 0
            self.rect.y = self.__screen.get_height()/2+100 - self.rect.height
            if self.__player_num == 1:
                self.image = self.__p1
            else:
                self.image = self.__p2
                
    
            
            
    def update(self):
        '''This update method checks if the player hits the left or right endzone. It also calls the
        gravity method'''
        if self.rect.left < 125:
            self.rect.left = 125
        elif self.rect.right > self.__screen.get_width() - 125:
            self.rect.right = self.__screen.get_width() -125
            
        self.gravity()

        self.rect.y += self.__change_y
            
class Ball(pygame.sprite.Sprite):
    '''This is the ball class of the soccer game'''
    def __init__(self,screen):
        '''This method takes in a screen parameter'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Set attributes
        self.image = pygame.image.load("Ball.png")
        self.__screen = screen
        self.__change_y =0
        self.__height = .35
        self.maxspeed = 5
        self.__bounce = .25
 
        # the ball velocity
        self.velx = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__screen.get_width()/2
        self.rect.centery = self.__screen.get_height()/2- 100
        
    def gravity(self):
        '''This method is called in order to allow the ball to have a positive y-velocity'''
        if self.__change_y == 0:
            self.__change_y = 1
        else:
            self.__change_y += self.__height
         
        if self.rect.y >= self.__screen.get_height()/2 + 100 - self.rect.height and self.__change_y >= 0:
            self.__change_y = 0
            self.rect.y = self.__screen.get_height()/2 + 100 - self.rect.height
            self.__height += .25
            
        #self.rect.centerx += self.velx
    
    def bounce(self):
        '''This method is called when the ball hits the bottom of the screen, it allows the
        ball to go back up'''
        if self.rect.top == self.__screen.get_height() / 2: #If the ball hits the floor
            self.rect.bottom -= 2
            self.__height += self.__bounce
                    
        if self.rect.bottom >= self.__screen.get_height()/2+100:
            self.__change_y = -10
            self.__height += self.__bounce
            
    def ball_reset(self):
        self.velx = 0
        self.rect.centerx = self.__screen.get_width()/2
        self.rect.centery = self.__screen.get_height()/2- 100
        
            
    def collisionHelper(self, ball, player):
        '''This method is called when the player collides with the ball'''
        self.ball = ball
 
        # test corners first
        # if the ball hit the top left
        if self.ball.rect.collidepoint(player.rect.left,player.rect.top):
            speed = math.hypot(self.velx, self.__change_y)
            component = speed * .95 #Set the X-velocity
            if self.velx >= 0: #if the velocity is greater than 0, give it a negative x-velocity
                self.velx = -component
            if self.__change_y >= 0: # change y direction to go down
                self.__change_y = -component
            self.rect.bottom = player.rect.top -1    # move out of collision
            self.__height = .35
            self.__bounce = .25
            
        # if the ball hit the top right
        if self.ball.rect.collidepoint(player.rect.right,player.rect.top):
            speed = math.hypot(self.velx, self.__change_y)
            component = speed * .95 #Set a x-velocity
            if self.velx <= 0: # only change x velocity if going left
                self.velx = component
            if self.__change_y >= 0: # only change y velocity if going down
                self.__change_y = -component
            self.rect.bottom = player.rect.top -1    # move out of collision
            self.__height = .35
            self.__bounce = .25
 
        # if the ball hit the bottom left
        if self.ball.rect.collidepoint (player.rect.left,player.rect.bottom):
            speed = math.hypot(self.velx, self.__change_y)
            component = speed * 2 # gives the ball a 45 degree release
            if self.velx >= 0: # only change x velocity if going right
                self.velx = -component
            if self.__change_y <= 0: # only change y velocity if going up
                self.__change_y = component
            self.ball.rect.top  = player.rect.bottom + 1  # move out of collision
            self.__height = .15
            self.__bounce = .1

 
        # if the ball hit the bottom right
        if self.ball.rect.collidepoint (player.rect.left,player.rect.bottom):
            speed = math.hypot(self.velx, self.__change_y)
            component = speed * 2 #gives the ball a 45 degree release
            if self.velx <= 0: # only change x velocity if going left
                self.velx = component
            if self.__change_y <= 0: # only change y velocity if going up
                self.__change_y = component
            self.ball.rect.top = player.rect.bottom + 1   # move out of collision
            player1.jump()
            self.__height = .15
            self.__bounce = .1
 
        # if the ball hit the top edge
        if self.ball.rect.colliderect (pygame.Rect(player.rect.left,player.rect.top,player.rect.width,2)):
            self.__change_y *= -1                        # flip y velocity
            self.ball.rect.bottom = player.rect.top - 1   # move out of collision
 
        # if the ball hit the bottom edge
        #elif self.ball.rect.colliderect( pygame.Rect(player.rect.left, player.rect.bottom-2, player.rect.width, 2) ):
            #self.__change_y *= -1        #Change y velocity
            #self.ball.rect.top = player.rect.bottom + 1   # move out of collision
 
        # if the ball hit the left side
        if player.rect.collidepoint (self.ball.rect.left,self.ball.rect.y):
            self.velx = 3   #Gives ball a positive velocity to go right
 
        # if the ball hit the right side
        elif player.rect.collidepoint (self.ball.rect.right,self.ball.rect.y):
            self.velx = -3    #Gives ball a negative ball velocity to go left
            
    def friction(self):
        '''This method allows the x-velocity to decrease over time'''
        while self.velx > 0 or self.velx < 0 and self.rect.bottom == self.__screen.get_height()/2:
            if self.velx >0:
                self.velx -= 0.5
            elif self.velx < 0:
                self.velx += 0.5
            if self.velx <= 0.1 and self.velx > 0:
                self.velx = 0
            elif self.velx <= -0.1 and self.velx<0:
                self.velx = 0
            

    def update(self):
        '''This method calls the bounce,gravity, and friction method. It checks
        to see if the ball hits the endzone or if velocity is capped'''
        self.bounce()
        self.gravity()
        #self.friction()
        self.rect.y += self.__change_y
        if self.__height > 2:
            self.rect.y = self.__screen.get_height()/2 + 100 - self.rect.height
        #Collision of endzones
        if self.rect.left <= 125 and self.rect.bottom <= 225:
            self.velx = -self.velx
        elif self.rect.right >= self.__screen.get_width()-125 and self.rect.bottom <= 225:
            self.velx = -self.velx
        #Sets a max speed
        if self.velx > self.maxspeed:
            self.velx = 5
        elif self.velx < -self.maxspeed:
            self.velx = -5            
        
        self.rect.centerx += (self.velx * 2)
        speed = math.hypot(self.velx, self.__change_y)
    
            
class Net(pygame.sprite.Sprite):
    '''This is the soccer net for our soccer game'''
    def __init__(self,screen,position):
        '''This initializer takes in a screen parameter and a position as a parameter'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__goal1 = pygame.image.load("SoccerGoal1.png")
        self.__goal2 = pygame.image.load("SoccerGoal2.png")
        self.__screen = screen
        
        if position == 1:
            self.image = self.__goal2
            self.rect = self.image.get_rect()
            self.rect.bottom = self.__screen.get_height()/2 + 175
            self.rect.right = 180
        else:
            self.image = self.__goal1
            self.rect = self.image.get_rect()
            self.rect.bottom = self.__screen.get_height()/2 + 175
            self.rect.left = self.__screen.get_width()-190
            
class Goal_Zone(pygame.sprite.Sprite):
    '''This will be the endzone to detect a soccer goal'''
    def __init__(self,screen,position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((1,250))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        self.__screen = screen
        
        self.rect = self.image.get_rect()
        if position ==1:
            self.rect.left = 125
            self.rect.bottom = self.__screen.get_height()/2 + 160
        else:
            self.rect.right = self.__screen.get_width()-125
            self.rect.bottom = self.__screen.get_height()/2 + 160
            
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class displays the scores of each player'''
    def __init__(self):
        '''THis initializer loads the font "Arial" and sets boths players
        starting score to 0'''
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__p1score = 0
        self.__p2score = 0
        
    def p1_scored(self):
        self.__p1score += 1
    def p2_scored(self):
        self.__p2score += 1
        
    def update(self):
        message = "Player 1: %d                                                                                                 Player 2: %d" %(self.__p1score,self.__p2score)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left = 10
        