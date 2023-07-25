import pygame
from animacion_proyectiles import fire_ball

class Proyectil:
    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.ancho = 20  # Ajusta el ancho del proyectil según tus necesidades
        self.alto = 20  # Ajusta el alto del proyectil según tus necesidades
        self.animacion_moverse = [pygame.transform.scale(imagen, (self.ancho, self.alto)) for imagen in fire_ball['moverse']]
        self.animacion_actual = 'moverse'
        self.indice_animacion = 0
        self.imagen_actual = self.animacion_moverse[self.indice_animacion]
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def actualizar(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.actualizar_animacion()

    def actualizar_animacion(self):
        tiempo_cambio = 100  # Número de frames para cambiar de imagen (1.67 segundos a 60 FPS)
        tiempo_actual = pygame.time.get_ticks()  # Tiempo actual del juego en milisegundos

        self.indice_animacion = (tiempo_actual // tiempo_cambio) % len(self.animacion_moverse)
        self.imagen_actual = self.animacion_moverse[self.indice_animacion]

    def dibujar(self, screen):
        screen.blit(self.imagen_actual, self.rect)
        pygame.draw.rect(screen, (0, 255, 0), self.rect)