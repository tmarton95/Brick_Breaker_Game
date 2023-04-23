import pygame
import math
import csv
import os
pygame.init()
pygame.font.init()

# Window setup: ================================
WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
FPS = 60
TARGET_LENGTH = 100
TARGET_PRECISION = 200
SHIFT_Y = 50
BORDER_LEFT = pygame.Rect(0, 0, 2, HEIGHT)
BORDER_RIGHT = pygame.Rect(WIDTH, 0, 2, HEIGHT)
BORDER_TOP = pygame.Rect(0, 0, WIDTH, SHIFT_Y)

# Object settings: ============================
# Slider:
SLIDER = pygame.image.load(os.path.join("images", "slider.png"))
SLIDER_LENGTH, SLIDER_HEIGHT = 80, 20
VEL_SLIDER = 6

# Block:
BLOCK_WIDTH, BLOCK_HEIGHT = 25, 25
BLOCK = pygame.image.load(os.path.join("images", "brick_1.png"))
BLOCK = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "brick_1.png")), (BLOCK_WIDTH, BLOCK_HEIGHT))
BLOCK_ROW = 8
HEIGHT_0 = 100

# Ball:
BALL_WIDTH, BALL_HEIGHT = 15, 15
BALL = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "ball.png")), (BALL_WIDTH, BALL_HEIGHT))
# Magnitude of Ball velocity:
VEL_BALL = 3.5

# Colors: =================================
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
DARKGREY = (70, 70, 70)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE = (0, 0, 255)
PURPLE = (165, 0, 165)
LIGHTGREEN = (96, 255, 175)

brick_style = {'normal': RED,
                'spec_1': BLUE,
                'wall': DARKGREY,
                'final': PURPLE }

# Labels: =================================
START_X = 12; START_Y = 2
title_font = pygame.font.SysFont('Verdana',25)
small_font = pygame.font.SysFont('Verdana',20)
start_button_text = title_font.render('Start!' , True , BLACK)
start_button_border = pygame.Rect(START_X-10, START_Y, 90, 35)
SHOT_TEXT_X = 360; SHOT_TEXT_Y = 12
shot_text = title_font.render('Shots:' , True , BLACK)
shot_num = 10
shot_number_text = title_font.render(str(shot_num) , True , BLACK)

back_button_text = title_font.render('Back' , True , BLACK)
back_button_border = pygame.Rect(START_X-10, START_Y, 90, 35)

# For menu staffs...: ===================================================================
BORDER_LEVEL_W = 170
BORDER_LEVEL_Y = 40
level_borders = []
for i in range(3):
    for j in range(3):
        level_borders.append(pygame.Rect(i * BORDER_LEVEL_W, 
                                        BORDER_LEVEL_Y + j * BORDER_LEVEL_W, 
                                        BORDER_LEVEL_W, 
                                        BORDER_LEVEL_W))

start_border = pygame.Rect(0, 0, WIDTH, BORDER_LEVEL_Y)
game_settings_menu = pygame.Rect(0, 0, WIDTH, SHIFT_Y)
game_settings_border = pygame.Rect(0, 0, WIDTH, SHIFT_Y+1)

level_pics = []
level_names = ["level_01", "level_02", "level_03", "level_04", "level_05", "level_06", "level_07"]
for name in level_names:
    level_pic = pygame.image.load(os.path.join("images", name + ".png"))
    level_pic = pygame.transform.scale(pygame.image.load(os.path.join("images", name + ".png")), (BORDER_LEVEL_W-4, BORDER_LEVEL_W-4))
    level_pics.append(level_pic)

# Render Functions: =======================================================================
def update_window_game(slider, ball, brick_types, target_end):
    WIN.fill(GREY)
    slider.draw_slider()
    ball.draw_ball()
    # Draw blocks for each type:
    for brick in brick_types.values():
        brick.draw_brick()

    if ball.drop_ball is False:
        pygame.draw.line(WIN, BLACK, (ball.x+6, ball.y), target_end, width = 2)
    pygame.draw.rect(WIN, LIGHTGREEN, game_settings_menu)
    pygame.draw.rect(WIN, BLACK, game_settings_menu, 2)
    WIN.blit(shot_text, (SHOT_TEXT_X, SHOT_TEXT_Y))
    WIN.blit(shot_number_text, (SHOT_TEXT_X+90, SHOT_TEXT_Y))
    WIN.blit(back_button_text, (START_X, SHOT_TEXT_Y))
    pygame.display.update()

