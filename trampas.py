import pygame
import random
import time
from animaciones_trampas import ojo_azul, ojo_rojo

class Trampas:
    def __init__(self):
        self.ojo_rojo = ojo_rojo
        self.ojo_azul = ojo_azul
        self.velocidad = 3
        self.indice_animacion = 0
        self.direccion = -1
        self.tamano_rectangulo = (72, 72)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.ultimo_tiempo_aparicion = time.time()
        self.animacion_moverse_rojo = ojo_rojo['moverse']
        self.animacion_moverse_azul = ojo_azul['moverse']
        self.lista_trampas_rojas = []
        self.lista_trampas_azules = []

    def generar_posicion(self):
        x = self.SCREEN_WIDTH
        y = random.randint(0, self.SCREEN_HEIGHT - self.tamano_rectangulo[1])
        return x, y

    def generar_rectangulo(self, x, y, imagen):
        return pygame.Rect(x, y, *self.tamano_rectangulo), pygame.transform.scale(imagen, self.tamano_rectangulo)

    def dibujar_trampas(self):
        tiempo_actual = time.time()

        if tiempo_actual - self.ultimo_tiempo_aparicion >= 8:
            x, y = self.generar_posicion()
            
            if random.random() < 0.5 and len(self.animacion_moverse_rojo) > 0:
                trampa_rect, trampa_imagen = self.generar_rectangulo(x, y, self.animacion_moverse_rojo[self.indice_animacion % len(self.animacion_moverse_rojo)])
                trampa = {
                    'surface': trampa_rect,
                    'image': trampa_imagen
                }
                self.lista_trampas_rojas.append(trampa)
            elif len(self.animacion_moverse_azul) > 0:
                trampa_rect, trampa_imagen = self.generar_rectangulo(x, y, self.animacion_moverse_azul[self.indice_animacion % len(self.animacion_moverse_azul)])
                trampa = {
                    'surface': trampa_rect,
                    'image': trampa_imagen
                }
                self.lista_trampas_azules.append(trampa)
            
            self.ultimo_tiempo_aparicion = tiempo_actual

        for trampa in self.lista_trampas_rojas:
            trampa['surface'].move_ip(-self.velocidad, 0)
            pygame.draw.rect(self.screen, (255, 0, 0), trampa['surface'])  # Dibujar rectángulo rojo
            self.screen.blit(trampa['image'], trampa['surface'])

        for trampa in self.lista_trampas_azules:
            trampa['surface'].move_ip(-self.velocidad, 0)
            pygame.draw.rect(self.screen, (0, 0, 255), trampa['surface'])  # Dibujar rectángulo azul
            self.screen.blit(trampa['image'], trampa['surface'])
