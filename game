# coding: utf-8
# 1 - Import library
import pygame
import math
import random
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
pygame.mixer.init()
width, height = 700, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("打鼩鼬鼱")

# 3 - Set values & variables
time_teller = pygame.time.get_ticks
positions_s = [(posx, posy) for posy in [150, 280, 410] for posx in [90, 280, 470]]
positions_h = [(posx, posy) for posy in [115, 245, 375] for posx in [110, 300, 490]]
positions_k = [(posx, posy) for posy in [190, 320, 450] for posx in [150, 340, 530]]

## heart_rate ( over-high heart rate claims to failure...)
heart_rate, mild_rate, blush_rate, over_rate = 70, 140, 220, 300
delayed_time_on_hit = 250               ## lasting time after hit
hold_time_before_hit = 1300             ## waiting time before hit
kissing_time = 400

level_a = 100
level_b = 200
level_c = 350

# 4 - Load images
raw_bg = pygame.image.load("resources/images/background.jpg")
raw_hole = pygame.image.load("resources/images/hole.png")
raw_shrew = pygame.image.load("resources/images/shrew.png")
raw_hammer = pygame.image.load("resources/images/hammer.png")
raw_kisses = pygame.image.load("resources/images/kisses.png")
raw_gameover = pygame.image.load("resources/images/gameover.png")
background = pygame.transform.scale(raw_bg, (width, height))
hole = pygame.transform.scale(raw_hole, (150, 150))
shrew = pygame.transform.scale(raw_shrew, (150, 150))
hammer = pygame.transform.scale(raw_hammer, (100, 100))
kisses = pygame.transform.scale(raw_kisses, (25, 25))
gameover = pygame.transform.scale(raw_gameover, (width, height))

normal_img = pygame.image.load("resources/images/594x600.png")
cute_img = pygame.image.load("resources/images/600x582.png")
shy_img = pygame.image.load("resources/images/600x461.png")
heart_img = pygame.image.load("resources/images/heart.png")
normal = [pygame.transform.scale(normal_img.subsurface((x*594, 0), (594, 600)), (99, 100)) for x in range(2)]
cute = [pygame.transform.scale(cute_img.subsurface((x*600, 0), (600, 582)), (100, 97)) for x in range(5)]
shy = [pygame.transform.scale(shy_img.subsurface((x*600, 0), (600, 461)), (140, 108)) for x in range(6)]
heart = [pygame.transform.scale(heart_img, (x, x)) for x in [30, 36, 42]]

# 5 - Load audios
hit = pygame.mixer.Sound("resources/audio/hit.ogg")
hit.set_volume(0.5)

# 6 - Init textbox
font = pygame.font.Font(None, 44)
def hearttext(heart_rate, pos=(120, 70)):
    global font, screen
    screen.blit(font.render(str(heart_rate), True, (255, 0, 0)), pos)
    return
def scoretext(player_score, pos=(635, 65)):
    global font, screen
    screen.blit(font.render(str(player_score), True, (255, 187, 119)), pos)
    return

# 7 - Main functions
def shining_animation(group, interval, time, pos, frame_num=None, adjust_factor=0, screen=screen):
    if not frame_num:
        frame_num = len(group)
    temp = time / interval % frame_num
    screen.blit(group[temp], (pos[0] + adjust_factor * temp, pos[1] + adjust_factor * temp))
def generate_shrew(player_score, shrews):
    temp = random.randint(0, 8)
    while shrews[temp]:
        temp = random.randint(0, 8)
    if player_score < level_a:
        return temp if not time_teller() % 40 else None
    elif player_score < level_b:
        return temp if not time_teller() % 30 else None
    elif player_score < level_c:
        return temp if not time_teller() % 20 else None
    else:
        return temp if not time_teller() % 7 else None
def maingame(heart_rate=heart_rate):
    global screen
    audio_k = [False for x in range(9)]  ## kissed yet?
    shrew_ques = {x: 0 for x in range(9)}
    hammer_on = {x: 0 for x in range(9)}
    player_score, heart_rate = 0, 70  ## initial score & heart_rate
    while True:
        if heart_rate > over_rate:
            screen.blit(gameover, (0, 0))
            pygame.display.flip()
            break
        screen.fill(0)
        screen.blit(background, (0, 0))
        #  draw the screen elements -- shrew, hammer & hole
        for index in range(9):
            if hammer_on[index]:
                screen.blit(shrew, positions_s[index])
                screen.blit(hammer, positions_h[index])
                if time_teller() - hammer_on[index] > delayed_time_on_hit:
                    shrew_ques[index] = hammer_on[index] = 0
            elif shrew_ques[index]:
                screen.blit(shrew, positions_s[index])
                mid = time_teller() - shrew_ques[index]
                if mid > hold_time_before_hit + kissing_time:  # vanishing shrew
                    shrew_ques[index] = 0
                    audio_k[index] = False
                elif mid > hold_time_before_hit:  # kissing shrew
                    if not audio_k[index]:
                        # hit.play()# play audio
                        audio_k[index] = True
                        heart_rate += 10
                    mid -= hold_time_before_hit
                    screen.blit(
                        pygame.transform.scale(kisses, (25 + mid / 60, 25 + mid / 60)),
                        (positions_k[index][0], positions_k[index][1] - mid / 20))
            else:
                screen.blit(hole, positions_s[index])
        # draw heart_rate & score
        scoretext(player_score)
        hearttext(heart_rate)

        # draw girl
        time = time_teller()
        if heart_rate < mild_rate:
            shining_animation(normal, 500, time, (180, 30), 2)
            shining_animation(heart, 650, time, (70, 70), 3, -3)
        elif heart_rate < blush_rate:
            shining_animation(cute, 500, time, (180, 30), 5)
            shining_animation(heart, 330, time, (70, 70), 3, -3)
        else:
            shining_animation(shy, 500, time, (170, 25), 6)
            shining_animation(heart, 100, time, (70, 70), 3, -3)

        # generate shrew
        if shrew_ques.values().count(0) > 3:
                shrew_ques[generate_shrew(player_score, shrew_ques)] = time_teller()

        # mouse & keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if K_0 < event.key <= K_9:
                    mid = event.key - 49
                    # if shrew being up & not kissing
                    if shrew_ques[mid] and time_teller() - shrew_ques[mid] < hold_time_before_hit:
                        hit.play()
                        player_score += 10
                        shrew_ques[event.key - 49] += delayed_time_on_hit
                        hammer_on[mid] = time_teller()
        pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

# -1 - __Main__
if __name__ == '__main__':
    maingame()
    
