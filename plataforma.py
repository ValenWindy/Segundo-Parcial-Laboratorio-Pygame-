import pygame

class Plataforma:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0)  # Color verde para la plataforma

    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)