import pygame
import sys
import time
import random
from pygame.locals import *
from options import Options
from texto import Texto 
from personajes_boss import Personajes
from enemigo_final import Jefe




class Nivel_4:
    def __init__(self):
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
    


    # def colision_enemigos(self):
    #     personaje_rect = self.personajes.personaje_rect
        
    #     for enemigo in self.enemigos.lista_enemigos:
    #         enemigo_rect = enemigo.enemigo_rect
            
    #         if personaje_rect.colliderect(enemigo_rect):
    #             if self.golpes == 0:
    #                 self.personajes.recibir_golpe()
    #                 self.personajes.actualizar_vidas()
    #                 self.personajes.actualizar_resistencia()
    #                 self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
    #                 self.golpes += 1
    #                 self.personajes.inmunidad = True  # Establecer inmunidad
    #                 self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
    #             elif self.golpes > 0 and not self.personajes.inmunidad:
    #                 self.personajes.recibir_golpe()
    #                 self.personajes.actualizar_vidas()
    #                 self.personajes.actualizar_resistencia()
    #                 self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
    #                 self.golpes += 1
    #                 self.personajes.inmunidad = True  # Establecer inmunidad
    #                 self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
        
        

    # def colision_ataque(self):
    #     if self.personajes.personaje_actual == 1:  # Solo para el personaje 2
    #         if self.personajes.ataque:
    #             for enemigo in self.enemigos.lista_enemigos:
    #                 if self.personajes.rectangulo_ataque_personaje_2.colliderect(enemigo.enemigo_rect):
    #                     self.enemigos.lista_enemigos.remove(enemigo)
    #                     self.personajes.puntos += enemigo.valor
    #                     break
    #     elif self.personajes.personaje_actual == 0:  # Solo para el personaje 1
    #         if self.personajes.ataque and self.personajes.flecha_posicion:
    #             for enemigo in self.enemigos.lista_enemigos:
    #                 if self.personajes.rectangulo_flecha.colliderect(enemigo.enemigo_rect):
    #                     self.enemigos.lista_enemigos.remove(enemigo)
    #                     self.personajes.puntos += enemigo.valor
    #                     self.personajes.flecha_posicion = None
    #                     break



    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.personajes.dibujar_personaje()
        self.jefe.dibujar_jefe()
        self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
        self.texto.dibujar_tiempo_restante()


        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_derecha_rect)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_izquierda_rect)

        if self.personajes.inmunidad:
            pygame.draw.rect(self.screen, (255, 255, 0), self.personajes.personaje_rect)  # Dibujar rectángulo amarillo para indicar inmunidad
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.personajes.personaje_rect, 2)  # Dibujar rectángulo verde normalmente

    


    def actualizar_tiempo_transcurrido(self):
        self.texto.tiempo_transcurrido += self.clock.tick(60) / 1000.0

        if self.texto.animacion_inicio_finalizado:
            if self.texto.tiempo_transcurrido >= 3.0:
                self.screen.blit(self.fondo, (0, 0))

        # Verificar si la inmunidad ha expirado
        if self.personajes.inmunidad:
            tiempo_actual = pygame.time.get_ticks()
            duracion_inmunidad = 5 * 1000  # Duración de la inmunidad en milisegundos (2 segundos en este ejemplo)
            if tiempo_actual - self.personajes.inicio_inmunidad >= duracion_inmunidad:
                self.personajes.inmunidad = False  # Desactivar inmunidad


    def mostrar_mensaje_final(self, puntos):
        score = self.personajes.calcular_puntos(puntos)
        mensaje = f"Nivel {self.nivel} completado. Total de puntos: {score}"
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(mensaje, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        self.screen.blit(self.fondo, (0, 0))
        self.screen.blit(texto, texto_rect)
        pygame.display.update()
        self.animacion_inicio_finalizado = True
        time.sleep(3)

    def game_over(self):
        mensaje = "FIN DEL JUEGO "
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(mensaje, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        self.screen.blit(self.fondo, (0, 0))
        self.screen.blit(texto, texto_rect)
        pygame.display.update()
        self.animacion_inicio_finalizado = True
        time.sleep(3)



    def run(self):
        while True:
            self.personajes.eventos()
            self.actualizar_tiempo_transcurrido()

            if self.texto.animacion_inicio_finalizado:
                self.personajes.actualizar_salto()
                # self.colision_enemigos()
                # self.colision_ataque()
                self.dibujar_elementos()
                
                
                tiempo_restante = self.duracion_nivel - (time.time() - self.texto.tiempo_inicial)
                if tiempo_restante <= 0:
                    self.mostrar_mensaje_final(self.personajes.puntos)
                    self.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado         
                    break

                if self.personajes.vidas <= 0:
                    self.game_over()
                    self.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado         
                    break

            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.texto.animacion_inicio_inicial
                if tiempo_transcurrido >= self.texto.animacion_inicio_tiempo:
                    self.texto.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado
                self.screen.blit(self.texto.texto_inicio, self.texto.texto_inicio_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)

            