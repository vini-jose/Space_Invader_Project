import pygame
import math
import os
from random import randint

# Inicializando o pygame
pygame.init()
FPS = 120
CLOCK = pygame.time.Clock()

# Criando a tela
SCREEN = pygame.display.set_mode((800, 600))

# PLANO DE FUNDO
BACKGROUND = pygame.image.load(os.path.join("imagens", "background.png"))

# Título e ícone
pygame.display.set_caption("Space Invader")
ICON = pygame.image.load(os.path.join("imagens", "ufo.png"))
pygame.display.set_icon(ICON)

# Pontuação
valor_pontuacao = 0
FONT = pygame.font.Font("freesansbold.ttf", 32)
TEST_X = 10
TEST_Y = 10

def mostrar_pontuacao(x, y):
    pontuacao = FONT.render("Pontuação: " + str(valor_pontuacao), True, (255, 255, 255))
    SCREEN.blit(pontuacao, (x, y))

# Fim de jogo
FIM_DE_JOGO_FONT = pygame.font.Font("freesansbold.ttf", 64)

def texto_fim_de_jogo():
    fim_de_jogo = FIM_DE_JOGO_FONT.render("FIM DE JOGO", True, (255, 255, 255))
    SCREEN.blit(fim_de_jogo, (200, 250))

# Jogador
imagem_jogador = pygame.image.load(os.path.join("imagens", "spaceship.png"))
posicao_jogadorX = 370
posicao_jogadorY = 480
mudanca_posicao_jogadorX = 0

def jogador(x, y):
    SCREEN.blit(imagem_jogador, (x, y))

# Alien
imagem_alien = []
posicao_alienX = []
posicao_alienY = []
mudanca_posicao_alienX = []
mudanca_posicao_alienY = []
alien_destruido = []
num_alienigenas = 6

for i in range(num_alienigenas):
    imagem_alien.append(pygame.image.load("imagens\\alien.png"))
    posicao_alienX.append(randint(0, 735))
    posicao_alienY.append(randint(50, 150))
    mudanca_posicao_alienX.append(1)
    mudanca_posicao_alienY.append(40)
    alien_destruido.append(False)

def alienigena(x, y):
    SCREEN.blit(imagem_alien[i], (x, y))

# Bala
imagem_bala = pygame.image.load("imagens\\bullet.png")
posicao_balaX = 0
posicao_balaY = 480
mudanca_posicao_balaX = 0
mudanca_posicao_balaY = 5
estado_bala = "pronta"

def disparar_bala(x, y):
    global estado_bala
    estado_bala = "disparo"
    SCREEN.blit(imagem_bala, (x + 16, y + 10))

def colisao(alienX, alienY, balaX, balaY):
    distancia = math.sqrt(
        (math.pow(alienX - balaX, 2)) + (math.pow(alienY - balaY, 2))
    )
    if distancia < 27:
        return True
    return False

# O programa principal
executando = True
while executando:
    # Relógio
    CLOCK.tick(FPS)

    # RGB
    SCREEN.fill((0, 0, 0))

    # PLANO DE FUNDO
    SCREEN.blit(BACKGROUND, (0, 0))

    # Verifica se não foi pedido para sair
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Gerando inimigos
    for i in range(num_alienigenas):
        # Fim de Jogo
        if posicao_alienY[i] > 440:
            for j in range(num_alienigenas):
                posicao_alienY[j] = 9999
            texto_fim_de_jogo()
            break

        posicao_alienX[i] += mudanca_posicao_alienX[i]

        if posicao_alienX[i] > 736:
            mudanca_posicao_alienX[i] *= -1
            posicao_alienX[i] = 736
            posicao_alienY[i] += mudanca_posicao_alienY[i]
        elif posicao_alienX[i] < 0:
            mudanca_posicao_alienX[i] *= -1
            posicao_alienX[i] = 0
            posicao_alienY[i] += mudanca_posicao_alienY[i]

        # Colisão
        colisao_ocorreu = colisao(posicao_alienX[i], posicao_alienY[i], posicao_balaX, posicao_balaY)
        if colisao_ocorreu:
            posicao_balaY = 480
            estado_bala = "pronta"
            posicao_alienX[i] = randint(0, 735)
            posicao_alienY[i] = randint(50, 150)
            valor_pontuacao += 1

        alienigena(posicao_alienX[i], posicao_alienY[i])

    # Jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mudanca_posicao_jogadorX = -2
    if keys[pygame.K_RIGHT]:
        mudanca_posicao_jogadorX = 2
    if keys[pygame.K_SPACE] and estado_bala == "pronta":
        posicao_balaX = posicao_jogadorX
        disparar_bala(posicao_balaX, posicao_balaY)

    if keys[pygame.K_UP]:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            mudanca_posicao_jogadorX = 1
    posicao_jogadorX += mudanca_posicao_jogadorX

    if posicao_jogadorX <= 10 or posicao_jogadorX >= 726:
        mudanca_posicao_jogadorX *= -1

    # Movimento da Bala
    if posicao_balaY <= 0:
        posicao_balaY = 480
        estado_bala = "pronta"

    if estado_bala == "disparo":
        disparar_bala(posicao_balaX, posicao_balaY)
        posicao_balaY -= mudanca_posicao_balaY

    jogador(posicao_jogadorX, posicao_jogadorY)
    mostrar_pontuacao(TEST_X, TEST_Y)
    pygame.display.update()

# Finaliza o pygame
pygame.quit()