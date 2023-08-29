import pygame
import random

# Iniciando o pygame
pygame.init()

x = 1280
y = 720

# Criando o screen
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Space Invader")

# Backgraund
bg = pygame.image.load("imagens/background.png").convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

# Alien
alien = pygame.image.load("imagens/alien.png").convert_alpha()
alien = pygame.transform.scale(alien, (150, 150))

pos_alien_x = 500
pos_alien_y = 360
alien_visivel = True

alien_rect = alien.get_rect()

# Player
playerImg = pygame.image.load("imagens/spaceship.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (90, 90)) # conversão do tamanho da nave
playerImg = pygame.transform.rotate(playerImg, -90)

pos_player_x = 200
pos_player_y = 300
vida_player = 4

player_rect = playerImg.get_rect()

# Boss
boss = pygame.image.load("imagens/boss.png").convert_alpha()
boss = pygame.transform.scale(boss, (200, 200))

pos_boss_x = 1000
pos_boss_y = 360
direcao_boss = -1
vida_boss = 5

boss_rect = boss.get_rect()

# Missil
missil = pygame.image.load("imagens/bullet.png").convert_alpha()
missil = pygame.transform.scale(missil, (40, 40))
missil = pygame.transform.rotate(missil, -90)

vel_missil_x = 0
pos_missil_x = 200
pos_missil_y = 300

missil_rect = missil.get_rect()

pontos = 0

triggered = False

rodando = True

font = pygame.font.SysFont("", 50)

# funções
def respawn_alien():
    x = 1350
    y = random.randint(1, 640)
    return [x, y]
    
# Respawn do missil
def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    vel_x_missil = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_x_missil]

# ColiçãoS
def colisao_alien():
    global vida_player, pontos
    if player_rect.colliderect(alien_rect) or alien_rect.x == 60:
        vida_player -= 1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos += 1
        return True  
    else:
        return False

# Rodando o Jogo
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
            
    screen.blit(bg, (0, 0))
    
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0))
    if rel_x < 1200:
        screen.blit(bg, (rel_x, 0))
        
    # Teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        
        if not triggered:
            pos_missil_y -= 1
            
    if tecla[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1
        
        if not triggered:
            pos_missil_y += 1
            
    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_missil_x = 2
        
    if vida_player == 0:
        rodando = False
    
    # Respawn
    if pos_missil_x == 1300:
        pos_missil_x, pos_missil_y, triggered, vel_missil_x = respawn_missil()
    
    if pos_alien_x == 50 or colisao_alien():
        pos_alien_x = respawn_alien()[0]
        pos_alien_y = respawn_alien()[1]
    if alien_visivel:
        screen.blit(alien, (pos_alien_x, pos_alien_y))
        
        
    if pontos >= 3:
        screen.blit(boss, (pos_boss_x, pos_boss_y))
        
                
    # Alien Invisivel
    if pontos >= 3:
        pos_alien_x = respawn_alien()[0]
        pos_alien_y = respawn_alien()[1]
        alien_visivel = False
        
    # Posições rect    
    player_rect.x = pos_player_x
    player_rect.y = pos_player_y
    
    missil_rect.x = pos_missil_x
    missil_rect.y = pos_missil_y
    
    alien_rect.x = pos_alien_x
    alien_rect.y = pos_alien_y
    
    boss_rect.x = pos_boss_x
    boss_rect.y = pos_boss_y
    
    # Movimento do alien
    x -= 2
    pos_alien_x -= 1
    
    # Movimento do boss
    pos_boss_y += direcao_boss

    if pos_boss_y <= 0:
        direcao_boss = 1
    elif pos_boss_y >= 650:
        direcao_boss = -1
    
    # Movimento do missil
    pos_missil_x += vel_missil_x
    
    # Pontos
    score_ponto = font.render(f"Pontos: {int(pontos)} ", True, (255, 0, 0))
    screen.blit(score_ponto, (25, 25))
    
    # Vida_player
    score_vida_player = font.render(f"Vida: {int(vida_player)}", True, (255, 0, 0))
    screen.blit(score_vida_player, (25, 65))
    
    # Vida_boss
    if pontos >= 3:
        score_vida_boss = font.render(f"Vida Boss: {int(vida_boss)}", True, (255, 0, 0))
        screen.blit(score_vida_boss, (550, 25))
        
    # criar imagens
    screen.blit(missil, (pos_missil_x, pos_missil_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))
    
    pygame.display.update()