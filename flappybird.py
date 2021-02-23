
import pygame
import random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-300 ))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collides_between_pipe_and_bird(pipes):
    for pipe in pipes :
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:# check <> in the code because its important
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 4,1)#it will scale and rotate the bird
    return new_bird

def animation_bird():
    new_bird = bird_wing_moves[index_bird]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(0,0,0)) # the values in the bracket are RGB colors
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render("SCORE : {} ".format(int(score)), True, (0, 0, 0)) # the values in the bracket are RGB colors
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("HIGH SCORE : {} ".format(int(high_score)), True, (0, 0, 0))  # the values in the bracket are RGB colors
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_scores(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()  # initiates pygame
screen = pygame.display.set_mode((576, 1024))  # we have to create display canvas
clock = pygame.time.Clock()  # sets the number of frames
game_font = pygame.font.Font('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/04B_19.TTF',50)

#THE VARIABLES WHICH WILL BE IMPLEMENTED IN THE GAME
gravity = 0.50
bird_movement = 0
active_game = True
score = 0
high_score = 0

# background surface
bg_surface = pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/background-night.png').convert()  # it will covert into file
bg_surface = pygame.transform.scale2x(bg_surface)  # it will fill up the screen with the dimentions we provide in screen

# floor surface
floor_surface = pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0  # for animation we can move the surface

#bird wings animation
bird_downwing = pygame.transform.scale2x(pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/bluebird-downflap.png').convert_alpha())
bird_midwing = pygame.transform.scale2x(pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha())
bird_upwing = pygame.transform.scale2x(pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha())
index_bird = 0
bird_wing_moves = [bird_downwing,bird_midwing,bird_upwing]
bird_surface = bird_wing_moves[index_bird]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRDWING = pygame.USEREVENT
pygame.time.set_timer(BIRDWING,200)

# bird surface, we can use this in the game but it will not have an animation of the wings
#bird_surface = pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/redbird-midflap.png').convert()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center=(100, 512))

#pipes
pipe_surface = pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/pipe-red.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

#cover
game_title_surface = pygame.transform.scale2x(pygame.image.load('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha())
game_title_rect = game_title_surface.get_rect(center =(288,512))

#sound
flap_sound = pygame.mixer.Sound('/Users/aditya/PycharmProjects/pythonProject/aditya/com/flappy-bird-assets-master/audio/hit.wav')

while True:
    for event in pygame.event.get():  # it gives us every event happening in pygame
        if event.type == pygame.QUIT:
            pygame.quit()  # the logic should be inside the init() and quit()
            SystemExit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and active_game:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and active_game == False:
                active_game = True
                pipe_list[:] = []
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDWING:
            if index_bird < 2:
                index_bird +=1
            else:
                index_bird = 0

            bird_surface,bird_rect = animation_bird()

    screen.blit(bg_surface, (0, 0))  # we will always change the surface from top left and set it anywhere on the screen as a position

    if active_game:

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        #birds
        bird_movement += gravity
        rotation_bird = rotate_bird(bird_surface)#rotation of the bird
        bird_rect.centery += bird_movement
        screen.blit(rotation_bird, bird_rect)
        active_game = check_collides_between_pipe_and_bird(pipe_list)
        #score
        score += 0.01 #if we give 1 score will increase fast
        score_display('main_game')
    else:
        screen.blit(game_title_surface,game_title_rect)
        high_score = update_scores(score,high_score)
        score_display('game_over')

    floor_x_pos -= 1  # to move the surface we can use the position
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # we can set the number of frames per second
