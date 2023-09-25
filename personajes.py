import pygame
import sys
import time
import keyboard
import threading
from pygame.locals import *
from movimientos import animaciones_personaje_1, animaciones_personaje_2
from plataformas import Plataformas


class Personajes:
    def __init__(self):
        self.characters = [animaciones_personaje_1, animaciones_personaje_2]
        self.personaje_actual = 0
        self.plataformas = Plataformas()
        self.puntos = 0
        self.vidas = 1
        self.resistencia = 4
        self.inmunidad = False  
        self.inicio_inmunidad = 0
        self.contador_salto = 0
        self.cambio_personaje_realizado = False
        self.velocidad_movimiento = 10
        self.movimiento_derecha = False
        self.movimiento_izquierda = False
        self.ataque = False
        self.saltar = False
        self.personaje_imagen = None
        self.posicion_x = 100
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_y = self.posicion_y_inicial
        self.direccion_personaje = "derecha"
        self.velocidad_salto = 30
        self.altura_salto = 300
        self.gravedad = 1.5
        self.velocidad_animacion = 0.2
        self.frame_actual = 0
        self.max_saltos = 0
        self.velocidad_vertical = 0
        self.velocidad_horizontal = 0
        self.piso_x = 100  
        self.piso_y = self.SCREEN_HEIGHT - 100 
        self.plataforma_piso_rect = pygame.Rect(0, self.piso_y, self.posicion_x, 20)
        self.rectangulo_ataque_personaje_2 = pygame.Rect(0, 0, 100, 50)
        self.rectangulo_flecha = pygame.Rect(100, 100, 200, 100)  
        self.punto = (150, 150) 
        self.rectangulo_punto = pygame.Rect(self.punto, (1, 1))
        self.flecha_posicion = None
        self.en_suelo = True
        # self.sound_huntress_attack = pygame.mixer.Sound("Music/Arrow.wav")
        # self.sound_soulhunter_attack = pygame.mixer.Sound("Music/Sword.wav")
        # self.sound_huntress_hit = pygame.mixer.Sound("Music/Huntress-Hit.WAV")
        # self.sound_soulhunter_hit = pygame.mixer.Sound("Music/Soulhunter-Hit.wav")
        # self.sound_jump = pygame.mixer.Sound("Music/Jump.mp3")

        pygame.font.init()

        self.personaje_rect = pygame.Rect(
            self.posicion_x,
            self.posicion_y,
            100,
            100  
        )

        self.top_personaje = self.personaje_rect.top
        self.bottom_personaje = self.personaje_rect.bottom
        self.left_personaje = self.personaje_rect.left
        self.right_personaje = self.personaje_rect.right


    def actualizar_posicion_y(self):
        if self.saltar:
            if self.posicion_y > self.posicion_y_inicial - 100:
                self.posicion_y -= 5  
            else:
                self.saltar = False
                self.posicion_y = self.posicion_y_inicial
                self.en_suelo = True

    def actualizar_salto(self):
        if self.saltar and self.en_suelo:
            self.en_suelo = False
            self.altura_inicial = self.posicion_y
            self.velocidad_vertical = -self.velocidad_salto
            self.contador_salto += 1

        if not self.en_suelo:
            self.velocidad_vertical += self.gravedad

            # Verificar colisión con las plataformas
            plataforma_actual = self.plataformas.obtener_plataforma_actual(self.personaje_rect)
            if plataforma_actual is not None:
                if self.velocidad_vertical > 0 and self.personaje_rect.colliderect(plataforma_actual) and self.posicion_y >= plataforma_actual.top - self.personaje_rect.height:
                    self.posicion_y = plataforma_actual.top - self.personaje_rect.height
                    self.velocidad_vertical = 0
                    self.en_suelo = True
                    self.contador_salto = 0  # Reiniciar el contador de saltos
                elif self.velocidad_vertical < 0 and self.posicion_y <= plataforma_actual.bottom:
                    self.posicion_y = plataforma_actual.bottom
                    self.velocidad_vertical = self.gravedad  # Aplicar gravedad si el personaje supera la plataforma
                elif self.velocidad_vertical > 0 and self.personaje_rect.colliderect(plataforma_actual) and self.personaje_rect.bottom >= plataforma_actual.top:
                    self.posicion_y = plataforma_actual.top - self.personaje_rect.height
                    self.velocidad_vertical = 0
                    self.en_suelo = True
                    self.contador_salto = 0  # Reiniciar el contador de saltos
                elif self.velocidad_vertical > 0 and plataforma_actual.top is not None:
                    self.velocidad_vertical = self.gravedad

                # Verificar colisión en posición x con el top de la plataforma
                if self.posicion_x <= plataforma_actual.right and self.posicion_x >= plataforma_actual.left:
                    if self.posicion_y >= plataforma_actual.top - self.personaje_rect.height:
                        self.posicion_y += self.velocidad_vertical
                        self.velocidad_vertical += self.gravedad
                    else:
                        # El personaje ha superado la plataforma, caer
                        self.posicion_y += self.velocidad_vertical
                        self.velocidad_vertical += self.gravedad
                        self.en_suelo = False
                else:
                    # El personaje ha superado la plataforma en el eje x, caer
                    self.en_suelo = False

            else:
                # Actualizar la posición vertical del personaje
                self.posicion_y += self.velocidad_vertical

                # Verificar si el personaje ha caído al suelo
                if self.posicion_y >= self.piso_y:
                    self.posicion_y = self.piso_y
                    self.en_suelo = True
                    self.velocidad_vertical = 0
                    self.contador_salto = 0


    def dibujar_personaje(self):

        accion_actual = 'quieto'
        if self.movimiento_derecha or self.movimiento_izquierda:
            accion_actual = 'correr'
        if self.saltar and self.en_suelo:
            accion_actual = 'saltar'
        if self.ataque:
            accion_actual = 'atacar'

        if self.movimiento_derecha and self.posicion_x < self.SCREEN_WIDTH - self.velocidad_movimiento:
            self.posicion_x += self.velocidad_movimiento
        elif self.movimiento_izquierda and self.posicion_x > 0:
            self.posicion_x -= self.velocidad_movimiento

        # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, self.piso_y - 20, self.SCREEN_WIDTH, 20))

        self.frame_actual = (self.frame_actual + 1) % len(self.obtener_imagen_personaje_actual()[accion_actual])
        imagen_actual = self.obtener_imagen_personaje_actual()[accion_actual][self.frame_actual]
        if self.movimiento_izquierda:
            imagen_actual = pygame.transform.flip(imagen_actual, True, False)
        imagen_redimensionada = pygame.transform.scale(imagen_actual, (100, 100))
        self.screen.blit(imagen_redimensionada, (self.posicion_x, self.posicion_y))
        self.rectangulo_flecha.x += self.velocidad_movimiento * 2
        self.actualizar_flecha()
        self.dibujar_flecha()

        if self.ataque and self.personaje_actual == 1: 
            if self.direccion_personaje == "derecha":
                self.rectangulo_ataque_personaje_2.left = self.personaje_rect.right
            else:
                self.rectangulo_ataque_personaje_2.right = self.personaje_rect.left

            self.rectangulo_ataque_personaje_2.centery = self.personaje_rect.centery

        self.personaje_rect = pygame.Rect(self.posicion_x, self.posicion_y, 100, 100)

    

            

    def cambiar_personaje(self):
        self.personaje_actual = (self.personaje_actual + 1) % len(self.characters)
        self.cambio_personaje_realizado = True 


    def obtener_imagen_personaje_actual(self):
        self.personaje_imagen = self.characters[self.personaje_actual].get('personaje')
        return self.characters[self.personaje_actual]

    
    def recibir_golpe(self):
        if self.resistencia > 0:
            self.resistencia -= 1

    def actualizar_vidas(self):
        if self.resistencia <= 0:
            self.vidas -= 1
            self.resistencia = 3

    def actualizar_resistencia(self):
        if self.resistencia < 0:
            self.resistencia = 0


    def actualizar_flecha(self):
        if self.ataque and not self.flecha_posicion and self.personaje_actual == 0:
            self.flecha_posicion = list(self.personaje_rect.center) 

        if self.flecha_posicion:
            x, y = self.flecha_posicion  
            self.rectangulo_flecha.center = self.flecha_posicion

            if self.direccion_personaje == "derecha":
                x += self.velocidad_movimiento * 2 
            else:
                x -= self.velocidad_movimiento * 2 

            self.flecha_posicion = [x, y]  

            if self.flecha_posicion[0] > self.SCREEN_WIDTH or self.flecha_posicion[0] < 0:
                self.flecha_posicion = None  
            


    def dibujar_flecha(self):
        if self.flecha_posicion:
            flecha_imagen = self.obtener_imagen_personaje_actual()['flecha']
            flecha_redimensionada = pygame.transform.scale(flecha_imagen[0], (48, 48))
            self.flecha_rect = flecha_redimensionada.get_rect()
            self.flecha_rect.center = self.flecha_posicion

            # Dibujar el rectángulo de la flecha
            # pygame.draw.rect(self.screen, (255, 0, 0), self.flecha_rect, 2)


            self.screen.blit(flecha_redimensionada, self.flecha_posicion)

    def calcular_puntos(self, puntos):
            puntos_por_vida = 250
            puntos_por_resistencia = 150
            total_puntos = self.vidas * puntos_por_vida + self.resistencia * puntos_por_resistencia + puntos
            return total_puntos