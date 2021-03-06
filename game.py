import pygame
import math
from PIL import Image

original = Image.open("levels/00.png")   #create the pixel map
# print("The size of the Image is: ")
# print(original.format, original.size, original.mode)

original_rgb = original.convert('RGB')
game_matrix = []

for i in range(25):    # for every col:
    for j in range(25):    # For every row
        r, g, b = original_rgb.getpixel((i, j))
        # print(r, g, b)
        if( r == 0 and g == 0 and b == 0 ):
            # print("wall!")
            game_matrix.append({'x': i, 'y': j, 'type': 'wall'})
        if( r == 255 and g == 255 and b == 255 ):
            game_matrix.append({'x': i, 'y': j, 'type': 'air'})
        #     game_matrix[i,j] = {'x': i, 'y': j, 'type': 'stone'}

print(game_matrix)

player_x = 200
player_y = 400
player_width = 25
player_height = 25
speed = 5
isJump = True
jumpCount = 10

joystick = False

game_width = 500
game_height = 500
game_border_width = 20
game_left_border = game_border_width
game_top_border = game_border_width
game_right_border = game_width - game_border_width - player_width
game_bottom_border = game_height - game_border_width - player_height

pygame.init()
win = pygame.display.set_mode((game_width,game_height))

pygame.display.set_caption("Jump game")

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


run = True
while run:
    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and player_x < game_right_border:
        player_x += speed
    if keys[pygame.K_LEFT] and player_x > game_left_border:
        player_x -= speed
    if keys[pygame.K_SPACE]:
        isJump = True
    # if keys[pygame.K_DOWN] and player_y < game_bottom_border:
    #     player_y += speed
    # if keys[pygame.K_UP] and player_y > game_top_border:
    #     player_y -= speed

    if joystick:
        # Ускорение O
        if(joystick.get_button(0) == 1):
            speed = 10
        else:
            speed = 5
        # Прыжок X
        if(joystick.get_button(1) == 1):
            isJump = True
        # Стик по горизонтали
        if(joystick.get_axis(0) > 0) and player_x < game_right_border:
            player_x += math.ceil(speed * joystick.get_axis(0))
            if(joystick.get_axis(0) < 0) and player_x > game_left_border:
                player_x += math.ceil(speed * joystick.get_axis(0))


    # Падение
    if(isJump):
        if jumpCount >= -10 or player_y < game_bottom_border - game_border_width:
            if( jumpCount < 0 ):
                player_y += math.ceil((jumpCount ** 2) / 5)
            else:
                player_y -= math.ceil((jumpCount ** 2) / 5)
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    # Стик по вертикали
    # if(joystick.get_axis(1) > 0) and player_y < game_bottom_border:
    #     player_y += math.ceil(speed * joystick.get_axis(1))
    # if(joystick.get_axis(1) < 0) and player_y > game_top_border:
    #     player_y += math.ceil(speed * joystick.get_axis(1))

    win.fill((0,0,0))
    pygame.draw.rect(win, (123,123,123), (0, 0, game_border_width, 500)) # top border
    pygame.draw.rect(win, (123,123,123), (0, 0, 500, game_border_width)) # left border
    pygame.draw.rect(win, (123,123,123), (0, game_height - game_border_width, 500, game_border_width)) # bottom border
    pygame.draw.rect(win, (123,123,123), (game_width - game_border_width, 0, game_bottom_border, 500)) # right border

    pygame.draw.rect(win, (150,0,255), (player_x, player_y, player_width, player_height))
    pygame.display.update()

pygame.quit()
