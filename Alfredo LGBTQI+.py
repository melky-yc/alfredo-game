import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROXO = (128, 0, 128)

# RAINBOW COLORS
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0),  
                  (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]



# Configurações da tela
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20
VELOCIDADE = 10

# Configurações da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Alfredo")

# Carrega o background
background = pygame.image.load("assets/image.png")
background = pygame.transform.scale(background, (LARGURA, ALTURA))

# Efeitos sonoros
pygame.mixer.init()

# Carregar e tocar a música de fundo
pygame.mixer.music.load("assets/musica.mp3")  # Carrega a música
pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop infinito
pygame.mixer.music.set_volume(1.0)  # Ajusta o volume (0.0 a 1.0)

# Carregar o som de comer
som_comer = pygame.mixer.Sound("assets/comer.wav")

# Relógio
relogio = pygame.time.Clock()

def mensagem(msg, cor, y_offset=0):
    fonte = pygame.font.SysFont(None, 50)
    texto = fonte.render(msg, True, cor)
    texto_rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + y_offset))
    tela.blit(texto, texto_rect)

def mostrar_info(pontos, tempo_decorrido, velocidade):
    fonte = pygame.font.SysFont(None, 33)
    texto_pontos = fonte.render(f"{pontos}", True, BRANCO)
    texto_tempo = fonte.render(f"{int(tempo_decorrido)}", True, BRANCO)
    texto_velocidade = fonte.render(f"SPEED: {velocidade}", True, PRETO)
    tela.blit(texto_pontos, [130, 20])
    tela.blit(texto_tempo, [110, 563])

def jogo():
    fim_jogo = False
    game_over = False

    # Posição inicial do alfredo
    x = LARGURA / 2
    y = ALTURA / 2

    # Mudança de posição
    x_mudança = 0
    y_mudança = 0

    # Corpo do alfredo
    corpo_cobra = []
    comprimento_cobra = 1
    cores_cobra = []
    cores_cobra.append(RAINBOW_COLORS[0])  # Começa com vermelho


    # Comida do alfredo
    comida_x = round(random.randrange(50, 750 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
    comida_y = round(random.randrange(50, 550 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO

    # Variáveis de jogo
    pontos = 0
    tempo_inicio = time.time()

    while not fim_jogo:
        tempo_atual = time.time() - tempo_inicio
        
        while game_over:
            tela.fill(PRETO)
            mensagem(f"Game Over! Pontuação: {pontos}", VERMELHO, -50)
            mensagem("Pressione C para continuar ou Q para sair", BRANCO, 50)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    fim_jogo = True
                    game_over = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        fim_jogo = True
                        game_over = False
                    # Reiniciar variáveis
                    x = LARGURA / 2
                    y = ALTURA / 2
                    x_mudança = 0
                    y_mudança = 0
                    corpo_cobra = []
                    comprimento_cobra = 1
                    comida_x = round(random.randrange(50, 750 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
                    comida_y = round(random.randrange(50, 550 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
                    pontos = 0
                    tempo_inicio = time.time()
                    game_over = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_mudança == 0:
                    x_mudança = -TAMANHO_BLOCO
                    y_mudança = 0
                elif evento.key == pygame.K_RIGHT and x_mudança == 0:
                    x_mudança = TAMANHO_BLOCO
                    y_mudança = 0
                elif evento.key == pygame.K_UP and y_mudança == 0:
                    y_mudança = -TAMANHO_BLOCO
                    x_mudança = 0
                elif evento.key == pygame.K_DOWN and y_mudança == 0:
                    y_mudança = TAMANHO_BLOCO
                    x_mudança = 0

        # Colisão com a borda (agora causa game over)
        if x >= 750 or x < 50 or y >= 550 or y < 50:
            game_over = True

        # Atualização de posição
        x += x_mudança
        y += y_mudança

        # Alfredo não ultrapassar a borda

        if x < 45:
            x = 45
        elif x > 755 - TAMANHO_BLOCO:
            x = 755 - TAMANHO_BLOCO

        if y < 45:
            y = 45
        elif y > 555 - TAMANHO_BLOCO:
            y = 555 - TAMANHO_BLOCO

        # Desenha o background
        tela.blit(background, (0, 0))

        # Desenhar comida
        pygame.draw.rect(tela, AZUL, [comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO])

        # Desenhar alfredo
        cabeca = [x, y]
        corpo_cobra.append(cabeca)

        if len(corpo_cobra) > comprimento_cobra:
            del corpo_cobra[0]

        # Colisão com o próprio corpo
        for segmento in corpo_cobra[:-1]:
            if segmento == cabeca:
                game_over = True

        # Desenhar cobra
        for i, segmento in enumerate(corpo_cobra):
            cor = cores_cobra[i] if i < len(cores_cobra) else ROXO  # Se faltar cor, usa roxo por segurança
            pygame.draw.rect(tela, cor, [segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO])


        # Mostrar informações
        mostrar_info(pontos, tempo_atual, VELOCIDADE)

        pygame.display.update()

        # Colisão com a comida
        if abs(x - comida_x) < TAMANHO_BLOCO and abs(y - comida_y) < TAMANHO_BLOCO:
            comida_x = round(random.randrange(50, 750 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
            comida_y = round(random.randrange(50, 550 - TAMANHO_BLOCO) / TAMANHO_BLOCO) * TAMANHO_BLOCO
            comprimento_cobra += 1
            nova_cor = RAINBOW_COLORS[len(corpo_cobra) % len(RAINBOW_COLORS)]  
            cores_cobra.append(nova_cor)
            pontos += 1
            pygame.mixer.Sound.play(som_comer)  # Toca o som de comer

        relogio.tick(VELOCIDADE)

    pygame.quit()
    quit()

if __name__ == "__main__":
    jogo()