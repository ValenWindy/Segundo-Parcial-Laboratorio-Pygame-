import pygame
import sys
import time
import random
from personajes import Personajes



class Texto:
    def __init__(self, nivel, personajes):
        self.nivel = nivel
        self.personajes = personajes
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font_inicio = pygame.font.Font(self.font_path, self.font_size)
        self.texto_inicio = self.font_inicio.render(f"Nivel {nivel}", True, (255, 255, 255))
        self.texto_inicio_rect = self.texto_inicio.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.animacion_inicio_tiempo = 3
        self.animacion_inicio_finalizado = False
        self.puntaje = 0
        self.tiempo_inicial = time.time()
        self.duracion_nivel = 33
        self.tiempo_transcurrido = 0
        self.animacion_inicio_inicial = time.time()
        self.personajes = Personajes()
        
    
    

    
    def formato_tiempo(self, tiempo_restante):
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        return f"{minutos:02d}:{segundos:02d}"

    def dibujar_puntaje(self, puntos, vidas, resistencia):
        font = pygame.font.Font(None, 36)
        texto_puntaje = font.render("Puntaje: " + str(puntos), True, (255, 255, 255))
        texto_vidas = font.render("Vidas: " + str(vidas), True, (255, 255, 255))
        texto_resistencia = font.render("Resistencia: " + str(resistencia), True, (255, 255, 255))
        
        self.screen.blit(texto_puntaje, (10, 10))
        self.screen.blit(texto_vidas, (self.SCREEN_WIDTH - texto_vidas.get_width() - 10, 10))
        self.screen.blit(texto_resistencia, (self.SCREEN_WIDTH - texto_resistencia.get_width() - 10, 70))



    def dibujar_tiempo_restante(self):
        font = pygame.font.Font(None, 30)
        tiempo_restante = self.duracion_nivel - (time.time() - self.tiempo_inicial)
        tiempo_restante_str = self.formato_tiempo(tiempo_restante)
        texto_tiempo_restante = font.render("Tiempo restante: " + tiempo_restante_str, True, (255, 255, 255))

        self.screen.blit(texto_tiempo_restante, (10, 70))
        


    
