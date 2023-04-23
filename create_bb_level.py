import pygame
import sys
import os
import csv
import datetime
pygame.init()
pygame.font.init()

# Initial data: =======================================================================
WIDTH, HEIGHT = 500, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Colors:
GREY = (200, 200, 200)
DARKGREY = (70, 70, 70)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLUE = (0, 0, 255)
PURPLE = (165, 0, 165)
#----------------
FPS = 60
IMAGE_NORMAL = pygame.image.load(os.path.join("images", "brick_1.png"))
WIDTH_NORMAL, HEIGHT_NORMAL = 25, 25
row_num = int(WIDTH / WIDTH_NORMAL)
column_num = int((HEIGHT - 300) / HEIGHT_NORMAL)
pygame.display.set_caption("Brick Breaker - Creator Mode")
smallfont = pygame.font.SysFont('Verdana',25)
text_font = pygame.font.SysFont('Verdana',15)
field = ["name", "x", "y", "width"]
brick_style = {'normal': RED,
                'spec_1': BLUE,
                'wall': DARKGREY,
                'final': PURPLE }
# Buttons: ===============================================================================
BUTTON_1_X = 4
BUTTON_1_Y = HEIGHT - 85
BUTTON_1_WIDTH = 145
BUTTON_1_HEIGHT = 30
button_1_text = smallfont.render('Place Block' , True , BLACK)
button_1_border = pygame.Rect(BUTTON_1_X-2, BUTTON_1_Y, BUTTON_1_WIDTH, BUTTON_1_HEIGHT)

BUTTON_2_X = BUTTON_1_X + BUTTON_1_WIDTH + 10
BUTTON_2_Y = BUTTON_1_Y
BUTTON_2_WIDTH, BUTTON_2_HEIGHT = 80, BUTTON_1_HEIGHT
button_2_text = smallfont.render('Fill All' , True , BLACK)
button_2_border = pygame.Rect(BUTTON_2_X-2, BUTTON_2_Y, BUTTON_2_WIDTH, BUTTON_2_HEIGHT)

BUTTON_3_X = BUTTON_2_X + BUTTON_2_WIDTH + 10
BUTTON_3_Y = BUTTON_1_Y
BUTTON_3_WIDTH, BUTTON_3_HEIGHT = 70, BUTTON_1_HEIGHT
button_3_text = smallfont.render('Save' , True , BLACK)
button_3_border = pygame.Rect(BUTTON_3_X-2, BUTTON_3_Y, BUTTON_3_WIDTH, BUTTON_3_HEIGHT)

BUTTON_4_X = BUTTON_3_X + BUTTON_3_WIDTH + 10
BUTTON_4_Y = BUTTON_1_Y
BUTTON_4_WIDTH, BUTTON_4_HEIGHT = 70, BUTTON_1_HEIGHT
button_4_text = smallfont.render('Load' , True , BLACK)
button_4_border = pygame.Rect(BUTTON_4_X-2, BUTTON_4_Y, BUTTON_4_WIDTH, BUTTON_4_HEIGHT)

BUTTON_5_X = BUTTON_4_X + BUTTON_4_WIDTH + 10
BUTTON_5_Y = BUTTON_1_Y
BUTTON_5_WIDTH, BUTTON_5_HEIGHT = 70, BUTTON_1_HEIGHT
button_5_text = smallfont.render('Clear' , True , BLACK)
button_5_border = pygame.Rect(BUTTON_5_X-2, BUTTON_5_Y, BUTTON_5_WIDTH, BUTTON_5_HEIGHT)

ENTRY_X = 5
ENTRY_Y = BUTTON_1_Y + BUTTON_1_HEIGHT + 10
ENTRY_WIDTH, ENTRY_HEIGHT = 250, BUTTON_1_HEIGHT
entry_border = pygame.Rect(ENTRY_X, ENTRY_Y, ENTRY_WIDTH, ENTRY_HEIGHT)

BRICK_1_X = ENTRY_X + ENTRY_WIDTH + 15
BRICK_1_Y = ENTRY_Y
BRICK_1_WIDTH, BRICK_1_HEIGHT = 35, 35
brick_1 = pygame.Rect(BRICK_1_X, BRICK_1_Y, BRICK_1_WIDTH, BRICK_1_HEIGHT)
brick_1_border = brick_1.copy()

BRICK_2_X = BRICK_1_X + BRICK_1_WIDTH + 10
BRICK_2_Y = BRICK_1_Y
BRICK_2_WIDTH, BRICK_2_HEIGHT = 35, 35
brick_2 = pygame.Rect(BRICK_2_X, BRICK_2_Y, BRICK_2_WIDTH, BRICK_2_HEIGHT)
brick_2_border = brick_2.copy()

