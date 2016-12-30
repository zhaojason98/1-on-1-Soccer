import pygame,math
pygame.mixer.init()

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for Player 1 and Player 2'''
    def __init__(self,screen,player_num):
        '''This initializer takes the screen surface and the player number as
        parameters. It loads 2 seperate images for player 1 and player 2 along
        with different positions.'''
        
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Set Attributes
        #Player initial images
        self.__p1 = pygame.image.load("Player/Player_1.png")
        self.__p2 = pygame.image.load("Player/Player_2.png")
        #Players jump images
        self.__p1_jump = pygame.image.load("Player/Player1_Jump2.png")
        self.__p2_jump = pygame.image.load("Player/Player2_Jump.png")
        #Attributes
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
            
    def change_direction(self, xy_change,player_num):
        '''This method is called when the user presses a left or right direction
        it allows the player to move along the x axis'''
        self.rect.right += (xy_change[0] * 10)
        
        #Player 1 run animation
        if player_num == 1:
            if self.__running == self.__run_factor:
                self.__p1 = pygame.image.load("Player/Player1_running0.png")
            elif self.__running == self.__run_factor/2 :
                self.__p1 = pygame.image.load("Player/Player1_running1.png")
            self.__running += 1
            if self.__running > self.__run_factor:
                self.__running = 0
        #Player 2 run animation
        else:
            if self.__running == self.__run_factor:
                self.__p2 = pygame.image.load("Player/Player2_running0.png")
            elif self.__running == self.__run_factor/2:
                self.__p2 = pygame.image.load("Player/Player2_running1.png")
            self.__running += 1
            if self.__running > self.__run_factor:
                self.__running = 0
        
        
    def jump (self,player_num):
        '''This method is called when the user presses a jump button. It allows
        the player to go up in a negative y-direction'''
        self.rect.bottom += 2
        #Player 1 jump image
        if self.__player_num == 1:
            self.image = self.__p1_jump
        #Player 2 jump image
        else:
            self.image = self.__p2_jump
        #Change direction if max jump height is reached
        if self.rect.bottom >= self.__screen.get_height()/2+100:
            self.__change_y = -10

            
    def gravity(self):
        '''THis method is called when the user reaches a certain rate, it will slowly
        increase the y-value in a positive direction'''
        if self.__change_y == 0:
            self.__change_y = 1
        else:
            self.__change_y += .35
        #If the player going down, then cannot have a negative y value
        if self.rect.y >= self.__screen.get_height()/2+100 - self.rect.height and self.__change_y >= 0:
            self.__change_y = 0
            self.rect.y = self.__screen.get_height()/2+100 - self.rect.height
            #Resets it to run animation
            if self.__player_num == 1:
                self.image = self.__p1
            else:
                self.image = self.__p2
                
    
            
            
    def update(self):
        '''This update method checks if the player hits the left or right endzone. It also calls the
        gravity method'''
        #Cannot go off the field
        if self.rect.left < 125:
            self.rect.left = 125
        elif self.rect.right > self.__screen.get_width() - 125:
            self.rect.right = self.__screen.get_width() -125
            
        self.gravity()
        #Changes player's y location
        self.rect.y += self.__change_y
            
class Ball(pygame.sprite.Sprite):
    '''This is the ball class of the soccer game'''
    def __init__(self,screen):
        '''This initializer takes in a screen parameter. It sets the attributes for
        the ball class. Sets the balls current image, max speed and height attribute'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Set attributes
        self.image = pygame.image.load("Ball/Ball1.png")
        self.__screen = screen
        self.__change_y =0
        self.__height = .35
        self.maxspeed = 7
        self.__bounce = .25
        self.__current = 1
 
        # the ball velocity
        self.velx = 0
        #Set the ball's rect velocity
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
        self.__height = 0.35
        self.__bounce = 0.25
        self.__current = 1
        self.rect.centerx = self.__screen.get_width()/2
        self.rect.centery = self.__screen.get_height()/2- 100
        
            
    def collisionHelper(self, ball, player):
        '''This method is called when the player collides with the ball. It takes in
        the ball and player objects as parameters'''
        self.ball = ball
        speed = math.hypot(self.velx, self.__change_y)
        #X Velocity for a negative y value
        top_component = speed * .95
        #X-Velocity for a positive y value
        bottom_component = speed * 2
        # Corner collisions
        # if the ball hit the top left
        if self.ball.rect.collidepoint(player.rect.left,player.rect.top):
            if self.velx >= 0: #if the velocity is greater than 0, give it a negative x-velocity
                self.velx = -top_component
            if self.__change_y >= 0: # change y direction to go down
                self.__change_y = -top_component
            self.rect.bottom = player.rect.top -1    # move out of collision
            self.__height = .35
            self.__bounce = .25
            
        # if the ball hit the top right
        if self.ball.rect.collidepoint(player.rect.right,player.rect.top):
            if self.velx <= 0: # only change x velocity if going left
                self.velx = top_component
            if self.__change_y >= 0: # only change y velocity if going down
                self.__change_y = -top_component
            self.rect.bottom = player.rect.top -1    # move out of collision
            self.__height = .35
            self.__bounce = .25
 
        # if the ball hit the bottom left
        if self.ball.rect.collidepoint (player.rect.left,player.rect.bottom):
            if self.velx >= 0: # only change x velocity if going right
                self.velx = -bottom_component
            if self.__change_y <= 0: # only change y velocity if going up
                self.__change_y = bottom_component
            self.ball.rect.top  = player.rect.bottom + 1  # move out of collision
            self.__height = .15
            self.__bounce = .1

 
        # if the ball hit the bottom right
        if self.ball.rect.collidepoint (player.rect.left,player.rect.bottom):
            if self.velx <= 0: # only change x velocity if going left
                self.velx = bottom_component
            if self.__change_y <= 0: # only change y velocity if going up
                self.__change_y = bottom_component
            self.ball.rect.top = player.rect.bottom + 1   # move out of collision
            self.__height = .15
            self.__bounce = .1
 
        # if the ball hit the top
        if self.ball.rect.collidepoint(player.rect.centerx,player.rect.top) or player.rect.collidepoint(ball.rect.centerx,ball.rect.bottom):
            self.__change_y *= -1                        # flip y velocity
            self.ball.rect.bottom = player.rect.top - 1   # move out of collision
 
 
        # if the ball hit the left side
        if player.rect.collidepoint (self.ball.rect.left,self.ball.rect.y):
            self.velx = 7   #Gives ball a positive velocity to go right
 
        # if the ball hit the right side
        elif player.rect.collidepoint (self.ball.rect.right,self.ball.rect.y):
            self.velx = -7    #Gives ball a negative ball velocity to go left
            
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
        '''This method calls the bounce and . It checks
        to see if the ball hits the endzone or if velocity is capped'''
        self.bounce()
        self.gravity()
        #self.friction()
        self.rect.y += self.__change_y
        if self.__height > 2:
            self.rect.y = self.__screen.get_height()/2 + 100 - self.rect.height
        #Collision of endzones
        if self.rect.left <= 125 and self.rect.bottom <= 250:
            self.velx = -self.velx
        elif self.rect.right >= self.__screen.get_width()-125 and self.rect.bottom <= 250:
            self.velx = -self.velx
        #Hits roof
        if self.rect.top <= 0:
            self.__change_y = -self.__change_y
        #Sets a max speed
        if self.velx > self.maxspeed:
            self.velx = 5
        elif self.velx < -self.maxspeed:
            self.velx = -5
        #Ball animation
        if self.__current > 18:
            self.__current = 1
        elif self.__current == 0:
            self.__current = 18
        
        if self.velx > 0:
            self.__current += 1
        elif self.velx < 0:
            self.__current -= 1
        self.image =  pygame.image.load("Ball/Ball" + str(self.__current) + ".png")
            
        #update velocity
        self.rect.centerx += (self.velx * 2)
    
            
