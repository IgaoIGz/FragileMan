import pygame
import random
import time
import json

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
obstacle_speed = 1.25
max_obstacle_speed = 15
obstacles = []

# Fundo em movimento
bg_x = 0
bg_speed = 2
start_time = time.time()  # Guardar o tempo inicial para controlar a velocidade

# Pontuação
score = 0
speed_increment_threshold = 10  # Aumenta a velocidade a cada 10 pontos


# Função para carregar o placar dos líderes
def carregar_placar():
    try:
        with open("placar.json", "r") as f:
            placar = json.load(f)
    except FileNotFoundError:
        placar = []
    return placar


# Função para salvar o placar dos líderes
def salvar_placar(placar):
    # Abertura do arquivo em modo de escrita e garantindo que seja tratado como texto
    with open("placar.json", "w", encoding="utf-8") as f:
        json.dump(placar, f, ensure_ascii=False, indent=4)

# Função para adicionar uma pontuação ao placar
def adicionar_ao_placar(pontuacao):
    placar = carregar_placar()

    # Adiciona a pontuação e ordena
    placar.append(pontuacao)
    placar = sorted(placar, reverse=True)[:5]  # Mantém apenas as 5 maiores pontuações

    salvar_placar(placar)


# Função para desenhar o placar dos líderes
def desenhar_placar():
    placar = carregar_placar()
    font = pygame.font.Font(None, 36)

    screen.fill(PRETO)
    placar_texto = font.render("Top Scores", True, BRANCO)
    screen.blit(placar_texto, ((LARGURA - placar_texto.get_width()) // 2, 50))

    for i, score in enumerate(placar):
        score_text = font.render(f"{i+1}. {score}", True, BRANCO)
        screen.blit(score_text, (LARGURA // 2 - score_text.get_width() // 2, 100 + i * 40))

    pygame.display.flip()

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
    """Desenha o fundo em movimento, criando um looping contínuo."""
    global bg_x, bg_speed
    largura_fundo = background_img.get_width()  # Largura real da imagem do fundo
    bg_x -= bg_speed  # Move o fundo para a esquerda

    # Quando o fundo atingir a posição final (completa a tela), reinicia a posição
    if bg_x <= -largura_fundo:
        bg_x = 0

    # Desenha o fundo duas vezes para criar o efeito de looping
    screen.blit(background_img, (bg_x, 0))  # Fundo à esquerda
    screen.blit(background_img, (bg_x + largura_fundo, 0))  # Fundo à direita


def aumentar_velocidade():
    """Aumenta a velocidade do fundo gradualmente de acordo com o tempo."""
    global bg_speed
    elapsed_time = time.time() - start_time  # Tempo decorrido desde o início do jogo

    # Aumenta a velocidade do fundo com base no tempo decorrido
    bg_speed = 2 + elapsed_time / 50  # Ajuste a divisão para controlar a aceleração


def desenhar_pontuacao():
    """Desenha a pontuação na tela."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, PRETO)
    screen.blit(text, (10, 10))


def tela_game_over():
    """Exibe a tela de Game Over com a opção de 'Menu' ou 'Placar'."""
    font = pygame.font.Font(None, 50)
    option_rects = []
    options = ["Menu", "Ver Placar"]  # Adicionando a opção de "Ver Placar"

    # Adicionar pontuação ao placar, se necessário
    adicionar_ao_placar(score)

    while True:
        screen.fill(PRETO)
        game_over_text = font.render("Game Over", True, BRANCO)
        game_over_width, game_over_height = game_over_text.get_size()
        screen.blit(game_over_text, ((LARGURA - game_over_width) // 2, ALTURA // 3))

        option_rects = []
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(options):
            text = font.render(option, True, BRANCO)
            text_width, text_height = text.get_size()
            x = (LARGURA - text_width) // 2
            y = ALTURA // 2 + i * 60
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
                        if i == 0:  # Menu
                            return False  # Retorna para o menu sem fechar o jogo
                        elif i == 1:  # Ver Placar
                            desenhar_placar()
                            time.sleep(3)  # Exibe o placar por 3 segundos
                            return False  # Retorna ao menu após ver o placar


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
                            return False  # Se escolher "Exit", retorna False para encerrar o jogo

    return True  # Se escolheu "Start", retorna True para iniciar o jogo


# Loop principal
running = True
while running:
    if not menu():  # Se o jogador escolher "Exit" no menu, encerra o jogo
        break

    score = 0
    obstacles = []
    player_pos = 1
    bg_x = 0
    obstacle_speed = 1.25
    start_time = time.time()

    # Loop do jogo
    while True:
        clock.tick(FPS)
        score += 1

        if score % speed_increment_threshold == 0 and obstacle_speed < max_obstacle_speed:
            obstacle_speed += 1

        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                running = False
                break
            if current_event.type == pygame.KEYDOWN:
                if current_event.key == pygame.K_UP and player_pos < 2:
                    player_pos += 1
                elif current_event.key == pygame.K_DOWN and player_pos > 0:
                    player_pos -= 1

        if random.randint(1, 100) > 98:
            criar_obstaculo()

        if verificar_colisao():
            if not tela_game_over():  # Se o jogador escolher "Menu", volta ao menu
                break  # Se o jogador escolher "Tente Novamente", reinicia o jogo

        # Aumenta a velocidade do fundo com o tempo
        aumentar_velocidade()

        desenhar_background()
        desenhar_pistas()
        desenhar_jogador()
        desenhar_obstaculos()
        desenhar_pontuacao()

        pygame.display.flip()

pygame.quit()
