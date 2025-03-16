import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Definições da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Plataforma 2D")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock para controle de FPS
clock = pygame.time.Clock()

# Definições do jogador
player_width = 50
player_height = 60
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_health = 100

# Definições do inimigo
enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []

# Definições da moeda
coin_width = 30
coin_height = 30
coins = []

# Fonte
font = pygame.font.SysFont(None, 30)

# Função para desenhar o jogador
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

# Função para desenhar os inimigos
def draw_enemy(enemy):
    pygame.draw.rect(screen, RED, (enemy['x'], enemy['y'], enemy_width, enemy_height))

# Função para desenhar moedas
def draw_coin(coin):
    pygame.draw.circle(screen, GREEN, (coin['x'], coin['y']), coin_width // 2)

# Função para desenhar a vida do jogador
def draw_health(health):
    health_text = font.render(f"Vida: {health}", True, WHITE)
    screen.blit(health_text, (10, 10))

# Função para gerar moedas aleatórias
def generate_coin():
    x = random.randint(50, screen_width - 50)
    y = random.randint(50, screen_height - 50)
    return {'x': x, 'y': y}

# Função para gerar inimigos aleatórios
def generate_enemy():
    x = random.randint(50, screen_width - 50)
    y = random.randint(50, screen_height - 50)
    return {'x': x, 'y': y}

# Função para checar colisão entre o jogador e a moeda
def check_coin_collision(player_x, player_y, coin):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    coin_rect = pygame.Rect(coin['x'] - coin_width // 2, coin['y'] - coin_height // 2, coin_width, coin_height)
    return player_rect.colliderect(coin_rect)

# Função para checar colisão entre o jogador e o inimigo
def check_enemy_collision(player_x, player_y, enemy):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)
    return player_rect.colliderect(enemy_rect)

# Função para atacar inimigo
def attack_enemy(player_x, player_y, enemy):
    global player_health
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        enemies.remove(enemy)  # Remove o inimigo após o ataque

# Função para atualizar inimigos (seguindo o jogador)
def move_enemies(player_x, player_y):
    for enemy in enemies:
        enemy_x, enemy_y = enemy['x'], enemy['y']
        # Calcular a direção para o jogador
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Normaliza a direção
        dx /= distance
        dy /= distance
        
        # Move o inimigo em direção ao jogador
        enemy['x'] += enemy_speed * dx
        enemy['y'] += enemy_speed * dy

# Função para aplicar dano ao jogador
def apply_damage():
    global player_health
    if player_health > 0:
        player_health -= 1

# Função para aumentar a vida do jogador
def increase_health():
    global player_health
    if player_health < 100:
        player_health += 1

# Função para fazer o jogador reaparecer do outro lado se sair da tela
def wrap_around_player(x, y):
    if x < 0:
        x = screen_width
    elif x > screen_width:
        x = 0
    if y < 0:
        y = screen_height
    elif y > screen_height:
        y = 0
    return x, y

# Função para fazer os inimigos reaparecerem do outro lado se saírem da tela
def wrap_around_enemy(enemy):
    if enemy['x'] < 0:
        enemy['x'] = screen_width
    elif enemy['x'] > screen_width:
        enemy['x'] = 0
    if enemy['y'] < 0:
        enemy['y'] = screen_height
    elif enemy['y'] > screen_height:
        enemy['y'] = 0

# Loop principal do jogo
running = True
coins.append(generate_coin())
enemies.append(generate_enemy())

while running:
    screen.fill(BLACK)
    
    # Eventos de controle do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Esquerda
        player_x -= player_speed
    if keys[pygame.K_d]:  # Direita
        player_x += player_speed
    if keys[pygame.K_w]:  # Cima
        player_y -= player_speed
    if keys[pygame.K_s]:  # Baixo
        player_y += player_speed

    # Fazer o jogador "viajar" de um lado para o outro
    player_x, player_y = wrap_around_player(player_x, player_y)

    # Coleta de moedas
    for coin in coins[:]:
        if check_coin_collision(player_x, player_y, coin):
            coins.remove(coin)  # Remove a moeda
            coins.append(generate_coin())  # Gera uma nova moeda
            increase_health()  # Aumenta a vida do jogador ao pegar a moeda

    # Verifica colisões com inimigos
    for enemy in enemies[:]:
        if check_enemy_collision(player_x, player_y, enemy):
            apply_damage()  # Aplica dano ao jogador se colidir com inimigo

    # Atacar inimigos com a tecla E
    if keys[pygame.K_e]:
        for enemy in enemies[:]:
            attack_enemy(player_x, player_y, enemy)

    # Desenha os elementos do jogo
    draw_player(player_x, player_y)
    for coin in coins:
        draw_coin(coin)
    for enemy in enemies:
        draw_enemy(enemy)
    
    # Desenha a vida do jogador
    draw_health(player_health)

    # Atualiza a posição dos inimigos
    move_enemies(player_x, player_y)

    # Fazer os inimigos "viajarem" de um lado para o outro
    for enemy in enemies:
        wrap_around_enemy(enemy)

    # Atualiza a tela
    pygame.display.update()
    
    # Controla a taxa de quadros
    clock.tick(60)

pygame.quit()