BRICK_3_X = BRICK_2_X + BRICK_2_WIDTH + 10
BRICK_3_Y = BRICK_2_Y
BRICK_3_WIDTH, BRICK_3_HEIGHT = 35, 35
brick_3 = pygame.Rect(BRICK_3_X, BRICK_3_Y, BRICK_3_WIDTH, BRICK_3_HEIGHT)
brick_3_border = brick_3.copy()

BRICK_4_X = BRICK_3_X + BRICK_3_WIDTH + 10
BRICK_4_Y = BRICK_3_Y
BRICK_4_WIDTH, BRICK_4_HEIGHT = 35, 35
brick_4 = pygame.Rect(BRICK_4_X, BRICK_4_Y, BRICK_4_WIDTH, BRICK_4_HEIGHT)
brick_4_border = brick_4.copy()

# Draw template bricks
bricks_template = []
for i in range(row_num):
    for j in range(column_num):
        bricks_template.append(pygame.Rect(i * WIDTH_NORMAL, j * HEIGHT_NORMAL, WIDTH_NORMAL, HEIGHT_NORMAL))
#=======================================================================================

# Block - Class: =======================================================================
class Block:
    def __init__(self, name, block_width, block_height):
        self.name = name
        self.block_width = block_width
        self.block_height = block_height
        self.block_list = []

    def create_brick_data(self, x_pos, y_pos):
        self.block_list.append(pygame.Rect(x_pos, y_pos, self.block_width, self.block_height))

    def delete_brick_data(self, block):
        self.block_list.remove(block)

    def draw_brick(self):
        brick_color = brick_style[self.name]
        if self.block_list:
            for block in self.block_list:
                pygame.draw.rect(WIN, brick_color, block)

# Functions: =======================================================================
def update_window(brick_types, border_1_color, entry_text, active_brick_border):
    WIN.fill(GREY)
    # Option buttons + borders:
    WIN.blit(button_1_text, (BUTTON_1_X, BUTTON_1_Y))
    WIN.blit(button_2_text, (BUTTON_2_X, BUTTON_2_Y))
    WIN.blit(button_3_text, (BUTTON_3_X, BUTTON_3_Y))
    WIN.blit(button_4_text, (BUTTON_4_X, BUTTON_4_Y))
    WIN.blit(button_5_text, (BUTTON_5_X, BUTTON_5_Y))
    WIN.blit(entry_text, (ENTRY_X + 4, ENTRY_Y + 4))
    pygame.draw.rect(WIN, border_1_color, button_1_border, 2)
    pygame.draw.rect(WIN, BLACK, button_2_border, 2)
    pygame.draw.rect(WIN, BLACK, button_3_border, 2)
    pygame.draw.rect(WIN, BLACK, button_4_border, 2)
    pygame.draw.rect(WIN, BLACK, button_5_border, 2)
    pygame.draw.rect(WIN, BLACK, entry_border, 2)
    # Brick switch - Buttons + borders:
    pygame.draw.rect(WIN, brick_style['normal'], brick_1)
    pygame.draw.rect(WIN, brick_style['spec_1'], brick_2)
    pygame.draw.rect(WIN, brick_style['wall'], brick_3)
    pygame.draw.rect(WIN, brick_style['final'], brick_4)
    pygame.draw.rect(WIN, active_brick_border['normal'], brick_1_border, 4)
    pygame.draw.rect(WIN, active_brick_border['spec_1'], brick_2_border, 4)
    pygame.draw.rect(WIN, active_brick_border['wall'], brick_3_border, 4)
    pygame.draw.rect(WIN, active_brick_border['final'], brick_4_border, 4)
    # Draw blocks for each type:
    for value in brick_types.values():
        value.draw_brick()
    # Draw template blocks:
    for temp_brick in bricks_template:
        pygame.draw.rect(WIN, BLACK, temp_brick, 1)
    pygame.display.update()

def fill_temp_block(brick_current, x_pos, y_pos, border_1_color, brick_types):
    # Add block:
    if border_1_color == GREEN:
        for block in bricks_template:
            if block not in brick_current.block_list and block.collidepoint(x_pos, y_pos):
                # deleting existing block there:
                for value in brick_types.values():
                    if block in value.block_list:
                        value.delete_brick_data(block)
                brick_current.create_brick_data(block.x, block.y)
                break
    # Delete block:
    elif border_1_color == BLACK:
        for block in brick_current.block_list:
            if block in brick_current.block_list and block.collidepoint(x_pos, y_pos):
                brick_current.delete_brick_data(block)
                break

