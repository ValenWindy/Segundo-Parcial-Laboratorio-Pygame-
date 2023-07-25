import pygame
import random
from animacion_boss import animacion_jefe


class Jefe:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.posicion_x = random.randint(0, self.SCREEN_WIDTH - 200)  # Posición x aleatoria
        self.posicion_y = random.randint(0, self.SCREEN_HEIGHT - 200)  # Posición y aleatoria
        self.escala = 200
        self.animacion_quieto = [pygame.transform.scale(imagen, (self.escala, self.escala)) for imagen in animacion_jefe['quieto']]
        self.animacion_ataque = [pygame.transform.scale(imagen, (self.escala, self.escala)) for imagen in animacion_jefe['ataque']]
        self.animacion_actual = 'quieto'
        self.tiempo_animacion = 0
        self.indice_animacion = 0
        self.resistencia = 5
        self.inmunidad = False
        self.inicio_inmunidad = 0
        self.valor = 5000
        self.direccion_x = random.choice([-1, 1])
        self.direccion_y = random.choice([-1, 1])
        self.velocidad_x = random.uniform(5, 7)  # Velocidad horizontal aleatoria
        self.velocidad_y = random.uniform(5, 7)  # Velocidad vertical aleatoria
        self.imagen_actual = self.animacion_quieto[self.indice_animacion]
        self.tamano_rectangulo = (self.escala, self.escala)
        self.jefe_rect = pygame.Rect(self.posicion_x, self.posicion_y, *self.tamano_rectangulo)
        self.lista_jefe = []
        self.proyectil_rect = pygame.Rect(0, 0, 40, 40)
        self.proyectil_ancho = 40  # Ajusta el ancho del proyectil según tus necesidades
        self.proyectil_alto = 40  # Ajusta el alto del proyectil según tus necesidades
        self.proyectil_velocidad = 5  # Ajusta la velocidad del proyectil según tus necesidades

    def crear_jefe(self):
        nuevo_jefe = Jefe()
        nuevo_jefe.posicion_x = random.randint(0, self.SCREEN_WIDTH - 200)
        nuevo_jefe.posicion_y = random.randint(0, self.SCREEN_HEIGHT - 200)
        self.lista_jefe.append(nuevo_jefe)
        return nuevo_jefe

    def actualizar_animacion(self):
        tiempo_cambio = 150
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual // tiempo_cambio % 2 == 0:
            self.animacion_actual = "quieto"
            self.indice_animacion = (tiempo_actual // tiempo_cambio // 2) % len(self.animacion_quieto)
            self.imagen_actual = self.animacion_quieto[self.indice_animacion]
        else:
            self.animacion_actual = "ataque"
            self.indice_animacion = (tiempo_actual // tiempo_cambio // 2) % len(self.animacion_ataque)
            self.imagen_actual = self.animacion_ataque[self.indice_animacion]

    def actualizar_jefe(self):
        # Actualizar posición del jefe
        self.posicion_x += self.velocidad_x * self.direccion_x
        self.posicion_y += self.velocidad_y * self.direccion_y

        # Verificar límites de la pantalla
        if self.posicion_x <= 0 or self.posicion_x >= self.SCREEN_WIDTH - self.escala:
            self.direccion_x *= -1

        if self.posicion_y <= 0 or self.posicion_y >= self.SCREEN_HEIGHT - self.escala:
            self.direccion_y *= -1

        # Actualizar la posición y rectángulo del jefe
        self.jefe_rect.x = self.posicion_x
        self.jefe_rect.y = self.posicion_y

        # Actualizar animación
        self.actualizar_animacion()

        # Actualizar proyectil
        if self.proyectil_rect is not None:
            self.actualizar_proyectil()

    def recibir_golpe_enemigo(self):
        if self.resistencia > 0:
            self.resistencia -= 1

    def actualizar_resistencia_enemigo(self):
        if self.resistencia <= 0:
            self.resistencia = 0
            for jefe in self.lista_jefe:
                if jefe == self:
                    self.lista_jefe.remove(jefe)
                    break

    def kill(self):
        for jefe in self.lista_jefe:
            if jefe == self:
                self.lista_jefe.remove(jefe)
                break

    def dibujar_jefe(self):
        if self.jefe_rect is None:
            return

        self.actualizar_jefe()

        if self.direccion_x == -1:
            imagen_volteada = pygame.transform.flip(self.imagen_actual, True, False)
            self.screen.blit(imagen_volteada, self.jefe_rect)
        else:
            self.screen.blit(self.imagen_actual, self.jefe_rect)

        # Lanzar proyectil
        if self.proyectil_rect is None:
            self.lanzar_proyectil()

        # Dibujar proyectil
        if self.proyectil_rect is not None:
            proyectil_imagen = pygame.transform.scale(pygame.image.load("Tramps/Fire_Ball_0.png"), (40, 40))  # Ajusta el tamaño de la imagen según tus necesidades

            if self.proyectil_velocidad > 0:
                proyectil_imagen = pygame.transform.flip(proyectil_imagen, True, False)

            self.screen.blit(proyectil_imagen, self.proyectil_rect)

    def lanzar_proyectil(self):
        proyectil_x = self.posicion_x + self.escala // 2
        proyectil_y = self.posicion_y + self.escala // 2

        self.proyectil_direccion = random.choice([-1, 1])
        self.proyectil_velocidad = self.proyectil_direccion * self.velocidad_x

        self.proyectil_rect = pygame.Rect(proyectil_x, proyectil_y, self.proyectil_ancho, self.proyectil_alto)

    def actualizar_proyectil(self):
        self.proyectil_rect.x += self.proyectil_velocidad

        # Verificar si el proyectil ha salido de la pantalla
        if self.proyectil_rect.right < 0 or self.proyectil_rect.left > self.SCREEN_WIDTH:
            self.proyectil_rect = None