class Net(pygame.sprite.Sprite):
    '''This is the soccer net for our soccer game'''
    def __init__(self,screen,position):
        '''This initializer takes in a screen parameter and a position as a parameter'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__goal1 = pygame.image.load("Net/SoccerGoal1.png")
        self.__goal2 = pygame.image.load("Net/SoccerGoal2.png")
        self.__screen = screen
        #Player 1's net
        if position == 1:
            self.image = self.__goal2
            self.rect = self.image.get_rect()
            self.rect.bottom = self.__screen.get_height()/2 + 175
            self.rect.right = 180
        #Player 2's net
        else:
            self.image = self.__goal1
            self.rect = self.image.get_rect()
            self.rect.bottom = self.__screen.get_height()/2 + 175
            self.rect.left = self.__screen.get_width()-190
            
class Goal_Zone(pygame.sprite.Sprite):
    '''This will be the endzone to detect a soccer goal'''
    def __init__(self,screen,position):
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Sets a thin black line
        self.image = pygame.Surface((1,225))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        #Attributes
        self.__screen = screen
        
        self.rect = self.image.get_rect()
        #Player 1's goal zone
        if position ==1:
            self.rect.left = 125
            self.rect.bottom = self.__screen.get_height()/2 + 160
        #Player 2's goal zone
        else:
            self.rect.right = self.__screen.get_width()-125
            self.rect.bottom = self.__screen.get_height()/2 + 160
            
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class displays the scores of each player'''
    def __init__(self):
        '''THis initializer loads the font "Arial" and sets boths players
        starting score to 0'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.SysFont("Arial", 30)
        self.__p1score = 0
        self.__p2score = 0
        clock = pygame.time.Clock()
        self.__time = 120
        
    def p1_scored(self):
        '''This method is called when the ball collides with player 2's goal zone
        It adds a point to player 1's score'''
        self.__p1score += 1
    def p2_scored(self):
        '''This method is called when the ball collides with player 1's goal zone
        It adds a point to player 2's score'''
        self.__p2score += 1
    def timer (self,time):
        '''This method is called every second and deducts 1 second from the
        total time'''
        self.__time = 120- time
        if self.__time < 0:
            self.__time = 0
        
    def winner(self):
        '''A winner is decided when the time limit reaches 0, or 3 minutes have
        passed. The method returns 0 if there is no winner (a tie), 1 if player 1
        wins, or 2 if player 2 wins'''
        #If player 1 wins
        if self.__p1score > self.__p2score:
            return 1
        #If player 2 wins
        elif self.__p2score > self.__p1score:
            return 2
        #If tie
        else:
            return 0
        
    def update(self):
        '''This method is called to update the players score and time'''
        message = "Player 1: %d%sTime:%d%sPlayer 2: %d" %(self.__p1score," "*40,self.__time," "*40,self.__p2score)
        self.image = self.__font.render(message,1,(255,0,0))
        self.rect = self.image.get_rect()
        self.rect.left = 10
        