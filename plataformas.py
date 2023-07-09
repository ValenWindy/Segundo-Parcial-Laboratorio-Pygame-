import pygame

class Plataformas:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.lista_plataformas = []

        imagen_plataforma1 = pygame.image.load('Platform/groundIce1.png')
        imagen_plataforma2 = pygame.image.load('Platform/groundIce2.png')
        imagen_plataforma3 = pygame.image.load('Platform/groundIce3.png')

        imagen_plataforma1 = pygame.transform.scale(imagen_plataforma1, (100, 100))
        imagen_plataforma2 = pygame.transform.scale(imagen_plataforma2, (100, 100))
        imagen_plataforma3 = pygame.transform.scale(imagen_plataforma3, (100, 100))

        plataforma_grande_izquierda = pygame.Surface((300, 100))
        plataforma_grande_izquierda.blit(imagen_plataforma1, (0, 0))
        plataforma_grande_izquierda.blit(imagen_plataforma2, (100, 0))
        plataforma_grande_izquierda.blit(imagen_plataforma3, (200, 0))
        self.plataforma_grande_izquierda_rect = plataforma_grande_izquierda.get_rect(topleft=(0, 200))
        self.plataforma_grande_izquierda_top_left = self.plataforma_grande_izquierda_rect.topleft
        self.plataforma_grande_izquierda_top_right = self.plataforma_grande_izquierda_rect.topright

        plataforma_grande_derecha = pygame.Surface((300, 100))
        plataforma_grande_derecha.blit(imagen_plataforma1, (0, 0))
        plataforma_grande_derecha.blit(imagen_plataforma2, (100, 0))
        plataforma_grande_derecha.blit(imagen_plataforma3, (200, 0))
        self.plataforma_grande_derecha_rect = plataforma_grande_derecha.get_rect(topright=(800, 300))
        self.plataforma_grande_derecha_top_left = self.plataforma_grande_derecha_rect.topleft
        self.plataforma_grande_derecha_top_right = self.plataforma_grande_derecha_rect.topright

        self.lista_plataformas.append(self.plataforma_grande_izquierda_rect)
        self.lista_plataformas.append(self.plataforma_grande_derecha_rect)

    def crear_plataforma(self, x, y, width, height):
        plataforma_rect = pygame.Rect(x, y, width, height)
        self.lista_plataformas.append(plataforma_rect)

    def dibujar_plataformas(self):
        imagen_plataforma_grande_izquierda = pygame.image.load('Platform/groundIce1.png')
        imagen_plataforma_grande_derecha = pygame.image.load('Platform/groundIce1.png')

        imagen_plataforma_grande_izquierda = pygame.transform.scale(imagen_plataforma_grande_izquierda, (300, 100))
        imagen_plataforma_grande_derecha = pygame.transform.scale(imagen_plataforma_grande_derecha, (300, 100))

        self.screen.blit(imagen_plataforma_grande_izquierda, self.plataforma_grande_izquierda_rect)
        self.screen.blit(imagen_plataforma_grande_derecha, self.plataforma_grande_derecha_rect)

        for plataforma in self.lista_plataformas:
            pygame.draw.rect(self.screen, (0, 255, 0), plataforma, 2)
        return self.lista_plataformas

    def obtener_plataforma_actual(self, personaje_rect):
        for plataforma in self.lista_plataformas:
            if personaje_rect.colliderect(plataforma):
                lado_izquierdo = plataforma.left
                lado_derecho = plataforma.right
                limite_superior = plataforma.top
                limite_inferior = plataforma.bottom

                return plataforma
        return None

    def obtener_plataforma_superior(self):
        plataforma_superior = None
        for plataforma in self.lista_plataformas:
            if plataforma_superior is None or plataforma.top < plataforma_superior.top:
                plataforma_superior = plataforma
        return plataforma_superior
