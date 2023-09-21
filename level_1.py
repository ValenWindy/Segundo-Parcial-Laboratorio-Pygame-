import pygame
import sys
import time
import random
import keyboard
import csv
import os
from pygame.locals import *
from options import Options
from texto import Texto 
from personajes import Personajes
from monedas import Monedas
from plataformas import Plataformas
from enemigos import Enemigos
from fruta import Frutas
from level_2 import Nivel_2
from marcadores import Marcadores




class Nivel_1:
    def __init__(self, nombre_jugador):
    
        self.nivel = 1
        self.options = Options()
        self.personajes = Personajes()
        self.plataformas = Plataformas()
        self.texto = Texto(self.nivel, self.personajes)
        self.enemigos = Enemigos()
        self.frutas = Frutas ()
        self.velocidad_caida_monedas = 5
        self.monedas = []
        self.golpes = 0
        self.FPS = 60
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_1.jpg").convert()
        self.titulo = pygame.display.set_caption("The Huntress and the Soulhunter")
        self.duracion_nivel = self.texto.duracion_nivel
        self.enemigos.crear_enemigo_suelo()     
        pygame.mixer.music.load("Music/Level_1.wav")
        pygame.mixer.music.play(-1)
        self.tiempo_creacion_enemigo = 10.0
        self.ultimo_tiempo_creacion_enemigo = time.time()
        self.nombre_jugador = nombre_jugador
        self.huntress_hit = False
        self.soulhunter_hit = False
        self.pausa = False
        self.game_over_state = False

        
    
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
                moneda.sound_coin.play()
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
                    self.frutas.sound_banana.play()
                    self.personajes.resistencia += 1
                elif tipo_fruta == "Manzana":
                    self.frutas.sound_apple.play()
                    self.personajes.vidas += 1
                self.frutas.lista_frutas.remove(fruta)
                break


    def colision_enemigos(self):
        personaje_rect = self.personajes.personaje_rect

        for enemigo in self.enemigos.lista_enemigos_suelo:
            enemigo_rect = enemigo.enemigo_rect

            if personaje_rect.colliderect(enemigo_rect):
                if self.golpes == 0:
                    if self.personajes.personaje_actual == 0:  # Huntress
                        self.huntress_hit = True
                        self.personajes.sound_huntress_hit.play()
                    elif self.personajes.personaje_actual == 1:  # Soulhunter
                        self.soulhunter_hit = True
                        self.personajes.sound_soulhunter_hit.play()

                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()
                elif self.golpes > 0 and not self.personajes.inmunidad:
                    if self.personajes.personaje_actual == 0:  
                        self.huntress_hit = True
                        self.personajes.sound_huntress_hit.play()
                    elif self.personajes.personaje_actual == 1:  
                        self.soulhunter_hit = True
                        self.personajes.sound_soulhunter_hit.play()

                    self.personajes.recibir_golpe()
                    self.personajes.actualizar_vidas()
                    self.personajes.actualizar_resistencia()
                    self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
                    self.golpes += 1
                    self.personajes.inmunidad = True
                    self.personajes.inicio_inmunidad = pygame.time.get_ticks()


    def colision_ataque(self):
        if self.personajes.personaje_actual == 1:  
            if self.personajes.ataque:
                for enemigo in self.enemigos.lista_enemigos_suelo:
                    if self.personajes.rectangulo_ataque_personaje_2.colliderect(enemigo.enemigo_rect):
                        self.enemigos.sound_death.play()
                        self.enemigos.lista_enemigos_suelo.remove(enemigo)
                        self.personajes.puntos += enemigo.valor
                        break
        elif self.personajes.personaje_actual == 0:  
            if self.personajes.ataque and self.personajes.flecha_posicion:
                self.rectangulo_punto = pygame.Rect(self.personajes.flecha_posicion, (1, 1))
                for enemigo in self.enemigos.lista_enemigos_suelo:
                    if self.rectangulo_punto.colliderect(enemigo.enemigo_rect):
                        self.enemigos.sound_death.play()
                        self.enemigos.lista_enemigos_suelo.remove(enemigo)
                        self.personajes.puntos += enemigo.valor
                        self.personajes.flecha_posicion = None
                        break

    def eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.personajes.movimiento_derecha = True
                    self.personajes.direccion_personaje = "derecha"
                    self.personajes.velocidad_horizontal = self.personajes.velocidad_movimiento
                elif event.key == K_LEFT:
                    self.personajes.movimiento_izquierda = True
                    self.personajes.direccion_personaje = "izquierda"
                    self.personajes.velocidad_horizontal = -self.personajes.velocidad_movimiento
                elif event.key == K_SPACE:
                    self.personajes.saltar = True
                    self.personajes.sound_jump.play()
                elif event.key == K_a:
                    self.personajes.ataque = True
                    if self.personajes.personaje_actual == 0:
                        self.personajes.sound_huntress_attack.play()
                    elif self.personajes.personaje_actual == 1:
                        self.personajes.sound_soulhunter_attack.play()
                elif event.key == K_c:
                    self.personajes.cambiar_personaje()
                elif event.key == pygame.K_ESCAPE:  # Tecla Q para activar el Game Over en pausa
                    self.pausar ()
                elif event.key == pygame.K_q:  # Tecla Q para activar el Game Over
                    if self.pausa:
                        self.game_over()
                        self.texto.animacion_inicio_finalizado = True
                        break
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.personajes.movimiento_derecha = False
                    self.personajes.velocidad_horizontal = 0
                elif event.key == K_LEFT:
                    self.personajes.movimiento_izquierda = False
                    self.personajes.velocidad_horizontal = 0
                elif event.key == K_SPACE:
                    self.personajes.saltar = False
                elif event.key == K_a:
                    self.personajes.ataque = False

    def pausar(self):
        self.pausa = True  # Activar la pausa

        while self.pausa:
            pygame.event.get()
            clock = pygame.time.Clock()
            fuente = pygame.font.Font(None, 36)
            mensaje_pausa = fuente.render("PAUSA", True, (255, 255, 255))
            mensaje_pausa_rect = mensaje_pausa.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            mensaje_continuar = fuente.render("Presione Enter para continuar", True, (255, 255, 255))
            mensaje_continuar_rect = mensaje_continuar.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
            mensaje_game_over = fuente.render("Presione Q para Game Over", True, (255, 255, 255))
            mensaje_game_over_rect = mensaje_game_over.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100))

            self.screen.blit(mensaje_pausa, mensaje_pausa_rect)
            self.screen.blit(mensaje_continuar, mensaje_continuar_rect)
            self.screen.blit(mensaje_game_over, mensaje_game_over_rect)
            pygame.display.update()
            clock.tick(60)

            if keyboard.is_pressed('enter'):
                self.pausa = False
            elif keyboard.is_pressed('q'):
                self.game_over_state = True  # Cambiar el nombre de la variable
                self.pausa = False
                break


    
    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.personajes.dibujar_personaje()
        self.plataformas.dibujar_plataformas()
        self.dibujar_monedas()
        self.frutas.dibujar_fruta()
        self.frutas.generar_frutas()  
        self.crear_enemigo_periodico()
        self.texto.dibujar_puntaje(self.personajes.puntos, self.personajes.vidas, self.personajes.resistencia)
        self.texto.dibujar_tiempo_restante()


        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_derecha_rect)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.plataformas.plataforma_grande_izquierda_rect)

        if self.personajes.inmunidad:
            pygame.draw.rect(self.screen, (255, 255, 0), self.personajes.personaje_rect, 2)  

    def actualizar_tiempo_transcurrido(self):
        self.texto.tiempo_transcurrido += self.clock.tick(60) / 1000.0

        if self.texto.animacion_inicio_finalizado:
            if self.texto.tiempo_transcurrido >= 3.0:
                self.screen.blit(self.fondo, (0, 0))

        # Verificar si la inmunidad ha expirado
        if self.personajes.inmunidad:
            tiempo_actual = pygame.time.get_ticks()
            duracion_inmunidad = 5 * 1000  
            if tiempo_actual - self.personajes.inicio_inmunidad >= duracion_inmunidad:
                self.personajes.inmunidad = False 


    def mostrar_mensaje_final(self, puntos):
        score_nivel = self.personajes.calcular_puntos(puntos)
        puntaje_total =  score_nivel  
        mensaje_nivel = f"Nivel {self.nivel} completado."
        mensaje_puntos = f"Total de puntos del nivel: {score_nivel}"
        mensaje_lore = "Anisum y Calyx llegan a un acuerdo para derrotar a Palez"
        
        
        fuente = pygame.font.Font(None, 36)
        texto_nivel = fuente.render(mensaje_nivel, True, (255, 255, 255))
        texto_puntos = fuente.render(mensaje_puntos, True, (255, 255, 255))
        texto_lore = fuente.render(mensaje_lore, True, (255, 255, 255))

        
        texto_nivel_rect = texto_nivel.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        texto_puntos_rect = texto_puntos.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        texto_lore_rect = texto_lore.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 30))

        
        self.screen.blit(self.fondo, (0, 0))
        self.screen.blit(texto_nivel, texto_nivel_rect)
        self.screen.blit(texto_puntos, texto_puntos_rect)
        self.screen.blit(texto_lore, texto_lore_rect)
        
        
        pygame.display.update()
        self.texto.animacion_inicio_finalizado = True
        time.sleep(3)

        marcadores = Marcadores()
        ranking = marcadores.obtener_calificacion(puntaje_total)
        marcadores.actualizar_puntaje_csv(puntaje_total, ranking, self.nombre_jugador)

        
        nivel_2 = Nivel_2(self.nombre_jugador, puntaje_total)
        nivel_2.run()



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
            self.eventos()
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
                    self.animacion_inicio_finalizado = True         
                    break

                if self.personajes.vidas <= 0 or self.game_over_state:  # Cambiar el nombre de la variable
                    self.game_over()
                    self.texto.animacion_inicio_finalizado = True
                    break

            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.texto.animacion_inicio_inicial
                if tiempo_transcurrido >= self.texto.animacion_inicio_tiempo:
                    self.texto.animacion_inicio_finalizado = True  
                self.screen.blit(self.texto.texto_inicio, self.texto.texto_inicio_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