def update_window_menu(visible_level, visible_level_fix):
    WIN.fill(WHITE)
    WIN.blit(start_button_text, (START_X, START_Y))
    #pygame.draw.rect(WIN, BLACK, start_button_border, 2)
    for border in level_borders:
        pygame.draw.rect(WIN, BLACK, border, 2)

    for count, value in enumerate(level_pics):
        value.set_alpha(100)
        if count == visible_level or count == visible_level_fix: value.set_alpha(255)
        WIN.blit(value, (level_borders[count].x+2, level_borders[count].y+2))

    pygame.draw.rect(WIN, BLACK, start_border, 2)
    pygame.display.update()

# Other Functions: =======================================================================
def collide_ball_brick(ball, brick_types):
    collision_hor = False
    collision_ver = False
    for brick in brick_types.values():
        for i in range(len(brick.block_list)):
            if ( pygame.Rect.colliderect(ball.rect, brick.border_list[i][0]) or
                pygame.Rect.colliderect(ball.rect, brick.border_list[i][1]) ):
                collision_hor = True
                if brick.name == 'normal':
                    del brick.block_list[i], brick.border_list[i]
                break
            if ( pygame.Rect.colliderect(ball.rect, brick.border_list[i][2]) or
                pygame.Rect.colliderect(ball.rect, brick.border_list[i][3]) ):
                collision_ver = True
                if brick.name == 'normal':
                    del brick.block_list[i], brick.border_list[i]
                break

    return collision_hor, collision_ver

def move_target(keys_pressed, ball):
    if keys_pressed[pygame.K_UP] and ball.target_alfa < math.pi/2:
        ball.target_alfa += math.pi / TARGET_PRECISION
    if keys_pressed[pygame.K_DOWN] and ball.target_alfa > -math.pi/2:
        ball.target_alfa -= math.pi / TARGET_PRECISION
    end_x = ball.x + 6 + TARGET_LENGTH*math.sin(ball.target_alfa)
    end_y = ball.y - TARGET_LENGTH*math.cos(ball.target_alfa)

    return end_x, end_y

def load_level(visible_level_fix, brick_types):
    def add_block(name, x_pos, y_pos):
        for brick in brick_types.values():
            if name == brick.name:
                brick.create_brick_data(x_pos, y_pos + SHIFT_Y)

    level_nr = visible_level_fix + 1
    with open(f"level_0{level_nr}.csv", 'r') as level_file:
        csv_file = csv.reader(level_file)
        for count, value in enumerate(csv_file):
            if value and count != 0:
                add_block(value[0], int(value[1]), int(value[2]))

    for brick in brick_types.values():
        brick.create_brick_border_data()
    
# Classes: =======================================================================
class Slider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.slider_top = [self.x + SLIDER_LENGTH/2 - 5, self.y-SLIDER_HEIGHT + 5]
        self.slider_image = SLIDER
        self.rect = pygame.Rect(self.x, self.y, SLIDER_LENGTH, 1)

    def move_slider(self, keys_pressed, ball):
        if keys_pressed[pygame.K_LEFT] and self.x - VEL_SLIDER > 0:
            self.x -= VEL_SLIDER
            if ball.drop_ball is False: ball.x -= VEL_SLIDER
        if keys_pressed[pygame.K_RIGHT] and self.x + VEL_SLIDER + SLIDER_LENGTH < WIDTH:
            self.x += VEL_SLIDER
            if ball.drop_ball is False: ball.x += VEL_SLIDER
    
    def draw_slider(self):
        WIN.blit(self.slider_image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, SLIDER_LENGTH, 1)


class Ball:
    def __init__(self, x, y):
        self.ball_image = BALL
        self.x = x
        self.y = y
        self.target_alfa = 0 #math.pi/3
        self.vel_x = VEL_BALL * math.sin(self.target_alfa)
        self.vel_y = -VEL_BALL * math.cos(self.target_alfa)
        self.drop_ball = False
        self.rect = pygame.Rect(self.x+1.8, self.y+1.5, BALL_WIDTH-3, BALL_HEIGHT-3)
        
    def move_ball(self, keys_pressed, slider):
        if self.drop_ball:
            self.y += self.vel_y
            self.x -= self.vel_x
            if slider.slider_top[1]-2 < self.y < slider.slider_top[1]+2 and (
                slider.x < self.x < slider.x + SLIDER_LENGTH):
                self.drop_ball = False
                self.vel_y *= -1
                self.target_alfa = 0
        elif keys_pressed[pygame.K_SPACE]: 
            self.drop_ball = not self.drop_ball
            self.vel_x = -VEL_BALL * math.sin(self.target_alfa)
            self.vel_y = -VEL_BALL * math.cos(self.target_alfa)
        self.rect = pygame.Rect(self.x+1.8, self.y+1.5, BALL_WIDTH-3, BALL_HEIGHT-3)

    def draw_ball(self):
        WIN.blit(self.ball_image, (self.x, self.y))
        pygame.draw.rect(WIN, RED, self.rect, 1)
        

