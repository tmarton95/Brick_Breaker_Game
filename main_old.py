import pygame
import sys
import os
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

FPS = 60
VEL = 8
VEL_BALL = 2.2

SLIDER = pygame.image.load(os.path.join("images", "slider.png"))
SLIDER_WIDTH, SLIDER_HEIGHT = 80, 20

BLOCK_WIDTH, BLOCK_HEIGHT = 25, 25
BLOCK = pygame.image.load(os.path.join("images", "brick_1.png"))
BLOCK = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "brick_1.png")), (BLOCK_WIDTH, BLOCK_HEIGHT))
BLOCK_ROW = 8
HEIGHT_0 = 100

BALL_WIDTH, BALL_HEIGHT = 15, 15
BALL = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "ball.png")), (BALL_WIDTH, BALL_HEIGHT))

BORDER_LEFT = pygame.Rect(0, 0, 2, HEIGHT)
BORDER_RIGHT = pygame.Rect(WIDTH, 0, 2, HEIGHT)
BORDER_TOP = pygame.Rect(0, 0, WIDTH, 1)

WHITE = ""
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

def update_window_1(slider, ball, brick):
    WIN.fill(GREY)
    slider.draw_slider()
    ball.draw_ball()
    brick.draw_brick()
    pygame.display.update()

def collide_ball_brick(ball, brick):
    collision_hor = False
    collision_ver = False
    for i in range(len(brick.block_list)):
        if ( pygame.Rect.colliderect(ball.rect, brick.border_list[i][0]) or
            pygame.Rect.colliderect(ball.rect, brick.border_list[i][1]) ):
            collision_hor = True
            del brick.block_list[i], brick.border_list[i]
            break
        if ( pygame.Rect.colliderect(ball.rect, brick.border_list[i][2]) or
            pygame.Rect.colliderect(ball.rect, brick.border_list[i][3]) ):
            collision_ver = True
            del brick.block_list[i], brick.border_list[i]
            break

    return collision_hor, collision_ver
        

class Slider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.slider_image = SLIDER
        self.rect = pygame.Rect(self.x, self.y, SLIDER_WIDTH, 1)

    def move_slider(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.x - VEL > 0:
            self.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and self.x + VEL + SLIDER_WIDTH < WIDTH:
            self.x += VEL
    
    def draw_slider(self):
        WIN.blit(self.slider_image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, SLIDER_WIDTH, 1)


class Ball:
    def __init__(self, x, y):
        self.ball_image = BALL
        self.x = x
        self.y = y
        self.vel_direction = 1
        self.vel_x = 0.7 * VEL_BALL
        self.vel_y = -VEL_BALL
        self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BALL_HEIGHT)
    
    def move_ball(self):
        self.y += self.vel_y
        self.x -= self.vel_x

    def draw_ball(self):
        WIN.blit(self.ball_image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BALL_HEIGHT)


class Bricks:
    def __init__(self):
        self.block_image = BLOCK
        self.block_list = []
        for j in range(BLOCK_ROW):
            for i in range(0, WIDTH, BLOCK_WIDTH):
                self.block_list.append(pygame.Rect(i, HEIGHT_0 + j*BLOCK_HEIGHT, 
                                        BLOCK_WIDTH, BLOCK_HEIGHT))
        self.border_list = []
        for block in self.block_list:
            self.border_list.append([
                            pygame.Rect(block.x, block.y, BLOCK_WIDTH, 1),
                            pygame.Rect(block.x, block.y + BLOCK_HEIGHT, BLOCK_WIDTH, 1),
                            pygame.Rect(block.x, block.y, 1, BLOCK_HEIGHT),
                            pygame.Rect(block.x + BLOCK_WIDTH, block.y, 1, BLOCK_HEIGHT)
                            ])

    def draw_brick(self):
        for block in self.block_list:
            WIN.blit(self.block_image, (block.x, block.y))
        

def main():
    slider = Slider(x = WIDTH/2, y = 0.8*HEIGHT)
    ball = Ball(x = WIDTH/2, y = slider.y-20)
    brick = Bricks()

    clock = pygame.time.Clock()
    run = True
    ''' 
    Game Main Loop...
    '''
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ball.y > HEIGHT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        # Collision ball-slider:
        if pygame.Rect.colliderect(ball.rect, slider.rect) and (ball.rect.y + BALL_HEIGHT) <= slider.rect.y+1:
            ball.vel_y = ball.vel_y * (-1)
            
        # Collision ball-brick:
        collision_hor, collision_ver = collide_ball_brick(ball, brick)
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
        
        # Update positions+window:
        keys_pressed = pygame.key.get_pressed()
        slider.move_slider(keys_pressed)
        ball.move_ball()
        update_window_1(slider, ball, brick)
    
    main()

if __name__ == "__main__":
    main()
