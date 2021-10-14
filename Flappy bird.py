import pygame, sys, random
from pygame.locals import*

pygame.init()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

#Xác định FPS:
FPS = 60
fpsClock = pygame.time.Clock()

running = True

screen_width, screen_height = 400, 600
Display_Suf = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
BACKGROUND = pygame.image.load('img/background.jpg')

BIRDIMG = pygame.image.load('img/bird1.png')
bird_width, bird_height = 60, 40
G = 0.5
bird_speed = -8

# Column:
COLUMNWIDTH = 60
COLUMNHEIGHT = 550
BLANK = 160
DISTANCE = 200
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('img/column.png')

class Column:
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.lst = []
        for i in range(3):
            x =  screen_width + i * self.distance
            y = random.randrange(60, screen_height - self.blank - 60, 20)
            self.lst.append([x,y])
    
    def draw(self):
        for i in range(3):
            Display_Suf.blit(self.surface, (self.lst[i][0], self.lst[i][1] - self.height))
            Display_Suf.blit(self.surface, (self.lst[i][0], self.lst[i][1] + self.blank))
    def update(self):
        for i in range(3):
            self.lst[i][0] -= self.speed
        if self.lst[0][0] < -self.width:
            self.lst.pop(0)
            x = self.lst[1][0] + self.distance
            y = random.randrange(60, screen_height - self.blank - 60, 10)
            self.lst.append([x, y])
 
class Bird:
    def __init__(self):
        self.width = bird_width
        self.height = bird_height
        self.x = (screen_width - self.width)/2
        self.y = (screen_height- self.height)/2
        self.surface = BIRDIMG
        self.speed = 0
    
    def draw(self):
        Display_Suf.blit(self.surface, (int(self.x), int(self.y)))

    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = bird_speed

class Score:
    def __init__(self):
        self.score = 0
        self.addScore = True
    
    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSuface.get_size()
        Display_Suf.blit(scoreSuface, (int((screen_width - textSize[0])/2), 100))

    def update(self, bird, columns):
        collision = False
        for i in  range(3):
            rectColumn = [columns.lst[i][0] + columns.width, columns.lst[i][1], 1, columns.blank]
            rectBird = [bird.x, bird.y, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(bird, columns):
    for i in range(3):
        rectbird = [bird.x, bird.y, bird.width, bird.height]
        rectColumn1 = [columns.lst[i][0], columns.lst[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.lst[i][0], columns.lst[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectbird, rectColumn1) == True or rectCollision(rectbird,rectColumn2) == True:
            return True
        return False

def gamePlay(bird, columns, score):
    bird.__init__()
    bird.speed = bird_speed
    columns.__init__()
    score.__init__()
    while True:
        mouseClick = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True
    
        Display_Suf.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        bird.draw()
        bird.update(mouseClick)
        score.draw()
        score.update(bird, columns)

        if isGameOver(bird, columns) == True:
            return

        pygame.display.update()
        fpsClock.tick(FPS)

def gameStart(bird):
    bird.__init__()
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('FLAPPY BIRD', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Click to start', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                return

        Display_Suf.blit(BACKGROUND, (0, 0))
        bird.draw()
        Display_Suf.blit(headingSuface, (int((screen_width - headingSize[0])/2), 100))
        Display_Suf.blit(commentSuface, (int((screen_width - commentSize[0])/2), 500))

        pygame.display.update()
        fpsClock.tick(FPS)

def gameOver(bird, columns, score):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    commentSize = commentSuface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
    scoreSize = scoreSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    return
        
        Display_Suf.blit(BACKGROUND, (0, 0))
        columns.draw()
        bird.draw()
        Display_Suf.blit(headingSuface, (int((screen_width - headingSize[0])/2), 100))
        Display_Suf.blit(commentSuface, (int((screen_width - commentSize[0])/2), 500))
        Display_Suf.blit(scoreSuface, (int((screen_width - scoreSize[0])/2), 160))

        pygame.display.update()
        fpsClock.tick(FPS)
def main():
    bird = Bird()
    columns = Column()
    score = Score()
    while running:
        gameStart(bird)
        gamePlay(bird, columns, score)
        gameOver(bird, columns, score)
if __name__ == "__main__":
    main()