class Block:
    def __init__(self, name, block_width, block_height):
        self.name = name
        self.block_width = block_width
        self.block_height = block_height
        self.block_list = []
        self.border_list = []

    def create_brick_data(self, x_pos, y_pos):
        self.block_list.append(pygame.Rect(x_pos, y_pos, self.block_width, self.block_height))
    
    def create_brick_border_data(self):
        if self.block_list:
            for block in self.block_list:
                self.border_list.append([
                                pygame.Rect(block.x, block.y, BLOCK_WIDTH, 1),
                                pygame.Rect(block.x, block.y + BLOCK_HEIGHT, BLOCK_WIDTH, 1),
                                pygame.Rect(block.x, block.y, 1, BLOCK_HEIGHT),
                                pygame.Rect(block.x + BLOCK_WIDTH, block.y, 1, BLOCK_HEIGHT)
                                ])

    def delete_brick_data(self, block):
        self.block_list.remove(block)

    def draw_brick(self):
        brick_color = brick_style[self.name]
        if self.block_list:
            for (block, borders) in zip(self.block_list, self.border_list):
                pygame.draw.rect(WIN, brick_color, block)
                for border in borders:
                    pygame.draw.rect(WIN, BLACK, border)

# Main function: =======================================================================
def main():
    # Define classes for brick types: -------------
    brick_normal = Block(name='normal',
                    block_width=BLOCK_WIDTH, 
                    block_height=BLOCK_HEIGHT)

    brick_spec_1 = Block(name='spec_1',
                    block_width=BLOCK_WIDTH, 
                    block_height=BLOCK_HEIGHT)
    
    brick_wall = Block(name='wall',
                    block_width=BLOCK_WIDTH, 
                    block_height=BLOCK_HEIGHT)

    brick_final = Block(name='final',
                    block_width=BLOCK_WIDTH, 
                    block_height=BLOCK_HEIGHT)
    
    brick_types = {'normal': brick_normal, 
                    'spec_1': brick_spec_1, 
                    'wall': brick_wall, 
                    'final': brick_final}
    # Initial data for run:---------------------------------
    slider = Slider(x = WIDTH/2, y = 0.9*HEIGHT)
    ball = Ball(x=slider.slider_top[0], y=slider.slider_top[1])
    window_mode = 'menu'
    clock = pygame.time.Clock()
    run = True
    visible_level_fix  = -1
    ''' 
    Game Main Loop...
    '''
    while run:
        clock.tick(FPS)
        visible_level = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ball.y > HEIGHT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if window_mode == 'menu':
                    for count, value in enumerate(level_borders):
                        if value.collidepoint(event.pos):
                            visible_level_fix = count
                            break
                        elif not start_button_border.collidepoint(pygame.mouse.get_pos()):
                            visible_level_fix = -1
                    
                    if start_button_border.collidepoint(pygame.mouse.get_pos()):
                        window_mode = 'game'
                        load_level(visible_level_fix, brick_types)
                
        # For Menu: =============================================
        if window_mode == 'menu':
            # Mouse pos.:
            for count, value in enumerate(level_borders):
                if value.collidepoint(pygame.mouse.get_pos()):
                    visible_level = count

            update_window_menu(visible_level, visible_level_fix)

        # For Game: =============================================
        elif window_mode == 'game':
            # Collision ball-slider:
            if pygame.Rect.colliderect(ball.rect, slider.rect) and (ball.rect.y + BALL_HEIGHT) <= slider.rect.y+1:
                ball.vel_y = ball.vel_y * (-1)
                
            # Collision ball-brick:
            collision_hor, collision_ver = collide_ball_brick(ball, brick_types)
            if collision_hor:
                ball.vel_y *= (-1)
            if collision_ver:
                ball.vel_x *= (-1)

            # Collision ball-border:
            if pygame.Rect.colliderect(ball.rect, BORDER_LEFT) or (
                pygame.Rect.colliderect(ball.rect, BORDER_RIGHT)):
                ball.vel_x *= (-1)
            if pygame.Rect.colliderect(ball.rect, BORDER_TOP):
                ball.vel_y *= (-1)

            # Update positions + window for the game:
            keys_pressed = pygame.key.get_pressed()
            slider.move_slider(keys_pressed, ball)
            ball.move_ball(keys_pressed, slider)
            target_end =move_target(keys_pressed, ball)
            update_window_game(slider, ball, brick_types, target_end)

    main()

if __name__ == "__main__":
    main()
