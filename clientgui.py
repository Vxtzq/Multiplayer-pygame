import sys
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
run = False
fpsClock = pygame.time.Clock()
xtosend,ytosend = 69,0
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

class Player():
    def __init__(self,x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        self.rect = Rect(self.x,self.y,40,40)
        pygame.draw.rect(screen, (255,255,0), self.rect)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5
    def update(self):
        self.move()
        self.draw()
            
player = Player(0,0)
# Game loop.
def run():
    screen.fill((0, 0, 0))
    xtosend,ytosend = player.x, player.y
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    # Update.
    player.update()
    
    
    
    # Draw.
    
    pygame.display.flip()
    fpsClock.tick(fps)
    return xtosend,ytosend