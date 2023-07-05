import pygame
from movimientos_enemigos import animacion_enemigo

class Enemigos:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.posicion_x = self.SCREEN_WIDTH - 100
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_y = self.posicion_y_inicial
        self.valor = 200
        self.velocidad = 2
        self.animacion_moverse = animacion_enemigo['moverse']
        self.indice_animacion = 0
        self.imagen_original = self.animacion_moverse[self.indice_animacion]
        self.imagen_volteada = pygame.transform.flip(self.imagen_original, True, False)
        self.imagen_actual = self.imagen_original
        self.direccion = -1  # -1 para moverse hacia la izquierda, 1 para moverse hacia la derecha
        self.tamano_rectangulo = (100, 100)
        self.enemigo_rect = pygame.Rect(self.posicion_x, self.posicion_y, *self.tamano_rectangulo)
        self.lista_enemigos = []  # Lista de enemigos
        

    def crear_enemigo(self):
        nuevo_enemigo = Enemigos()  # Crear un nuevo enemigo
        self.lista_enemigos.append(nuevo_enemigo)  # Agregar el enemigo a la lista

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
        if self.posicion_x <= 0 or self.posicion_x >= self.SCREEN_WIDTH - self.enemigo_rect.width:
            self.direccion *= -1
        self.enemigo_rect.x = self.posicion_x

    def actualizar_enemigos(self):
        for enemigo in self.lista_enemigos:
            enemigo.actualizar_animacion()
            enemigo.actualizar_posicion()

    def dibujar_enemigos(self):
        for enemigo in self.lista_enemigos:
            pygame.draw.rect(self.screen, (0, 255, 255), enemigo.enemigo_rect, 2)
            self.screen.blit(pygame.transform.scale(enemigo.imagen_actual, enemigo.tamano_rectangulo), enemigo.enemigo_rect)
