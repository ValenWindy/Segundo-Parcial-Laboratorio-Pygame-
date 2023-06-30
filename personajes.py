import pygame
import sys
from pygame.locals import *
from pygame.transform import flip
from monedas import Moneda
from movimientos import animaciones_personaje_1, animaciones_personaje_2


class Personajes:
    def __init__(self):
        self.monedas = Moneda()
        self.characters = [animaciones_personaje_1, animaciones_personaje_2]
        self.personaje_actual = 0
        self.puntos = 0
        self.vidas = 3
        self.resistencia = 4
        self.cambio_personaje_realizado = False
        self.velocidad_movimiento = 3
        self.movimiento_derecha = False
        self.movimiento_izquierda = False
        self.ataque = False
        self.saltar = False
        self.posicion_x = 100
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_y = self.posicion_y_inicial
        self.direccion_personaje = "derecha"
        self.en_suelo = True
        self.sound_huntress_attack = pygame.mixer.Sound("Music/Arrow.wav")
        self.sound_soulhunter_attack = pygame.mixer.Sound("Music/Sword.wav")

        self.personaje_rect = pygame.Rect(
            self.posicion_x,
            self.posicion_y,
            self.characters[self.personaje_actual]["quieto"][0].get_width(),
            self.characters[self.personaje_actual]["quieto"][0].get_height()
        )


    def actualizar_rectangulo_personaje(self):
        ancho_nuevo = 100
        alto_nuevo = 100
        self.personaje_rect = pygame.Rect(
            self.posicion_x,
            self.posicion_y,
            ancho_nuevo,
            alto_nuevo
        )
        

        
    def eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.movimiento_derecha = True
                    self.direccion_personaje = "derecha"
                elif event.key == K_LEFT:
                    self.movimiento_izquierda = True
                    self.direccion_personaje = "izquierda"
                elif event.key == K_SPACE:
                    self.saltar = True
                elif event.key == K_a:
                    self.ataque = True
                    if self.personaje_actual == 0:
                        self.sound_huntress_attack.play()
                    elif self.personaje_actual == 1:
                        self.sound_soulhunter_attack.play()
                elif event.key == K_c:
                    self.cambiar_personaje()
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.movimiento_derecha = False
                elif event.key == K_LEFT:
                    self.movimiento_izquierda = False
                elif event.key == K_SPACE:
                    self.saltar = False
                elif event.key == K_a:
                    self.ataque = False


    def cambiar_personaje(self):
            self.personaje_actual = (self.personaje_actual + 1) % len(self.characters)
            self.resistencia = 4
            self.cambio_personaje_realizado = True  # Marcar el cambio de personaje como realizado


    def obtener_imagen_personaje_actual(self):
        return self.characters[self.personaje_actual]


    def recibir_golpe(self):
        if self.resistencia > 0:
            self.resistencia -= 1
        if self.resistencia == 0 and not self.cambio_personaje_realizado:
            self.vidas -= 1
            if self.vidas > 0:
                self.cambiar_personaje()
            else:
                self.resetear_juego()


    def resetear_juego(self):
        self.personaje_actual = 0
        self.vidas = 3
        self.resistencia = 4
        self.cambio_personaje_realizado = False

    def calcular_puntos(self):
        puntos_por_vida = 250
        puntos_por_resistencia = 150
        total_puntos = self.vidas * puntos_por_vida + self.resistencia * puntos_por_resistencia + self.puntos
        return total_puntos
