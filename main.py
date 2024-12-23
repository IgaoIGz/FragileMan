import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações gerais
LARGURA = 800
ALTURA = 600
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Inicializa a tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Subway Surf Clone")
clock = pygame.time.Clock()

# Carregar imagens (substitua os caminhos pelos seus assets)
background_img = pygame.image.load("assets/background.jpg").convert()
player_img1 = pygame.image.load("assets/player_run1.png").convert_alpha()
player_img2 = pygame.image.load("assets/player_run2.png").convert_alpha()
obstacle_img = pygame.image.load("assets/obstacle.png").convert_alpha()
pista_imgs = [
    pygame.image.load("assets/andar.png").convert(),
    pygame.image.load("assets/andar.png").convert(),
    pygame.image.load("assets/andar.png").convert()
]

# Configurações do jogador
PLAYER_X = 100
PLAYER_Y_POS = [520, 420, 320]
PLAYER_WIDTH = player_img1.get_width()
PLAYER_HEIGHT = player_img1.get_height()
player_pos = 1
player_animation = [player_img1, player_img2]
player_animation_index = 0

# Controle da animação do jogador
animation_speed = 200
last_animation_time = pygame.time.get_ticks()

# Configuração dos obstáculos
obstacle_speed = 5
max_obstacle_speed = 15
obstacles = []

# Fundo em movimento
bg_x = 0
bg_speed = 2

# Pontuação
score = 0
speed_increment_threshold = 10  # Aumenta a velocidade a cada 10 pontos

def criar_obstaculo():
    """Cria um novo obstáculo em uma pista aleatória."""
    pista = random.choice([0, 1, 2])
    if not any(o[1] == pista for o in obstacles):  # Garante que não haverá obstáculo em todas as pistas
        x = LARGURA
        y = PLAYER_Y_POS[pista] - obstacle_img.get_height() + 10
        obstacles.append([x, y, pista])

def desenhar_pistas():
    """Desenha as pistas."""
    for i, pista in enumerate(pista_imgs):
        screen.blit(pista, (0, PLAYER_Y_POS[i] + PLAYER_HEIGHT // 2))

def desenhar_jogador():
    """Desenha o jogador com animação controlada por tempo."""
    global player_animation_index, last_animation_time
    current_time = pygame.time.get_ticks()

    if current_time - last_animation_time > animation_speed:
        last_animation_time = current_time
        player_animation_index = (player_animation_index + 1) % len(player_animation)

    player_y = PLAYER_Y_POS[player_pos] - PLAYER_HEIGHT + 23
    screen.blit(player_animation[player_animation_index], (PLAYER_X, player_y))

def desenhar_obstaculos():
    """Desenha e atualiza a posição dos obstáculos."""
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))
        obstacle[0] -= obstacle_speed
    obstacles[:] = [o for o in obstacles if o[0] > -obstacle_img.get_width()]

def verificar_colisao():
    """Verifica se o jogador colidiu com algum obstáculo."""
    for obstacle in obstacles:
        if PLAYER_X < obstacle[0] < PLAYER_X + PLAYER_WIDTH and player_pos == obstacle[2]:
            return True
    return False

def desenhar_background():
    """Desenha o fundo em movimento."""
    global bg_x
    bg_x -= bg_speed
    if bg_x <= -LARGURA:
        bg_x = 0
    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + LARGURA, 0))

def desenhar_pontuacao():
    """Desenha a pontuação na tela."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, PRETO)
    screen.blit(text, (10, 10))

# Menu inicial
def menu():
    menu_running = True
    options = ["Start", "Exit"]
    selected_option = 0

    font = pygame.font.Font(None, 50)
    option_rects = []

    while menu_running:
        screen.fill(PRETO)
        logo_img = pygame.image.load("assets/titulo_jogo.png").convert_alpha()
        logo_width, logo_height = 250, 125
        logo_img = pygame.transform.scale(logo_img, (logo_width, logo_height))
        logo_x = (LARGURA - logo_width) // 2
        logo_y = 50
        screen.blit(logo_img, (logo_x, logo_y))

        option_rects = []
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(options):
            text = font.render(option, True, BRANCO)
            text_width, text_height = text.get_size()
            x = (LARGURA - text_width) // 2
            y = 300 + i * 60
            rect = pygame.Rect(x, y, text_width, text_height)
            option_rects.append(rect)

            if rect.collidepoint(mouse_pos):
                text = font.render(option, True, (120, 20, 255))

            screen.blit(text, (x, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            menu_running = False
                        elif i == 1:
                            pygame.quit()
                            exit()

menu()

# Loop principal
running = True
while running:
    clock.tick(FPS)
    score += 1

    if score % speed_increment_threshold == 0 and obstacle_speed < max_obstacle_speed:
        obstacle_speed += 1

    for current_event in pygame.event.get():
        if current_event.type == pygame.QUIT:
            running = False
        if current_event.type == pygame.KEYDOWN:
            if current_event.key == pygame.K_UP and player_pos < 2:
                player_pos += 1
            elif current_event.key == pygame.K_DOWN and player_pos > 0:
                player_pos -= 1

    if random.randint(1, 100) > 98:
        criar_obstaculo()

    if verificar_colisao():
        running = False

    desenhar_background()
    desenhar_pistas()
    desenhar_jogador()
    desenhar_obstaculos()
    desenhar_pontuacao()

    pygame.display.flip()

pygame.quit()
