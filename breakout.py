import pygame
import random

#inicializa o pygame
pygame.init()

#configurações da tela
LARGURA = 800
ALTURA = 600

#Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

#Cria a janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

class paddle:
    def __init__(self):
        self.x = LARGURA // 2 - 50
        self.y = ALTURA - 30
        self.largura = 100
        self.altura = 15
        self.velocidade = 10
        self.cor = AZUL

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.largura:
            self.x += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
    
paddle_jogador = paddle()

class Bola:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.raio = 10
        self.velocidade_x = 5
        self.velocidade_y = -5
        self.cor = BRANCO
    
    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)

    # Adiciona o método caiu
    def caiu(self):
        return self.y >= ALTURA

    # Adiciona o método reset
    def reset(self):
        self.x = LARGURA // 2
        self.y = ALTURA // 2
        self.velocidade_x = 5 * random.choice([-1, 1])  # direção aleatória
        self.velocidade_y = -5

bola = Bola()

class Bloco:
    def __init__ (self, x, y, largura, altura, cor):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

# Lista de cores para cada linha
cores_linhas = [VERMELHO, VERDE, AMARELO, AZUL]

# Lista para armazenar todos os blocos
blocos = []

# Configurações dos blocos
largura_bloco = 60
altura_bloco = 20
espacamento = 10  # Espaço entre os blocos

# Gera os blocos em várias linhas
for linha in range(len(cores_linhas)):
    for coluna in range(11):  # 10 blocos por linha
        x = coluna * (largura_bloco + espacamento) + espacamento
        y = linha * (altura_bloco + espacamento) + espacamento
        cor = cores_linhas[linha]
        blocos.append(Bloco(x, y, largura_bloco, altura_bloco, cor))

class Vida:
    def __init__(self, x, y, vidas):
        self.x = x
        self.y = y
        self.raio = 10
        self.cor = VERMELHO
        self.vidas = vidas

    def desenhar(self, tela):
        for i in range(self.vidas):
            pygame.draw.circle(tela, self.cor, (self.x + i * 30, self.y), self.raio)

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1

vidas = 3  # Número inicial de vidas
vida_jogador = Vida(30, ALTURA - 20, vidas)  # Inicializa a classe Vida

class GameOver:
    def __init__(self):
        self.fonte = pygame.font.SysFont(None, 74)
        self.texto = self.fonte.render('Game Over', True, VERMELHO)
        self.rect = self.texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

    def desenhar(self, tela):
        tela.blit(self.texto, self.rect)

game_over = GameOver()

class Pontuacao:
    def __init__(self):
        self.pontos = 0
        self.fonte = pygame.font.SysFont(None, 36)

    def adicionar_pontos(self, valor):
        self.pontos += valor

    def desenhar(self, tela):
        texto = self.fonte.render(f'Pontos: {self.pontos}', True, BRANCO)
        tela.blit(texto, (10, 10))

pontuacao = Pontuacao()

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Preenche a tela com a cor preta
    tela.fill(PRETO)

    # Pega as teclas pressionadas
    teclas = pygame.key.get_pressed()

    # Move o paddle
    paddle_jogador.mover(teclas)

    # Desenha o paddle
    paddle_jogador.desenhar(tela)

    # Move a bola
    bola.mover()

    # Desenha a bola
    bola.desenhar(tela)

    # Verifica colisão da bola com as paredes
    if bola.x - bola.raio <= 0 or bola.x + bola.raio >= LARGURA:
        bola.velocidade_x *= -1
    if bola.y - bola.raio <= 0:
        bola.velocidade_y *= -1

    # Verifica se a bola caiu (perdeu uma vida)
    if bola.caiu():
        vida_jogador.perder_vida()
        if vida_jogador.vidas <= 0:
            game_over.desenhar(tela)
            pygame.display.flip()
            pygame.time.delay(2000)
            rodando = False  # Finaliza o jogo
        else:
            bola.reset()

    # Verifica colisão da bola com o paddle
    if bola.get_rect().colliderect(paddle_jogador.get_rect()):
        bola.velocidade_y *= -1
        bola.y = paddle_jogador.y - bola.raio  # Ajusta a posição da bola para evitar múltiplas colisões

    # Desenha os blocos
    for bloco in blocos:
        bloco.desenhar(tela)

    # Verifica colisão da bola com os blocos
    for bloco in blocos:
        if bola.get_rect().colliderect(bloco.get_rect()):
            bola.velocidade_y *= -1
            if bola.y < bloco.y:
                bola.y = bloco.y - bola.raio
            else:
                bola.y = bloco.y + bloco.altura + bola.raio
            bloco.x = -100
            bloco.y = -100

    # Desenha as vidas do jogador
    vida_jogador.desenhar(tela)

    # Desenha a pontuação
    pontuacao.desenhar(tela)

    # Conta os blocos destruídos para atualizar a pontuação
    blocos_destruidos = sum(1 for bloco in blocos if bloco.x == -100 and bloco.y == -100)
    pontuacao.pontos = blocos_destruidos * 10  # Cada bloco vale 10 pontos

    # Atualiza a tela
    pygame.display.flip()

    # Define o FPS
    clock.tick(60)

pygame.quit()