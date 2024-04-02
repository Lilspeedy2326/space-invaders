import pygame #bring in module o handle graphics, input, etc
import random
import time
pygame.init() #set up pygame
pygame.display.set_caption("space invaders!") #sets the window title
gamescreen = pygame.display.set_mode((800, 800)) #creates game screen
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop
lives = 3
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('LIVES:', False, (255, 0, 0))

class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
        
    def move(self, xpos, ypos):
        if self.isAlive == True: #only shoot live bullets
            self.ypos-=5 #move up when shot
        if self.ypos < 0: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = xpos #reset to player position
            self.ypos = ypos
            
    def draw(self):
        pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
        
#instantiate bullet object

class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
    def move(self, time):
        
        #reset what direction you're moving every 8 moves:
        if time % 800==0:
            self.ypos += 100 #move down
            self.direction *=-1 #flip direction
            return 0 #resets timer to 0
        
        #move every time the timer increases by 100:
        if time % 100 == 0:
            self.xpos+=50*self.direction #move right
            
        return time #doesn't reset if first if statement hasn't executed!

    def collide(self, BulletX, BulletY):
        if self.isAlive: #only hit live aliens
            if BulletX > self.xpos: #check if bullet is right of the left side of the alien
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check f the bullet is aove the alien's bottom
                        if BulletY > self.ypos: #check if the byllet is below the top of the alien
                            print("hit!") #for testing
                            self.isAlive = False #set the alien to dead
                            return False #set the BULLET to dead
                        
        return True #otherwise keep bullet alive
class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHit = 0
        
    def draw(self):
        if self.numHit ==0:
            pygame.draw.rect(gamescreen, (34, 139, 34), (self.xpos, self.ypos, 30, 30))
        if self.numHit ==1:
            pygame.draw.rect(gamescreen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))
        if self.numHit ==2:
            pygame.draw.rect(gamescreen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
            
    def collide(self, BulletX, BulletY):
        if self.numHit < 3: #only hit live aliens
            if BulletX > self.xpos: #check if bullet is right of the left side of the alien
                if BulletX < self.xpos + 40: #check if the bullet is left of the right side
                    if BulletY < self.ypos + 40: #check f the bullet is aove the alien's bottom
                        if BulletY > self.ypos: #check if the byllet is below the top of the alien
                            print("hit!") #for testing
                            self.numHit += 1 #set the alien to dead
                            return False #set the BULLET to dead
                        
        return True #otherwise keep bullet alive
class missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
        
    def move(self):
        if self.isAlive == True: #only shoot live bullets
            self.ypos+=5 #move up when shot
        if self.ypos > 800: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = -10 #reset to player position
            self.ypos = -10
            
    def draw(self):
        pygame.draw.rect(gamescreen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
                  
armada = [] #create empty list
for i in range (4): #handles rows
    for j in range (9): #handles columns
        armada.append(Alien(j*60+50, i*50+50)) #push Alien objects into list
        
walls = [] #create empty list
for k in range (4): #creates 4 sets
    for i in range (2): #handles rows
        for j in range (3): #handles columns
            walls.append(Wall(j*30+200*k+50, i*30+600)) #push wall objects into list 
missiles = []
for i in range (10):
    missiles.append(missile())
#player variables
xpos = 400
ypos = 750
moveLeft = False
moveRight = False
timer = 0;
shoot = False
bullet = Bullet(xpos+28, ypos)#create bullet object and pass player position

while not gameover: #GAME LOOP#########################################################################################
    clock.tick(60) #FPS
    timer += 1
    #Input Section-----------------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True #quit game if x is pressed int op corner
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_SPACE:
                shoot = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_SPACE:
                shoot = False

    # physics section--------------------------------------------------------------------------------------------------
    
    for i in range (len(armada)):
        timer = armada[i].move(timer)
        
    #shoot bullet
    if shoot == True: #check keyboard input
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos) #shoot from player position
        if bullet.isAlive == True:
        #check for collision between bullet and enemy
            for i in range (len(armada)): #check bullet with entire armada's position
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos) #if we hit, set bullet to false
                if bullet.isAlive == False:
                    break
                
    for i in range(len(walls)): #check each wall box
        for j in range(len(missiles)): #against each missile
            if missiles[j].isAlive == True: #check if missile is true
                if walls[i].collide(missiles[j].xpos, missiles[j].ypos) == False: #call wall collision for each combo
                    missiles[j].isAlive = False #kill missile
                    print("missile kill")
                    break #stop killing walls if you're dead!
                
    #2% chance every game loop that a missile will drop from a random alien
    for i in range (len(missiles)):
        missiles[i].move()
    chance = random.randrange(100)
    if chance < 2:
        
        #print("missile drop!") #for testing
        pick = random.randrange(len(armada))#pick a random alien from the armada
        if armada[pick].isAlive == True: #only drop from live aliens
            for i in range(len(missiles)): #find the first live missile to move
                if missiles[i].isAlive == False: #only fire missiles that aren't already gpomg
                    missiles[i].isAlive = True #set is to alive
                    missiles[i].xpos = armada[pick].xpos+5#set the missile's postiton to the aliens's position
                    missiles[i].ypos = armada[pick].ypos
                    break 
    #shoot walls   
    if bullet.isAlive == True:
    #check for collision between bullet and enemy
        for i in range (len(walls)): #check bullet with entire list of wall positions
            bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos) #if we hit, set bullet to false
            if bullet.isAlive == False:
                break
        
    else: #make bullet follow player when not moving up
        bullet.xpos = xpos + 28
        bullet.ypos = ypos
        
    
        
    
    # check varables from the input section
    if moveLeft == True:
        vx =- 3
    elif moveRight == True:
        vx = 3
    else:
        vx = 0
        
    for i in range (len(missiles)): #check for collision with each missile in list
        if missiles[i].isAlive: #only get hit by live missiles
            if missiles[i].xpos > xpos: #check of missiles is right of the left side of the player
                if missiles[i].xpos < xpos + 60: #check if the missile is left of the right side
                    if missiles[i].ypos < ypos + 40: #check if the missile is above the the players's bottom
                        if missiles[i].ypos > ypos: #check if the missile is below the top of the player
                            lives -= 1
                            time.sleep(1)
                            xpos = 400
                            ypos = 750
                            print("player hit!") #for testing
        
    #update player position
    xpos += vx
    if lives <= 0:
        gameover = True
    # RENDER Section---------------------------------------------------------------------------------------------------
    
    gamescreen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    pygame.draw.rect(gamescreen, (34, 139, 34), (xpos, 750, 60, 20)) #draw player
    pygame.draw.rect(gamescreen, (34, 139, 34), (xpos+5, 745, 50, 10)) #draw player
    pygame.draw.rect(gamescreen, (34, 139, 34), (xpos+20, 736, 20, 10)) #draw player
    pygame.draw.rect(gamescreen, (34, 139, 34), (xpos+27, 730, 5, 10)) #draw player
    
    #draw all aliens in list
    for i in range (len(armada)):
        armada[i].draw()
    for i in range (len(walls)):
        walls[i].draw()
    for i in range (len(missiles)):
        missiles[i].draw()
    if bullet.isAlive == True:
        bullet.draw()
        
    gamescreen.blit(text_surface, (0,0))
    
    
    pygame.display.flip()#this flips the buffer (memory) where stuff has been "drawn" to the actual screen
    
#end game loop##########################################################################################################
    
pygame.quit()
