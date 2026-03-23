#Imports modules
#============================================================================
import pygame
import random
#============================================================================


#Intializes
#============================================================================
pygame.init()
pygame.font.init()
#============================================================================


#Imports player's images
#============================================================================
Up_Snake_Head = pygame.image.load('Images/Up_Snake_Head.png')
Up_Snake_Tail = pygame.image.load('Images/Up_Snake_Tail.png')
Left_Snake_Head = pygame.image.load('Images/Left_Snake_Head.png')
Left_Snake_Tail = pygame.image.load('Images/Left_Snake_Tail.png')
Right_Snake_Head = pygame.image.load('Images/Right_Snake_Head.png')
Right_Snake_Tail = pygame.image.load('Images/Right_Snake_Tail.png')
Down_Snake_Tail = pygame.image.load('Images/Down_Snake_Tail.png')
Down_Snake_Head = pygame.image.load('Images/Down_Snake_Head.png')
Y_Snake_Body = pygame.image.load('Images/Y_Snake_Body.png')
X_Snake_Body = pygame.image.load('Images/X_Snake_Body.png')
Left_Round = pygame.image.load('Images/Left_Round.png')
#============================================================================


#Imports Apple's Images
#============================================================================
Apple_Image = pygame.image.load('Images/Apple_Image.png')
#============================================================================


#Sets window
#============================================================================
WIDTH = 500
HEIGHT= 500
CELL_SIZE = 25
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mygame')
#============================================================================


#Sets Apple
#============================================================================
Apples = []
Apple_spawn_x = random.randrange(100, 400, CELL_SIZE)
Apple_spawn_y = random.randrange(100, 400, CELL_SIZE)
Apples.append(pygame.Rect(Apple_spawn_x, Apple_spawn_y, CELL_SIZE, CELL_SIZE))
#============================================================================


#Sets Player
#============================================================================
Player_Part = []
Player=pygame.Rect(WIDTH/2, HEIGHT-100, CELL_SIZE, CELL_SIZE)
Player_Tail=pygame.Rect(WIDTH/2, HEIGHT-125, CELL_SIZE, CELL_SIZE)
Player_Part.append(Player)
Player_Part.append(Player_Tail)
#============================================================================


#Saves score
#============================================================================
def Save(High_Score):

    with open('Score_Data.txt', 'w', encoding='utf-8') as f:
        f.write(str(High_Score))
#============================================================================


#Loads score
#============================================================================
def load():
    try:
        with open('Score_Data.txt', 'r', encoding='utf-8') as f:
            return int(f.read())
    except:
        return 0
#============================================================================


#Defines formate and blits text on the screen
#============================================================================
font = pygame.font.Font('Silkscreen-Regular.ttf', 30)

highscore_font = pygame.font.Font('Silkscreen-Regular.ttf', 15)
Score = 0
Highest_Score = load()

def score_board(score):

    return font.render(score, True, (0, 0, 0))


def high_score_board(highscore):

    return highscore_font.render(highscore, True, (218,196,0))
#============================================================================


#Defines game mechanics
#============================================================================
Direction = 'up'
clock = pygame.time.Clock()
running = True
#============================================================================

