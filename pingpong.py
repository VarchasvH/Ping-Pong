import pygame, sys, random

def ball_animation():
    global ball_speed_y, ball_speed_x, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
        
    if ball.left <= 0 :
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
        
    if ball.right >= WIDTH:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1
        
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)# Makes Sure that the collision occurs only when speed of ball is +ve
        if abs(ball.right - player.left) < 10:           # Makes sure that ball only bounces of the left side of the Paddle
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
            ball_speed_x *= -1
        elif abs(ball. top - player.bottom) < 10 and ball_speed_y > 10:
             ball_speed_x *= -1                             
        
    if ball.colliderect(opponent) and ball_speed_x < 0:    # Makes Sure that the collision occurs only when speed of ball is -ve
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:          # Makes sure that ball only bounces of the right side of the Paddle
            ball_speed_x *= -1                   
        elif abs(ball. top - opponent.bottom) < 10 and ball_speed_y > 10:
            ball_speed_x *= -1                             
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_x *= -1                             

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT

def opponent_ai():
    if opponent.centery < ball.y:
        opponent.y += opponent_speed
    if opponent.centery > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT

def ball_restart():
    global ball_speed_y, ball_speed_x, current_time, score_time, number_three, number_two, number_one
    
    current_time = pygame.time.get_ticks()
    ball.center = (WIDTH/2, HEIGHT/2)
    
    
    if current_time - score_time < 700:
        number_three = game_font.render( "3", False, cyan)
        screen.blit(number_three, (WIDTH/2 - 10, HEIGHT/2 +20))
    
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render( "2", False, cyan)
        screen.blit(number_two, (WIDTH/2 - 10, HEIGHT/2 +20))
        
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render( "1", False, cyan)
        screen.blit(number_one, (WIDTH/2 - 10, HEIGHT/2 +20))
        
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0

    else:
        ball_speed_y = 8 * random.choice((1, -1))
        ball_speed_x = 8 *  random.choice((1, -1))
        score_time = None
    
def display_score():
    player_text = game_font.render(f"{player_score}", False, cyan)
    screen.blit(player_text, (WIDTH/2 + 10, 0))
    opponent_text = game_font.render(f"{opponent_score}", False, cyan)
    screen.blit(opponent_text, (WIDTH/2 - 28, 0))

pygame.mixer.pre_init(44100, -16, 2, 512)           # making sure there is no lag in sound
pygame.init()                                       # Initialzing Pygame
clock = pygame.time.Clock()

#CONSTANTS
WIDTH = 1080
HEIGHT = 720
BALL_WIDTH = 18
BALL_HEIGHT = 18
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 140

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Displaying the Screen
pygame.display.set_caption('PING PONG')

BG_COLOR = pygame.Color('black')        #COLORS
cyan = (0, 255, 255)

player_score = 0            #TEXT FILES
opponent_score = 0
game_font = pygame.font.Font("Playguard.otf", 32)
score_time = None 

#Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(WIDTH/2 - 2, 0 , 4, HEIGHT)

#Speeds
ball_speed_x = 8 * random.choice((1, -1))
ball_speed_y = 8 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Game Rectangles
ball = pygame.Rect(WIDTH/2 - BALL_WIDTH/2, HEIGHT/2 - BALL_HEIGHT/2, BALL_WIDTH, BALL_HEIGHT)
player = pygame.Rect(WIDTH - 20, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(10, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)


# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        #To Quit the Game
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:     #To Move the player
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

        if event.type == pygame.KEYUP:     
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7


    ball_animation() 
    player_animation()
    opponent_ai()
    
    #Visuals
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, cyan, player)
    pygame.draw.rect(screen, cyan, opponent)
    pygame.draw.ellipse(screen, cyan, ball)
    pygame.draw.aaline(screen, cyan, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    
    if score_time:
        ball_restart()
        
    display_score()
            
    pygame.display.flip()
    clock.tick(60)