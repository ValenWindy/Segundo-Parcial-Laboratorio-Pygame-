import pygame
import random
from pygame.locals import *
from movimientos_enemigos import animacion_enemigo
from plataformas import Plataformas

class Enemigos:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.posicion_x_inicial = self.SCREEN_WIDTH - 100
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_x = self.posicion_x_inicial
        self.posicion_y = self.posicion_y_inicial
        self.velocidad = 6
        self.valor = 250
        self.animacion_moverse = animacion_enemigo['moverse']
        self.indice_animacion = 0
        self.imagen_original = self.animacion_moverse[self.indice_animacion]
        self.imagen_volteada = pygame.transform.flip(self.imagen_original, True, False)
        self.imagen_actual = self.imagen_original
        self.direccion_inicial = -1  # -1 para moverse hacia la izquierda, 1 para moverse hacia la derecha
        self.direccion = self.direccion_inicial
        self.tamano_rectangulo = (100, 100)
        self.plataformas = Plataformas()
        self.enemigo_rect = pygame.Rect(self.posicion_x, self.posicion_y, *self.tamano_rectangulo)
        self.lista_enemigos_suelo = []  
        # self.sound_death = pygame.mixer.Sound ("Music/Zombie_Death.WAV")

    def crear_enemigo_suelo(self):
        nuevo_enemigo = Enemigos()
        nuevo_enemigo.posicion_x = nuevo_enemigo.posicion_x_inicial
        nuevo_enemigo.posicion_y = nuevo_enemigo.posicion_y_inicial
        self.lista_enemigos_suelo.append(nuevo_enemigo)
        return nuevo_enemigo



    def actualizar_animacion(self):
        self.indice_animacion += 1
        if self.indice_animacion >= len(self.animacion_moverse):
            self.indice_animacion = 0
        self.imagen_original = self.animacion_moverse[self.indice_animacion]
        self.imagen_volteada = pygame.transform.flip(self.imagen_original, True, False)
        if self.direccion == -1:
            self.imagen_actual = self.imagen_volteada
        else:
            self.imagen_actual = self.imagen_original

    def actualizar_posicion(self):
        self.posicion_x += self.velocidad * self.direccion
        if self.direccion == -1 and self.posicion_x <= 0:
            self.direccion = 1  # Cambiar la dirección a la derecha
        elif self.direccion == 1 and self.posicion_x >= self.SCREEN_WIDTH - self.enemigo_rect.width:
            self.direccion = -1  # Cambiar la dirección a la izquierda
        self.enemigo_rect.x = self.posicion_x

    def actualizar_enemigos(self):
        for enemigo in self.lista_enemigos_suelo:
            enemigo.actualizar_animacion()
            enemigo.actualizar_posicion()

            # Verificar si el enemigo ha dado 30 pasos
            if abs(enemigo.posicion_x - enemigo.posicion_x_inicial) >= 30 * enemigo.velocidad:
                # Cambiar aleatoriamente la dirección del enemigo
                enemigo.direccion = random.choice([-1, 1])
                enemigo.posicion_x_inicial = enemigo.posicion_x

                # Actualizar la imagen del enemigo en función de la dirección
                if enemigo.direccion == -1:
                    enemigo.imagen_actual = enemigo.imagen_volteada
                else:
                    enemigo.imagen_actual = enemigo.imagen_original

                    
    def dibujar_enemigos(self):
        for enemigo in self.lista_enemigos_suelo:
            self.screen.blit(pygame.transform.scale(enemigo.imagen_actual, enemigo.tamano_rectangulo), enemigo.enemigo_rect)
        