import random
import pygame
import time
from pygame.locals import *
from plataformas import Plataformas

class Frutas:
    def __init__(self):
        self.imagenes = []
        self.plataformas = Plataformas()
        self.cargar_imagenes()
        self.tipo = ""
        self.lista_frutas = []  # Lista para almacenar las frutas generadas
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.sound_banana = pygame.mixer.Sound("Music/Banana.wav")
        self.sound_apple = pygame.mixer.Sound("Music/Apple.wav")
        self.tiempo_anterior = time.time()
        self.intervalo = 15  # Intervalo de tiempo en segundos

    def cargar_imagenes(self):
        self.imagenes.append((pygame.image.load("Frutas/Apple.png"), "Manzana"))
        self.imagenes.append((pygame.image.load("Frutas/Banana.png"), "Banana"))

        # Redimensionar las imágenes de las frutas
        for i in range(len(self.imagenes)):
            imagen, tipo = self.imagenes[i]
            self.imagenes[i] = (pygame.transform.scale(imagen, (50, 50)), tipo)

    def generar_frutas(self):
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_anterior

        if tiempo_transcurrido >= self.intervalo:
            fruta = self.generar_fruta()
            self.lista_frutas.append(fruta)
            self.tiempo_anterior = tiempo_actual

    def generar_fruta(self):
        imagen, tipo = random.choice(self.imagenes)
        posicion = self.generar_posicion()
        rect = pygame.Rect(posicion[0], posicion[1], 50, 50)
        return {"imagen": imagen, "tipo": tipo, "posicion": posicion, "rect": rect}

    def generar_posicion(self):
        plataforma_izquierda_rect = self.plataformas.plataforma_grande_izquierda_rect
        plataforma_derecha_rect = self.plataformas.plataforma_grande_derecha_rect

        x_izquierda = random.randint(plataforma_izquierda_rect.left, plataforma_izquierda_rect.right)
        y_izquierda = random.randint(plataforma_izquierda_rect.top - 100, plataforma_izquierda_rect.bottom - 100)

        x_derecha = random.randint(plataforma_derecha_rect.left, plataforma_derecha_rect.right)
        y_derecha = random.randint(plataforma_derecha_rect.top - 100, plataforma_derecha_rect.bottom - 100)

        # Elegir aleatoriamente entre la plataforma izquierda y la plataforma derecha
        if random.random() < 0.5:
            return (x_izquierda, y_izquierda)
        else:
            return (x_derecha, y_derecha)



    def dibujar_fruta(self):
        for fruta in self.lista_frutas:
            self.screen.blit(fruta["imagen"], fruta["posicion"])
            # pygame.draw.rect(self.screen, (255, 0, 0), fruta["rect"], 2)

