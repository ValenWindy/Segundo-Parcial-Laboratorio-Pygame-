import pygame 
from pygame.locals import *

class Pausa:
    def __init__(self):
        self.pausa = False
        self.regresar_a_menu = False
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def pausar_juego(self):
        self.pausa = not self.pausa
        # if self.pausa:
        #     self.pausar_musica()

    # def pausar_musica(self):
    #     pygame.mixer.music.pause()

    # def reanudar_musica(self):
    #     pygame.mixer.music.unpause()

    def reanudar_juego(self):
        self.pausa = False
        # self.reanudar_musica()

    def volver_menu_principal(self):
        self.regresar_a_menu = True
        # self.pausar_musica()

    def dibujar_pausa(self):
        fuente = pygame.font.Font("Constantine.ttf", 36)
        pausa_fondo = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pausa_fondo.set_alpha(128) 
        pausa_fondo.fill((0, 0, 0))  
        self.screen.blit(pausa_fondo, (0, 0))

        texto_pausa = fuente.render("PAUSA", True, (255, 255, 255))
        texto_pausa_rect = texto_pausa.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(texto_pausa, texto_pausa_rect)

        texto_opciones = fuente.render("Presione Enter para continuar o Escape para volver al menú principal", True, (255, 255, 255))
        texto_opciones_rect = texto_opciones.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(texto_opciones, texto_opciones_rect)

        pygame.display.update()  
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pausa:
                        self.volver_menu_principal()
                    else:
                        self.pausar_juego()
                elif event.key == pygame.K_RETURN:
                    if self.pausa:
                        self.pausar_juego()
                    else:
                        self.reanudar_juego()
