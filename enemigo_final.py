import pygame
import random
from pygame.locals import *
from animacion_boss import animacion_jefe

class Jefe:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.posicion_x = self.SCREEN_WIDTH - 100
        self.posicion_y_inicial = self.SCREEN_HEIGHT // 2 - 100  # Posición y centrada en la mitad de la pantalla
        self.posicion_y = self.posicion_y_inicial
        self.valor = 2000
        self.escala = 200
        self.resistencia = 15
        self.animacion_quieto = [pygame.transform.scale(imagen, (self.escala, self.escala)) for imagen in animacion_jefe['quieto']]
        self.animacion_ataque = [pygame.transform.scale(imagen, (self.escala, self.escala)) for imagen in animacion_jefe['ataque']]
        self.animacion_habilidad = [pygame.transform.scale(imagen, (self.escala, self.escala)) for imagen in animacion_jefe['habilidad']]
        self.indice_animacion = 0
        self.imagen_actual = self.animacion_quieto[self.indice_animacion]
        self.direccion = 1  # Dirección inicial 1 para que no esté volteado al inicio
        self.tamano_rectangulo = (self.escala, self.escala)
        self.jefe_rect = pygame.Rect(self.posicion_x, self.posicion_y, *self.tamano_rectangulo)
        self.velocidad_x = 3  # Velocidad horizontal del jefe
        self.velocidad_y = 3  # Velocidad vertical del jefe
        self.ticks_quieto = 120  # Tiempo que el jefe estará en estado quieto
        self.ticks_ataque = 60  # Duración del ataque
        self.ticks_habilidad = 90  # Duración de la habilidad
        self.ticks_estado_actual = 0
        self.estado_actual = 'quieto'  # Estado inicial del jefe

    def actualizar_animacion(self, animacion):
        self.indice_animacion += 1
        if self.indice_animacion >= len(animacion):
            self.indice_animacion = 0
        self.imagen_actual = animacion[self.indice_animacion]

    def actualizar_jefe(self):
        if self.estado_actual == 'quieto':
            self.ticks_estado_actual += 1
            if self.ticks_estado_actual >= self.ticks_quieto:
                self.ticks_estado_actual = 0
                # Determinar el siguiente estado aleatoriamente (ataque o habilidad)
                siguiente_estado = random.choice(['ataque', 'habilidad'])
                if siguiente_estado == 'ataque':
                    self.estado_actual = 'ataque'
                    # Agregar lógica específica de ataque aquí
                elif siguiente_estado == 'habilidad':
                    self.estado_actual = 'habilidad'
                    # Agregar lógica específica de habilidad aquí
        elif self.estado_actual == 'ataque':
            self.ticks_estado_actual += 1
            if self.ticks_estado_actual >= self.ticks_ataque:
                self.ticks_estado_actual = 0
                self.estado_actual = 'quieto'
                # Agregar lógica para regresar al estado quieto después del ataque
        elif self.estado_actual == 'habilidad':
            self.ticks_estado_actual += 1
            if self.ticks_estado_actual >= self.ticks_habilidad:
                self.ticks_estado_actual = 0
                self.estado_actual = 'quieto'
                # Agregar lógica para regresar al estado quieto después de la habilidad

        # Actualizar la posición del jefe
        self.posicion_x += self.velocidad_x * self.direccion
        self.posicion_y += self.velocidad_y

        # Verificar límites de la pantalla para invertir la dirección del jefe
        if self.posicion_x <= 0 or self.posicion_x >= self.SCREEN_WIDTH - self.escala:
            self.direccion *= -1

        # Actualizar la posición y rectángulo del jefe
        self.jefe_rect.x = self.posicion_x
        self.jefe_rect.y = self.posicion_y

    def dibujar_jefe(self):
        if self.direccion == -1:
            imagen_volteada = pygame.transform.flip(self.imagen_actual, True, False)
            self.screen.blit(imagen_volteada, self.jefe_rect)
        else:
            self.screen.blit(self.imagen_actual, self.jefe_rect)

        self.actualizar_animacion(self.animacion_quieto)
        self.actualizar_jefe()

