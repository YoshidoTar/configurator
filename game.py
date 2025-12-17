import pygame
import sys
import math
import random
import sqlite3

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball – Advanced Models")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 26)

SKY = (135, 206, 235)
COURT = (200, 170, 120)
BLACK = (30, 30, 30)
WHITE = (245, 245, 245)
ORANGE = (255, 140, 0)
RED = (200, 50, 50)
BLUE = (70, 130, 180)
SKIN = (255, 220, 180)
GRAY = (120, 120, 120)

player_x = 150
player_y = HEIGHT - 160
player_speed = 5
leg_anim = 0
arm_angle = -20

ball_x = player_x
ball_y = player_y
ball_r = 10
ball_active = False
ball_vx = 0
ball_vy = 0
gravity = 0.5

power = 0
max_power = 28
charging = False

score = 0

def new_hoop():
    return {
        "x": random.randint(650, 880),
        "y": random.randint(140, 260),
        "hit_anim": 0
    }

hoop = new_hoop()

def draw_background():
    screen.fill(SKY)
    pygame.draw.rect(screen, (180, 180, 180), (0, 300, WIDTH, 120))
    pygame.draw.rect(screen, COURT, (0, HEIGHT - 80, WIDTH, 80))

def draw_shadow(x, y):
    shadow_w = 60
    shadow_h = 18
    shadow_x = x + 20
    shadow_y = HEIGHT - 85
    pygame.draw.ellipse(
        screen,
        (0, 0, 0, 80),
        (shadow_x - shadow_w // 2, shadow_y, shadow_w, shadow_h)
    )

def draw_player(x, y, leg_phase, arm_angle):
    # Тень
    draw_shadow(x, y)

    pygame.draw.circle(screen, SKIN, (x + 20, y - 25), 14)

    pygame.draw.rect(screen, SKIN, (x + 16, y - 12, 8, 10))

    pygame.draw.rect(screen, BLUE, (x + 5, y, 30, 55), border_radius=8)

    shoulder_x = x + 35
    shoulder_y = y + 12

    upper_len = 20
    lower_len = 22

    rad = math.radians(arm_angle)
    elbow_x = shoulder_x + upper_len * math.cos(rad)
    elbow_y = shoulder_y + upper_len * math.sin(rad)

    hand_x = elbow_x + lower_len * math.cos(rad)
    hand_y = elbow_y + lower_len * math.sin(rad)

    pygame.draw.line(screen, BLACK, (shoulder_x, shoulder_y), (elbow_x, elbow_y), 4)
    pygame.draw.line(screen, BLACK, (elbow_x, elbow_y), (hand_x, hand_y), 4)
    pygame.draw.circle(screen, SKIN, (int(hand_x), int(hand_y)), 4)

    leg_offset = int(math.sin(leg_phase) * 6)
    pygame.draw.line(screen, BLACK, (x + 12, y + 55), (x + 10, y + 90 + leg_offset), 4)
    pygame.draw.line(screen, BLACK, (x + 28, y + 55), (x + 30, y + 90 - leg_offset), 4)

    pygame.draw.line(screen, BLACK, (x + 6, y + 90), (x + 18, y + 90), 4)
    pygame.draw.line(screen, BLACK, (x + 22, y + 90), (x + 34, y + 90), 4)

    return hand_x, hand_y

def draw_hoop(h):
    x, y = h["x"], h["y"]

    pygame.draw.rect(screen, GRAY, (x + 35, y + 10, 8, 140))
    pygame.draw.rect(screen, WHITE, (x - 40, y - 20, 100, 60))
    pygame.draw.rect(screen, BLACK, (x - 40, y - 20, 100, 60), 2)

    hoop_rect = pygame.Rect(x - 10, y + 20, 50, 8)
    pygame.draw.rect(screen, RED, hoop_rect)

    return hoop_rect

def draw_power_bar(power):
    pygame.draw.rect(screen, BLACK, (30, 30, 240, 24), 2)
    pygame.draw.rect(
        screen,
        (min(255, int(power * 8)), max(0, 255 - int(power * 6)), 60),
        (32, 32, int(power * 8), 20)
    )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_active:
                charging = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and charging:
                charging = False
                ball_active = True
                ball_vx = 6
                ball_vy = -power
                power = 0
                arm_angle = -20

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_a]:
        player_x -= player_speed
        moving = True
    if keys[pygame.K_d]:
        player_x += player_speed
        moving = True

    if moving:
        leg_anim += 0.25

    if charging and power < max_power:
        power += 0.5
        arm_angle = -20 - power

    draw_background()

    hand_x, hand_y = draw_player(player_x, player_y, leg_anim, arm_angle)

    if not ball_active:
        ball_x, ball_y = hand_x, hand_y

    if ball_active:
        ball_vy += gravity
        ball_x += ball_vx
        ball_y += ball_vy

    hoop_rect = draw_hoop(hoop)

    if ball_active:
        ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, ball_r * 2, ball_r * 2)
        if ball_rect.colliderect(hoop_rect):
            score += 1
            hoop = new_hoop()
            ball_active = False
        if ball_y > HEIGHT:
            ball_active = False

    pygame.draw.circle(screen, ORANGE, (int(ball_x), int(ball_y)), ball_r)

    draw_power_bar(power)
    screen.blit(font.render(f"Score: {score}", True, BLACK), (30, 65))

    pygame.display.flip()
    clock.tick(60)

