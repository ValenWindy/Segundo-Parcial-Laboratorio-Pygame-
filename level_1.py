import pygame
import sys
import time
import random
import csv
from pygame.locals import *
from options import Options
from texto import Texto 
from personajes import Personajes
from monedas import Monedas
from plataformas import Plataformas
from level_2 import Nivel_2
from marcadores import Marcadores


class Nivel_1:
    def __init__(self, nombre_jugador):
        self.nivel = 1
        self.options = Options()
        self.personajes = Personajes()
        self.plataformas = Plataformas()
        self.texto = Texto(self.nivel, self.personajes)
        self.velocidad_caida_monedas = 2
        self.monedas = []
        self.FPS = 60
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_1.jpg").convert()
        self.titulo = pygame.display.set_caption("The Huntress and the Soulhunter")
        self.duracion_nivel = self.texto.duracion_nivel
        pygame.mixer.music.load("Music/Main Theme.wav")
        pygame.mixer.music.play(-1)
        self.nombre_jugador = nombre_jugador  
    


    def caer_monedas(self):
        if random.random() < 0.01:  
            nueva_moneda = Monedas()  
            self.monedas.append(nueva_moneda)  

        for moneda in self.monedas:
            x, y = moneda.posicion_actual()
            y += self.velocidad_caida_monedas
            moneda.posicion = (x, y)

            if y > self.SCREEN_HEIGHT:
                self.monedas.remove(moneda)

            if random.random() < 0.01:
                indice = random.randint(0, len(moneda.imagenes) - 1)
                moneda.cambiar_imagen(indice)
                moneda.redimensionar_imagen(30, 30)  

    def dibujar_monedas(self):
        for moneda in self.monedas:
            x, y = moneda.posicion
            moneda.redimensionar_imagen(30, 30)  
            imagen_moneda = moneda.imagen_actual[0]
            self.screen.blit(imagen_moneda, (x, y))


    def colision_monedas(self):
        personaje_rect = self.personajes.personaje_rect
        
        for moneda in self.monedas:
            moneda_rect = pygame.Rect(moneda.posicion_actual(), moneda.imagen_actual[0].get_size())
            if personaje_rect.colliderect(moneda_rect):
                self.personajes.puntos += moneda.imagen_actual[2]
                print(self.personajes.puntos)
                self.monedas.remove(moneda)


    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.personajes.dibujar_personaje()
        self.plataformas.dibujar_plataformas()
        self.dibujar_monedas()
        self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
        self.texto.dibujar_tiempo_restante()

    def actualizar_tiempo_transcurrido(self):
        self.texto.tiempo_transcurrido += self.clock.tick(60) / 1000.0

        if self.texto.animacion_inicio_finalizado:
            if self.texto.tiempo_transcurrido >= 3.0:
                self.screen.blit(self.fondo, (0, 0))

    def mostrar_mensaje_final(self, puntos):
        score_nivel = self.personajes.calcular_puntos(puntos)
        puntaje_total = score_nivel  
        mensaje_nivel = f"Nivel {self.nivel} completado."
        mensaje_puntos = f"Total de puntos del nivel: {score_nivel}"
        mensaje_score = f"Puntaje total: {puntaje_total}"
        
        fuente = pygame.font.Font(None, 36)
        texto_nivel = fuente.render(mensaje_nivel, True, (255, 255, 255))
        texto_puntos = fuente.render(mensaje_puntos, True, (255, 255, 255))
        texto_score = fuente.render(mensaje_score, True, (255, 255, 255))
        
        texto_nivel_rect = texto_nivel.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        texto_puntos_rect = texto_puntos.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        texto_score_rect = texto_score.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(self.fondo, (0, 0))
        self.screen.blit(texto_nivel, texto_nivel_rect)
        self.screen.blit(texto_puntos, texto_puntos_rect)
        self.screen.blit(texto_score, texto_score_rect)
        
        pygame.display.update()
        self.texto.animacion_inicio_finalizado = True
        time.sleep(3)

        marcadores = Marcadores()
        ranking = marcadores.obtener_calificacion(puntaje_total)
        marcadores.actualizar_puntaje_csv(puntaje_total, ranking, self.nombre_jugador)

        
        nivel_2 = Nivel_2(self.nombre_jugador, puntaje_total)
        nivel_2.run()




        


    def run(self):
        while True:
            self.personajes.eventos()
            self.actualizar_tiempo_transcurrido()

            if self.texto.animacion_inicio_finalizado:
                self.personajes.actualizar_salto()
                self.caer_monedas()
                self.colision_monedas()
                self.dibujar_elementos()
                
                tiempo_restante = self.duracion_nivel - (time.time() - self.texto.tiempo_inicial)
                if tiempo_restante <= 0:
                    self.mostrar_mensaje_final(self.personajes.puntos)
                    self.animacion_inicio_finalizado = True           
                    break

            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.texto.animacion_inicio_inicial
                if tiempo_transcurrido >= self.texto.animacion_inicio_tiempo:
                    self.texto.animacion_inicio_finalizado = True  
                self.screen.blit(self.texto.texto_inicio, self.texto.texto_inicio_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
