import pygame
from random import randint

tamanho = (900, 600)
branco = (255, 255, 255)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption('Fruit Basket')
pygame.init()
pygame.mixer.init()

img_fundo = pygame.image.load('./assets/sprites/fundologo.png').convert_alpha()
img_fundo_go = pygame.image.load('./assets/sprites/fundogameover.png').convert_alpha()
img_logo = pygame.image.load('./assets/sprites/logo.png').convert_alpha()
img_go = pygame.image.load('./assets/sprites/gameover.png').convert_alpha()
img_comecar = pygame.image.load('./assets/sprites/comecar.png').convert_alpha()
img_cesta = pygame.image.load('./assets/sprites/cesta.png').convert_alpha()
img_frutas = [
    pygame.image.load('./assets/sprites/abacaxi.png').convert_alpha(),
    pygame.image.load('./assets/sprites/laranja.png').convert_alpha(),
    pygame.image.load('./assets/sprites/morango.png').convert_alpha(),
    pygame.image.load('./assets/sprites/pimenta.png').convert_alpha()
]
img_vidas = [
    pygame.image.load('./assets/sprites/vida0.png').convert_alpha(),
    pygame.image.load('./assets/sprites/vida1.png').convert_alpha(),
    pygame.image.load('./assets/sprites/vida2.png').convert_alpha(),
    pygame.image.load('./assets/sprites/vida3.png').convert_alpha()
]
img_perde_pts = pygame.image.load('./assets/sprites/-5pts.png').convert_alpha()

rect_fundo = img_fundo.get_rect()
rect_fundo_go = img_fundo_go.get_rect()
rect_go = img_go.get_rect()
rect_logo = img_logo.get_rect()
rect_comecar = img_comecar.get_rect()
rect_cesta = img_cesta.get_rect()
rect_vidas = img_vidas[0].get_rect()
rect_frutas = [
    img_frutas[0].get_rect(),
    img_frutas[1].get_rect(),
    img_frutas[2].get_rect(),
    img_frutas[3].get_rect()
]
rect_logo.centerx = tamanho[0] / 2
rect_logo.y = -rect_logo.height
rect_go.y = -rect_go.height
rect_comecar.centerx = tamanho[0] / 2
rect_comecar.y = -rect_comecar.height
rect_cesta.centerx = tamanho[0] / 2
rect_cesta.y = 450
rect_vidas.x = 20
rect_vidas.y = tamanho[1] - rect_vidas.height
rect_frutas[0].x = randint(0, 850)
rect_frutas[1].x = randint(0, 850)
rect_frutas[2].x = randint(0, 850)
rect_frutas[0].y = 0
rect_frutas[0].y = 0
rect_frutas[0].y = 0
rect_perde_pts = img_perde_pts.get_rect()
rect_perde_pts.x = rect_cesta.centerx
rect_perde_pts.y = rect_cesta.y - rect_perde_pts.height

music_logo = pygame.mixer.Sound('./assets/music/musicalogo.ogg')
music_game = pygame.mixer.Sound('./assets/music/musicagame.ogg')
sfx_ponto = pygame.mixer.Sound('./assets/sfx/ponto.ogg')
sfx_erro = pygame.mixer.Sound('./assets/sfx/erro.ogg')
sfx_grito = pygame.mixer.Sound('./assets/sfx/grito.ogg')
sfx_comeca = pygame.mixer.Sound('./assets/sfx/comeca.ogg')
sfx_go = pygame.mixer.Sound('./assets/sfx/gameover.ogg')
music_channel = pygame.mixer.Channel(1)
sfx_channel = pygame.mixer.Channel(2)
music_channel.set_volume(.5)
sfx_channel.set_volume(.3)

fonte = pygame.font.SysFont('arial', 28)

cont_comecar = 0
esquerda = False
direita = False
velocidade = 20
vidas = 3
trigger_fruta = 0
tempo_fruta = 60
tipo_fruta = 0
angulo = 0
desenha_fruta = False
pontos = 0
texto_pontos = 'Pontos: %i' %pontos
trigger_pontos = 0
cont_perda = 0
music_trigger = True
flag = 1

tela.fill(branco)


