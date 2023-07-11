import pygame
import sys
import time
import random
import csv
import os 
from pygame.locals import *
from options import Options
from texto import Texto 
from personajes_boss import Personajes
from enemigo_final import Jefe
from marcadores import Marcadores




class Nivel_4:
    def __init__(self, nombre_jugador, puntaje_total):
        self.nivel = 4
        self.options = Options()
        self.personajes = Personajes()
        self.jefe = Jefe ()
        self.texto = Texto(self.nivel, self.personajes)
        self.golpes = 0
        self.FPS = 60
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_4.jpg").convert()
        self.titulo = pygame.display.set_caption("The Huntress and the Soulhunter")
        self.duracion_nivel = self.texto.duracion_nivel   
        pygame.mixer.music.load("Music/Main Theme.wav")
        pygame.mixer.music.play(-1)
        self.nombre_jugador = nombre_jugador
        self.puntaje_total = puntaje_total
        
    
    def colision_jefe(self):
        personaje_rect = self.personajes.personaje_rect
        jefe_rect = self.jefe.jefe_rect
            
        if personaje_rect.colliderect(jefe_rect):
            if self.golpes == 0:
                self.personajes.recibir_golpe()
                self.personajes.actualizar_vidas()
                self.personajes.actualizar_resistencia()
                self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                self.golpes += 1
                self.personajes.inmunidad = True  
                self.personajes.inicio_inmunidad = pygame.time.get_ticks()  
            elif self.golpes > 0 and not self.personajes.inmunidad:
                self.personajes.recibir_golpe()
                self.personajes.actualizar_vidas()
                self.personajes.actualizar_resistencia()
                self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                self.golpes += 1
                self.personajes.inmunidad = True  
                self.personajes.inicio_inmunidad = pygame.time.get_ticks()  

    def colision_ataque(self):
        jefe_rect = self.jefe.jefe_rect

        if self.personajes.ataque:
            if self.personajes.personaje_actual == 1:  # Solo para el personaje 2
                if self.personajes.rectangulo_ataque_personaje_2.colliderect(jefe_rect):
                    if self.golpes == 0:
                        self.jefe.recibir_golpe_enemigo()
                        self.jefe.actualizar_resistencia_enemigo()
                        self.dibujar_texto_enemigo(self.jefe.resistencia)
                        self.golpes += 1
                        self.jefe.inmunidad = True  
                        self.personajes.inmunidad = True
                        self.personajes.inicio_inmunidad = pygame.time.get_ticks() 
                        self.jefe.inicio_inmunidad = pygame.time.get_ticks()  
                        if self.jefe.resistencia <= 0:
                            self.personajes.puntos += self.jefe.valor
                elif self.golpes > 0 and not self.jefe.inmunidad:
                    self.jefe.recibir_golpe_enemigo()
                    self.jefe.actualizar_resistencia_enemigo()
                    self.dibujar_texto_enemigo(self.jefe.resistencia)
                    self.golpes += 1
                    self.jefe.inmunidad = True  
                    self.personajes.inmunidad = True
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks() 
                    self.jefe.inicio_inmunidad = pygame.time.get_ticks()
                    if self.jefe.resistencia <= 0:
                            self.personajes.puntos += self.jefe.valor  

            elif self.personajes.personaje_actual == 0:  
                if self.personajes.flecha_posicion:
                    if self.golpes == 0:
                        if self.personajes.rectangulo_flecha.colliderect(jefe_rect):
                            self.jefe.recibir_golpe_enemigo()
                            self.jefe.actualizar_resistencia_enemigo()
                            self.dibujar_texto_enemigo(self.jefe.resistencia)
                            self.golpes += 1
                            self.jefe.inmunidad = True  
                            self.personajes.inmunidad = True
                            self.personajes.inicio_inmunidad = pygame.time.get_ticks() 
                            self.jefe.inicio_inmunidad = pygame.time.get_ticks()  
                            if self.jefe.resistencia <= 0:
                                    self.personajes.puntos += self.jefe.valor
                        elif self.golpes > 0 and not self.jefe.inmunidad:
                            self.jefe.recibir_golpe_enemigo()
                            self.jefe.actualizar_resistencia_enemigo()
                            self.dibujar_texto_enemigo(self.jefe.resistencia)
                            self.golpes += 1
                            self.jefe.inmunidad = True  
                            self.personajes.inmunidad = True
                            self.personajes.inicio_inmunidad = pygame.time.get_ticks() 
                            self.jefe.inicio_inmunidad = pygame.time.get_ticks()
                            if self.jefe.resistencia <= 0:
                                self.personajes.puntos += self.jefe.valor  
                                

    def dibujar_texto_enemigo(self, resistencia):

        fuente_jefe = pygame.font.Font(None, 24)
        texto_jefe = fuente_jefe.render("Jefe:", True, (255, 255, 255))
        texto_jefe_rect = texto_jefe.get_rect(bottomright=(self.SCREEN_WIDTH - 40, self.SCREEN_HEIGHT - 10))
        self.screen.blit(texto_jefe, texto_jefe_rect)


        fuente_resistencia = pygame.font.Font(None, 24)
        texto_resistencia = fuente_resistencia.render(str(self.jefe.resistencia), True, (255, 255, 255))
        texto_resistencia_rect = texto_resistencia.get_rect(bottomleft=(texto_jefe_rect.right + 5, texto_jefe_rect.bottom))
        self.screen.blit(texto_resistencia, texto_resistencia_rect)


    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.personajes.dibujar_personaje()
        self.jefe.dibujar_jefe()
        self.dibujar_texto_enemigo(self.jefe.resistencia)
        self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)


        if self.personajes.inmunidad:
            pygame.draw.rect(self.screen, (255, 255, 0), self.personajes.personaje_rect, 2) 


        if self.jefe.inmunidad:
            pygame.draw.rect(self.screen, (255, 255, 0), self.jefe.jefe_rect, 2)  


    def actualizar_tiempo_transcurrido(self):
        self.texto.tiempo_transcurrido += self.clock.tick(60) / 1000.0

        if self.texto.animacion_inicio_finalizado:
            if self.texto.tiempo_transcurrido >= 3.0:
                self.screen.blit(self.fondo, (0, 0))


        if self.personajes.inmunidad:
            tiempo_actual = pygame.time.get_ticks()
            duracion_inmunidad = 5 * 1000  
            if tiempo_actual - self.personajes.inicio_inmunidad >= duracion_inmunidad:
                self.personajes.inmunidad = False  


        if self.jefe.inmunidad:
            tiempo_actual = pygame.time.get_ticks()
            duracion_inmunidad = 5 * 1000  
            if tiempo_actual - self.jefe.inicio_inmunidad >= duracion_inmunidad:
                self.jefe.inmunidad = False  

        

    def mostrar_mensaje_final(self, puntos):
        score_nivel = self.personajes.calcular_puntos(puntos)
        puntaje_total = self.puntaje_total + score_nivel  # Suma el puntaje anterior con el puntaje del nivel actual
        mensaje_nivel = f"Nivel {self.nivel} completado."
        mensaje_puntos = f"Total de puntos del nivel: {score_nivel}"
        mensaje_score = f"Puntaje total: {puntaje_total}"
        mensaje_gracias = "Gracias por jugar."

        fuente_gracias = pygame.font.Font(None, 36)
        texto_gracias = fuente_gracias.render(mensaje_gracias, True, (255, 255, 255))
        texto_gracias_rect = texto_gracias.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        
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
        self.screen.blit(texto_gracias, texto_gracias_rect)
        
        pygame.display.update()
        self.texto.animacion_inicio_finalizado = True
        time.sleep(3)

        marcadores = Marcadores()
        ranking = marcadores.obtener_calificacion(puntaje_total)
        marcadores.actualizar_puntaje_csv(puntaje_total, ranking, self.nombre_jugador)




    def game_over(self):
        mensaje = "FIN DEL JUEGO "
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(mensaje, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        mensaje_gracias = "Gracias por jugar."
        fuente_gracias = pygame.font.Font(None, 36)
        texto_gracias = fuente_gracias.render(mensaje_gracias, True, (255, 255, 255))
        texto_gracias_rect = texto_gracias.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))

        self.screen.blit(self.fondo, (0, 0))
        self.screen.blit(texto, texto_rect)
        self.screen.blit(texto_gracias, texto_gracias_rect)
        pygame.display.update()
        self.animacion_inicio_finalizado = True
        time.sleep(3)

        marcadores = Marcadores()
        ranking = marcadores.obtener_calificacion(self.personajes.puntos)
        marcadores.actualizar_puntaje_csv(self.personajes.puntos, ranking, self.nombre_jugador)

        
        
    
    def run(self):
        while True:
            self.personajes.eventos()
            self.actualizar_tiempo_transcurrido()

            if self.texto.animacion_inicio_finalizado:
                self.personajes.actualizar_salto()
                self.colision_jefe()
                self.colision_ataque()
                self.dibujar_elementos()
                
                
                if self.jefe.resistencia <= 0:
                    self.mostrar_mensaje_final(self.personajes.puntos)
                    self.animacion_inicio_finalizado = True           
                    break

                if self.personajes.vidas <= 0:
                    self.game_over()
                    self.animacion_inicio_finalizado = True       
                    break

            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.texto.animacion_inicio_inicial
                if tiempo_transcurrido >= self.texto.animacion_inicio_tiempo:
                    self.texto.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado
                self.screen.blit(self.texto.texto_inicio, self.texto.texto_inicio_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)

