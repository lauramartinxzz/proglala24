import pygame
import sys

# Inicialização
pygame.init()

# Tamanho da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Raquete
paddle_width, paddle_height = 15, 100
player1 = pygame.Rect(30, (HEIGHT - paddle_height) // 2, paddle_width, paddle_height)
player2 = pygame.Rect(WIDTH - 30 - paddle_width, (HEIGHT - paddle_height) // 2, paddle_width, paddle_height)

# Bola
ball_size = 15
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_size, ball_size)
ball_speed_x = 5
ball_speed_y = 5

# Botão de reinício
restart_button = pygame.Rect(WIDTH - 120, 20, 100, 50)

# Pontuação
score1 = 0
score2 = 0

# Estado do jogo
game_over = False

def reset_game():
    global ball, ball_speed_x, ball_speed_y, player1, player2, score1, score2, game_over
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2
    ball_speed_x = 5
    ball_speed_y = 5
    player1.y = (HEIGHT - paddle_height) // 2
    player2.y = (HEIGHT - paddle_height) // 2
    score1 = 0
    score2 = 0
    game_over = False

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                reset_game()

    # Movimentação das raquetes
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= 5
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += 5
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= 5
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += 5

    # Movimentação da bola
    if not game_over:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Colisão com as paredes
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        # Pontuação
        if ball.left <= 0:
            score2 += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
        elif ball.right >= WIDTH:
            score1 += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2

        # Verificar se o jogo acabou
        if score1 >= 10 or score2 >= 10:
            game_over = True

    # Redesenhar a tela
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Desenhar o botão de reinício
    pygame.draw.rect(screen, WHITE, restart_button)
    font = pygame.font.Font(None, 36)
    text = font.render('Reiniciar', True, BLACK)
    text_rect = text.get_rect(center=restart_button.center)
    screen.blit(text, text_rect)

    # Desenhar a pontuação
    font = pygame.font.Font(None, 72)
    text = font.render(str(score1) + ' - ' + str(score2), True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, text_rect)

    # Desenhar a tela de vitória
    if game_over:
        font = pygame.font.Font(None, 72)
        if score1 >= 10:
            text = font.render('Jogador 1 venceu!', True, WHITE)
        else:
            text = font.render('Jogador 2 venceu!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

    # Controle de FPS
    pygame.time.Clock().tick(60)