while True:

    for e in pygame.event.get():
        if (e.type == pygame.QUIT):
            exit()

        if (flag == 1) and (rect_logo.y == 100):
            if (e.type == pygame.KEYDOWN):
                if (e.key == 32):
                    music_trigger = True
                    sfx_channel.play(sfx_comeca)
                    pygame.time.wait(2000)
                    flag = 2

        if (vidas > 0) and (flag == 2):
            if (e.type == pygame.KEYDOWN):
                if (e.key == 276):
                    esquerda = True
                if (e.key == 275):
                    direita = True
            if (e.type == pygame.KEYUP):
                if (e.key == 276):
                    esquerda = False
                if (e.key == 275):
                    direita = False
    if (flag == 1):
        if (music_trigger == True):
            music_channel.play(music_logo, -1)
            music_trigger = False
        if (rect_logo.y < 100):
            rect_logo.y += 5
        if (rect_logo.y == 100):
            rect_comecar.y = 450
            cont_comecar += 1
        tela.blit(img_fundo, rect_fundo)
        tela.blit(img_logo, rect_logo)
        if (cont_comecar > 20) and (cont_comecar <= 40):
            tela.blit(img_comecar, rect_comecar)
        if (cont_comecar > 40):
            cont_comecar = 0

    elif (flag == 2):
        texto_pontos = 'Pontos: %i' % pontos
        score = fonte.render(texto_pontos, True, (0, 0, 0), branco)
        rect_perde_pts.x = rect_cesta.centerx
        rect_perde_pts.y = rect_cesta.y - rect_perde_pts.height
        if (music_trigger == True):
            music_channel.play(music_game, -1)
            music_trigger = False
        if (esquerda):
            if (rect_cesta.x > 0):
                rect_cesta.x += -velocidade
        if (direita):
            if (rect_cesta.x + rect_cesta.width < tamanho[0]):
                rect_cesta.x += velocidade

        trigger_fruta += 1

        if (trigger_fruta == tempo_fruta):
            tipo_fruta = randint(0, 3)
            angulo = randint (1, 359)
            trigger_fruta = 0
            rect_frutas[tipo_fruta].x = randint(0, 850)
            rect_frutas[tipo_fruta].y = 0
            desenha_fruta = True

        if (desenha_fruta):
            if (rect_frutas[tipo_fruta].y < tamanho[1]):
                rect_frutas[tipo_fruta].y += velocidade - 10
                fruta = pygame.transform.rotate(img_frutas[tipo_fruta], angulo)
            else:
                desenha_fruta = False

        if (rect_frutas[tipo_fruta].colliderect(rect_cesta)):
            desenha_fruta = False
            rect_frutas[tipo_fruta].y = - rect_frutas[tipo_fruta].height
            if (tipo_fruta != 3):
                pontos += 1
                sfx_channel.play(sfx_ponto)
            else:
                pontos -= 5
                sfx_channel.play(sfx_grito)
                trigger_pontos = True
                if (pontos < 0):
                    pontos = 0

            if (velocidade < 40):
                velocidade += 1
            if (tempo_fruta > 20):
                tempo_fruta -= 1

        if (angulo < 360):
            angulo += 2
        else:
            angulo = 0

        if (rect_frutas[tipo_fruta].y >= tamanho[1]) and (tipo_fruta != 3):
            rect_frutas[tipo_fruta].y = -rect_frutas[tipo_fruta].height
            vidas -= 1
            desenha_fruta = False
            sfx_channel.play(sfx_erro)
            if (vidas < 0):
                vidas = 0

        if (vidas == 0):
            flag = 3
            music_trigger = True

        tela.fill(branco)
        tela.blit(score, (750, 550))
        if (trigger_pontos == True):
            tela.blit(img_perde_pts, rect_perde_pts)
            cont_perda += 1
            if (cont_perda >= 30):
                trigger_pontos = False
                cont_perda = 0
        if (desenha_fruta):
            tela.blit(fruta, rect_frutas[tipo_fruta])
        tela.blit(img_vidas[vidas], rect_vidas)
        tela.blit(img_cesta, rect_cesta)
    elif (flag == 3):
        rect_go.centerx = tamanho[0] / 2
        if (music_trigger == True):
            music_channel.play(sfx_go)
            music_trigger = False
        if (rect_go.y < 100):
            rect_go.y += 5
        else:
            pygame.time.wait(5000)
            cont_comecar = 0
            esquerda = False
            direita = False
            velocidade = 20
            vidas = 3
            trigger_fruta = 0
            tempo_fruta = 60
            tipo_fruta = 0
            angulo = 0
            desenha_fruta = False
            pontos = 0
            texto_pontos = 'Pontos: %i' % pontos
            trigger_pontos = 0
            cont_perda = 0
            music_trigger = True
            flag = 1
            rect_go.y = -rect_go.height
            tela.fill(branco)

        tela.fill(branco)
        tela.blit(img_vidas[vidas], rect_vidas)
        tela.blit(img_cesta, rect_cesta)
        tela.blit(img_fundo_go, rect_fundo_go)
        tela.blit(img_go, rect_go)

    pygame.time.wait(int(1000 / 30))
    print(flag)
    pygame.display.flip()