#Main game loop
#============================================================================
while running:

    window.fill((70, 137, 57))
    clock.tick(10)
    moved = False


    #Stores old position
    #============================================================================
    old_pos = []
    for p in Player_Part:
        old_pos.append((p.x, p.y))
    #============================================================================


    #QUIT
    #============================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #============================================================================


    #Player Direction
    #============================================================================
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        Direction='up'
    if keys[pygame.K_s] :
        Direction = 'down'
    if keys[pygame.K_a]:
        Direction = 'left'
    if keys[pygame.K_d]:
        Direction = 'right'
    #============================================================================


    #Player Movement
    #============================================================================
    if Direction == 'up':
        Player.y += -CELL_SIZE
        moved=True
    if Direction == 'down':
        Player.y += CELL_SIZE
        moved = True
    if Direction == 'left':
        Player.x += -CELL_SIZE
        moved = True
    if Direction=='right':
        Player.x += CELL_SIZE
        moved = True
    #============================================================================


    #If player is out of boundary death
    #============================================================================
    if Player.x >= WIDTH or Player.x <= 0 or Player.y >= HEIGHT or Player.y <= 0:
        running=False
    #============================================================================
    

    #Players Parts movement
    #============================================================================
    if moved:
        for i in range(1, len(Player_Part)):
            Player_Part[i].x = old_pos[i-1][0]
            Player_Part[i].y = old_pos[i-1][1]
    #============================================================================


    #If Player collides with its parts death
    #============================================================================
    for p in Player_Part[1:]:   
        if Player.colliderect(p):
            running=False
    #============================================================================


    #If player collides with apples
    #============================================================================
    for Apple in Apples[:]:
        if Player.colliderect(Apple):
            Apples.remove(Apple)

            Apple_spawn_x = random.randrange(25, 475, 25)
            Apple_spawn_y = random.randrange(50, 475, 25)

            if Apple_spawn_x == old_pos:
                Apple_spawn_x = old_pos[0][0]+25

            if Apple_spawn_y == old_pos:
                Apple_spawn_y = old_pos[0][1]+25
                
            Apples.append(pygame.Rect(Apple_spawn_x, Apple_spawn_y, 25, 25))

            last_pos = old_pos[-1]
            Player_Part.append(pygame.Rect(last_pos[0],last_pos[1], 25, 25 ))
            Score += 1
            if Score >= load():
                Save(Score)
        
    if Score >= load():
        Highest_Score = Score
    #============================================================================


    #Draws everything on the window
    #============================================================================

    #Defines apples
    #============================================================================
    for Apple in Apples[:]:
        window.blit(Apple_Image, (Apple.x, Apple.y))
    #============================================================================

    #Defines Head's movement
    #============================================================================
    if Direction == 'down':
        window.blit(Down_Snake_Head, (Player.x, Player.y))
    elif Direction == 'left':
        window.blit(Left_Snake_Head, (Player.x, Player.y))
    elif Direction == 'right':
        window.blit(Right_Snake_Head, (Player.x, Player.y))
    elif Direction == 'up':
        window.blit(Up_Snake_Head, (Player.x, Player.y))
    #============================================================================
        

    #Defines body movement
    #============================================================================

    #Defines corner itself
    #============================================================================
    for i, part in enumerate(Player_Part[1:-1], start=1):
        prev_body = Player_Part[i-1]
        curr_body = Player_Part[i]
        next_body = Player_Part[i+1]

        dx = next_body.x - prev_body.x
        dy = next_body.y - prev_body.y

        dx_prev = prev_body.x - curr_body.x
        dy_prev = prev_body.y - curr_body.y

        dx_next = next_body.x - curr_body.x
        dy_next = next_body.y - curr_body.y

        #Defines cases of corners
        #============================================================================
        if dx != 0 and dy != 0:

            #Defines left sided corners
            #============================================================================
            if dy_prev == CELL_SIZE and dx_next == CELL_SIZE: #Down
                rotated_image = pygame.transform.rotate(Left_Round, 90)
                window.blit(rotated_image, (part.x, part.y))
            elif dx_prev == -CELL_SIZE and dy_next == CELL_SIZE: #Left
                rotated_image = pygame.transform.rotate(Left_Round, 360) 
                window.blit(rotated_image, (part.x, part.y))
            elif dx_prev == CELL_SIZE and dy_next == -CELL_SIZE: #Right
                rotated_image = pygame.transform.rotate(Left_Round, 180)
                window.blit(rotated_image, (part.x, part.y))
            elif dy_prev == -CELL_SIZE and dx_next == -CELL_SIZE: #Up
                rotated_image = pygame.transform.rotate(Left_Round, 270)
                window.blit(rotated_image, (part.x, part.y))
            #============================================================================

            #Defines right sided corners
            #============================================================================
            elif dy_prev == -CELL_SIZE and dx_next == CELL_SIZE: #Up
                rotated_image = pygame.transform.rotate(Left_Round, 180)
                window.blit(rotated_image, (part.x, part.y))
            elif dx_prev == -CELL_SIZE and dy_next == -CELL_SIZE: #Left
                rotated_image = pygame.transform.rotate(Left_Round, 270)
                window.blit(rotated_image, (part.x, part.y))
            elif dy_prev == CELL_SIZE and dx_next == -CELL_SIZE: #Down
                rotated_image = pygame.transform.rotate(Left_Round, 360)
                window.blit(rotated_image, (part.x, part.y))
            elif dx_prev == CELL_SIZE and dy_next == CELL_SIZE: #Right
                rotated_image = pygame.transform.rotate(Left_Round, 90)
                window.blit(rotated_image, (part.x, part.y))
            #============================================================================

        #============================================================================

        elif dx != 0:
            window.blit(X_Snake_Body, (part.x, part.y))
        elif dy != 0:
            window.blit(Y_Snake_Body, (part.x, part.y))
    #============================================================================
    #============================================================================

    #Defines Tail's movement
    #============================================================================
    tail = Player_Part[-1]
    before_tail = Player_Part[-2]
    dx = before_tail.x-tail.x
    dy = before_tail.y-tail.y
    if dx == -CELL_SIZE:
        window.blit(Left_Snake_Tail, (tail.x, tail.y))
    elif dx == CELL_SIZE:
        window.blit(Right_Snake_Tail, (tail.x, tail.y))
    elif dy == CELL_SIZE:
        window.blit(Down_Snake_Tail, (tail.x, tail.y))
    elif dy == -CELL_SIZE:
        window.blit(Up_Snake_Tail,(tail.x, tail.y))
    #============================================================================


    #Displays updated score
    #============================================================================
    Score_Text = score_board(f'Score: {Score}')
    High_Score_Text = high_score_board(f'High-Score: {Highest_Score}')

    window.blit(Score_Text, (10, 10))
    window.blit(High_Score_Text, (10, 45))
    #============================================================================

    pygame.display.flip()

pygame.quit()
#============================================================================