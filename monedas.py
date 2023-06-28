import random
import pygame

class Moneda:
    def __init__(self, limite_x, limite_y):
        self.imagenes = []
        self.cargar_imagenes()
        self.imagen_actual = self.imagenes[0]
        self.posicion = self.generar_posicion(limite_x, limite_y)
        self.tipo = ""

    def cargar_imagenes(self):
        self.imagenes.append(pygame.image.load("Coins/Bronze/Bronze_10.png"))
        self.imagenes.append(pygame.image.load("Coins/Gold/Gold_20.png"))
        self.imagenes.append(pygame.image.load("Coins/Silver/Silver_30.png"))

    def cambiar_imagen(self, indice):
        self.imagen_actual = self.imagenes[indice]

    def generar_posicion(self, limite_x, limite_y):
        # Genera una posición aleatoria dentro de los límites del escenario
        x = random.randint(0, limite_x)
        y = random.randint(0, limite_y)
        return (x, y)

    def posicion_actual(self):
        return self.posicion

    def colision_personajes(self, personajes):
        # Verificar colisión con el personaje
        if pygame.Rect(personajes.posicion_actual(), personajes.imagen_actual.get_size()).colliderect(
                pygame.Rect(self.posicion_actual(), self.imagen_actual.get_size())):
            if self.tipo == "bronce":
                personajes.puntos += 100
            elif self.tipo == "plata":
                personajes.resistencia += 1
            elif self.tipo == "oro":
                personajes.vidas += 1
            return True
        return False