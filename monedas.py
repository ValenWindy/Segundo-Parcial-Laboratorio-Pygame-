import random
from pygame.locals import *
import pygame


class Monedas:
    def __init__(self):
        self.imagenes = []
        self.cargar_imagenes()
        self.imagen_actual = self.imagenes[0]
        self.posicion = self.generar_posicion()
        self.tipo = ""
        self.sound_coin = pygame.mixer.Sound("Music/Coin.wav")
        

    def cargar_imagenes(self):
        self.imagenes.append((pygame.image.load("Coins/Bronze/Bronze_10.png"), "Bronce", 100))
        self.imagenes.append((pygame.image.load("Coins/Silver/Silver_30.png"), "Plata", 200))
        self.imagenes.append((pygame.image.load("Coins/Gold/Gold_20.png"), "Oro", 300))

        # Redimensionar las imágenes de las monedas
        for i in range(len(self.imagenes)):
            imagen, _, _ = self.imagenes[i]
            self.imagenes[i] = (pygame.transform.scale(imagen, (30, 30)), self.imagenes[i][1], self.imagenes[i][2])


    def cambiar_imagen(self, indice):
        self.imagen_actual = self.imagenes[indice]
        self.redimensionar_imagen(30, 30)  # Redimensionar la imagen de la moneda

    def generar_posicion(self):
        x = random.randint(0, pygame.display.Info().current_w)
        y = random.randint(0, pygame.display.Info().current_h)
        return (x, y)

    def posicion_actual(self):
        return self.posicion


    def redimensionar_imagen(self, ancho, alto):
        imagen = self.imagen_actual[0]
        imagen_redimensionada = pygame.transform.scale(imagen, (ancho, alto))
        self.imagen_actual = (imagen_redimensionada, self.imagen_actual[1], self.imagen_actual[2])

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_actual, self.posicion)
