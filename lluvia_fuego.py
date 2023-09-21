import pygame
import random

class Lluvia:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.fuego_imagen = pygame.image.load("Tramps/Lluvia_Fuego.png")
        self.fuego_imagen = pygame.transform.scale(self.fuego_imagen, (100, 100))  # Redimensionar la imagen
        self.lista_fuegos = []

    def crear_fuego(self):
        x = random.randint(0, self.SCREEN_WIDTH - self.fuego_imagen.get_width())
        y = random.randint(-self.SCREEN_HEIGHT, 0)
        velocidad = random.randint(3, 10)
        fuego = {
            "imagen": self.fuego_imagen,
            "rect": pygame.Rect(x, y, self.fuego_imagen.get_width(), self.fuego_imagen.get_height()),
            "velocidad": velocidad
        }
        self.lista_fuegos.append(fuego)

    def mover_fuegos(self):
        for fuego in self.lista_fuegos:
            fuego["rect"].y += fuego["velocidad"]
            if fuego["rect"].y > self.SCREEN_HEIGHT:
                fuego["rect"].y = random.randint(-self.SCREEN_HEIGHT, 0)
                fuego["rect"].x = random.randint(0, self.SCREEN_WIDTH - self.fuego_imagen.get_width())

    def dibujar_fuegos(self, screen):
        for fuego in self.lista_fuegos:
            screen.blit(fuego["imagen"], fuego["rect"])