def fill_all(brick_current, brick_types):
    for block in bricks_template:
        if block not in brick_current.block_list:
            # deleting existing block there:
            for value in brick_types.values():
                    if block in value.block_list:
                        value.delete_brick_data(block)
            brick_current.create_brick_data(block.x, block.y)

def save_block_data(brick_types, file_text):
    if file_text:
        file_name = file_text
    else:
        x = datetime.datetime.now()
        sec = x.strftime("%S")
        mins = x.strftime("%M")
        hour = x.strftime("%I")
        day = x.strftime("%d")
        file_name = f"level_data_{day}_{hour}_{mins}_{sec}"

    file_to_csv = f"{file_name}.csv"
    with open(file_to_csv, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        block_data = []
        for brick in brick_types.values():
            for block in brick.block_list:
                block_data.append([brick.name, block.x, block.y, brick.block_width])
        csvwriter.writerows(block_data)
        csvfile.close()

def load_level(brick_types, file_text):

    def add_block(name, x_pos, y_pos):
        for brick in brick_types.values():
            if name == brick.name:
                brick.create_brick_data(x_pos, y_pos)

    for brick in brick_types.values():
        brick.block_list = []

    with open(file_text + ".csv", 'r') as level_file:
        csv_file = csv.reader(level_file)
        k = 0
        for line in csv_file:
            if line and k != 0:
                add_block(line[0], int(line[1]), int(line[2]))
            k += 1

def clear_all(brick_current):
    for block in bricks_template:
        if block in brick_current.block_list:
            brick_current.delete_brick_data(block)
        
# Main function: =======================================================================
def main():
    # Define classes for brick types: -------------
    brick_normal = Block(name='normal',
                    block_width=WIDTH_NORMAL, 
                    block_height=HEIGHT_NORMAL)

    brick_spec_1 = Block(name='spec_1',
                    block_width=WIDTH_NORMAL, 
                    block_height=HEIGHT_NORMAL)
    
    brick_wall = Block(name='wall',
                    block_width=WIDTH_NORMAL, 
                    block_height=HEIGHT_NORMAL)

    brick_final = Block(name='final',
                    block_width=WIDTH_NORMAL, 
                    block_height=HEIGHT_NORMAL)
    # Initial data for run:---------------------------------
    brick_types = {'normal': brick_normal, 
                    'spec_1': brick_spec_1, 
                    'wall': brick_wall, 
                    'final': brick_final}

    active_brick_border = {'normal': BLACK,
                            'spec_1': GREY,
                            'wall': GREY,
                            'final': GREY}
    file_text = ''
    entry_text = text_font.render(file_text, True , BLACK)
    border_1_color = GREEN
    current_style = 'normal'
    clock = pygame.time.Clock()
    run = True
    ''' 
    Game Main Loop:
    '''
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Create block by clicking:---------------------
                fill_temp_block(brick_types[current_style], mouse[0], mouse[1], border_1_color, brick_types)

                # Checking Option buttons: ------------------------
                # Block Place/delete button:
                if button_1_border.collidepoint(event.pos):
                    if border_1_color == BLACK:
                        border_1_color = GREEN
                    else: border_1_color = BLACK

                # Fill all button:
                if button_2_border.collidepoint(event.pos):
                    fill_all(brick_types[current_style], brick_types)

                # Save button:
                if button_3_border.collidepoint(event.pos):
                    save_block_data(brick_types, file_text)
                    
                # load button:
                if button_4_border.collidepoint(event.pos):
                    load_level(brick_types, file_text)
                
                # Clear all button:
                if button_5_border.collidepoint(event.pos):
                    clear_all(brick_types[current_style])
                
                # Brick switch buttons:-----------------------
                if brick_1.collidepoint(event.pos):
                    active_brick_border[current_style] = GREY
                    current_style = 'normal'
                    active_brick_border[current_style] = BLACK
                
                if brick_2.collidepoint(event.pos):
                    active_brick_border[current_style] = GREY
                    current_style = 'spec_1'
                    active_brick_border[current_style] = BLACK

                if brick_3.collidepoint(event.pos):
                    active_brick_border[current_style] = GREY
                    current_style = 'wall'
                    active_brick_border[current_style] = BLACK

                if brick_4.collidepoint(event.pos):
                    active_brick_border[current_style] = GREY
                    current_style = 'final'
                    active_brick_border[current_style] = BLACK

            # Reading the text:------------------------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    file_text = file_text[:-1]
                else:
                    file_text += event.unicode
                entry_text = text_font.render(file_text, True , BLACK)

        mouse = pygame.mouse.get_pos()
        update_window(brick_types, border_1_color, entry_text, active_brick_border)

if __name__ == "__main__":
    main()
