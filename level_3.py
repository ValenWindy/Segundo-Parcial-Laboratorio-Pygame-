import pygame
import sys
import time
import random

from pygame.locals import *
from options import Options
from texto import Texto 
from personajes import Personajes
from monedas import Monedas
from plataformas import Plataformas
from enemigos import Enemigos
from trampas import Trampas
from fruta import Frutas
from level_4 import Nivel_4



class Nivel_3:
    def __init__(self):
        self.nivel = 3
        self.options = Options()
        self.personajes = Personajes()
        self.plataformas = Plataformas()
        self.frutas = Frutas()
        self.texto = Texto(self.nivel, self.personajes)
        self.enemigos = Enemigos()
        self.trampas = Trampas()
        self.velocidad_caida_monedas = 2
        self.monedas = []
        self.golpes = 0
        self.FPS = 60
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_3.jpg").convert()
        self.titulo = pygame.display.set_caption("The Huntress and the Soulhunter")
        self.duracion_nivel = self.texto.duracion_nivel     
        self.enemigos.crear_enemigo_suelo()     
        pygame.mixer.music.load("Music/Main Theme.wav")
        pygame.mixer.music.play(-1)
        self.tiempo_creacion_enemigo = 10.0
        self.ultimo_tiempo_creacion_enemigo = time.time()
        

    def crear_enemigo_periodico(self):
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_tiempo_creacion_enemigo >= self.tiempo_creacion_enemigo:
            nuevo_enemigo = self.enemigos.crear_enemigo_suelo()
            nuevo_enemigo.posicion_x = random.randint(0, self.SCREEN_WIDTH - nuevo_enemigo.enemigo_rect.width)
            nuevo_enemigo.posicion_x_inicial = nuevo_enemigo.posicion_x
            self.ultimo_tiempo_creacion_enemigo = tiempo_actual

        self.enemigos.actualizar_enemigos()
        self.enemigos.dibujar_enemigos()


    def caer_monedas(self):
        if random.random() < 0.01:  
            nueva_moneda = Monedas()  
            self.monedas.append(nueva_moneda)  

        # Hacer que las monedas caigan
        for moneda in self.monedas:
            x, y = moneda.posicion_actual()
            y += self.velocidad_caida_monedas
            moneda.posicion = (x, y)

            # Eliminar las monedas que hayan alcanzado el límite inferior de la pantalla
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

    def colision_frutas(self):
        personaje_rect = self.personajes.personaje_rect

        for fruta in self.frutas.lista_frutas:
            fruta_rect = fruta["rect"]
            if personaje_rect.colliderect(fruta_rect):
                tipo_fruta = fruta["tipo"]
                if tipo_fruta == "Banana":
                    self.personajes.resistencia += 1
                elif tipo_fruta == "Manzana":
                    self.personajes.vidas += 1
                self.frutas.lista_frutas.remove(fruta)
                break


    def colision_enemigos(self):
        personaje_rect = self.personajes.personaje_rect
        
        for enemigo in self.enemigos.lista_enemigos_suelo:
            enemigo_rect = enemigo.enemigo_rect
            
            # Colisión con el personaje
            if personaje_rect.colliderect(enemigo_rect):
                if self.golpes == 0:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
                elif self.golpes > 0 and not self.personajes.inmunidad:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
            
            # Colisión con los ojos rojos
        for trampa in self.trampas.lista_trampas_rojas:
            trampa_rect = trampa['surface']
                
            if personaje_rect.colliderect(trampa_rect):
                if self.golpes == 0:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
            elif self.golpes > 0 and not self.personajes.inmunidad:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
                        
            # Colisión con los ojos azules
        for trampa in self.trampas.lista_trampas_azules:
            trampa_rect = trampa['surface']
                
            if personaje_rect.colliderect(trampa_rect):
                if self.golpes == 0:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad
                elif self.golpes > 0 and not self.personajes.inmunidad:
                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True  # Establecer inmunidad
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()  # Registrar tiempo de inicio de inmunidad


    def colision_ataque(self):
        if self.personajes.personaje_actual == 1:  # Solo para el personaje 2
            if self.personajes.ataque:
                for enemigo in self.enemigos.lista_enemigos:
                    if self.personajes.rectangulo_ataque_personaje_2.colliderect(enemigo.enemigo_rect):
                        self.enemigos.lista_enemigos.remove(enemigo)
                        self.personajes.puntos += enemigo.valor
                        break
        elif self.personajes.personaje_actual == 0:  # Solo para el personaje 1
            if self.personajes.ataque and self.personajes.flecha_posicion:
                for enemigo in self.enemigos.lista_enemigos_suelo:
                    if self.personajes.rectangulo_flecha.colliderect(enemigo.enemigo_rect):
                        self.enemigos.lista_enemigos_suelo.remove(enemigo)
                        self.personajes.puntos += enemigo.valor
                        self.personajes.flecha_posicion = None
                        break



    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.personajes.dibujar_personaje()
        self.plataformas.dibujar_plataformas()
        self.trampas.dibujar_trampas()
        self.crear_enemigo_periodico()
        self.dibujar_monedas()
        self.frutas.dibujar_fruta()
        self.frutas.generar_frutas()  
        self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
        self.texto.dibujar_tiempo_restante()


        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_derecha_rect)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_izquierda_rect)

        if self.personajes.inmunidad:
            pygame.draw.rect(self.screen, (255, 255, 0), self.personajes.personaje_rect, 2)  # Dibujar rectángulo amarillo para indicar inmunidad
        else:
            pass
            # pygame.draw.rect(self.screen, (0, 255, 0), self.personajes.personaje_rect, 2)  # Dibujar rectángulo verde normalmente

        pygame.display.flip()
    
    
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
        self.texto.animacion_inicio_finalizado = True
        time.sleep(3)
        nivel_4 = Nivel_4()
        nivel_4.run()


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
                self.caer_monedas()
                self.colision_monedas()
                self.colision_frutas()
                self.colision_enemigos()
                self.colision_ataque()
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

            