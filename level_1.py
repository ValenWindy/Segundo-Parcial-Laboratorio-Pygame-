import pygame
import sys
import time
import random
from pygame.locals import *
from pygame.transform import flip
from options import Options
from personajes import Personajes
from monedas import Moneda
from movimientos import animaciones_personaje_1, animaciones_personaje_2

class Texto:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font_inicio = pygame.font.Font(self.font_path, self.font_size)
        self.texto_inicio = self.font_inicio.render("Nivel 1", True, (255, 255, 255))
        self.texto_inicio_rect = self.texto_inicio.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.animacion_inicio_tiempo = 3
        self.animacion_inicio_finalizado = False
        self.puntaje = 0
        self.tiempo_inicial = time.time()
        self.duracion_nivel = 60
        self.tiempo_transcurrido = 0
        self.animacion_inicio_inicial = time.time()
        self.personajes = Personajes()

    
    def formato_tiempo(self, tiempo_restante):
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        return f"{minutos:02d}:{segundos:02d}"

    def dibujar_puntaje(self):
        font = pygame.font.Font(None, 24)
        texto_puntaje = font.render("Puntaje: " + str(self.personajes.puntos), True, (255, 255, 255))
        self.screen.blit(texto_puntaje, (10, 10))


    def dibujar_tiempo_restante(self):
        font = pygame.font.Font(None, 24)
        tiempo_restante = self.duracion_nivel - (time.time() - self.tiempo_inicial)
        tiempo_restante_str = self.formato_tiempo(tiempo_restante)
        texto_tiempo_restante = font.render("Tiempo restante: " + tiempo_restante_str, True, (255, 255, 255))
        self.screen.blit(texto_tiempo_restante, (10, 70))
        if self.personajes.personaje_actual == 0:
            texto_vidas = font.render("Huntress: " + str(self.personajes.vidas), True, (255, 255, 255))
            self.screen.blit(texto_vidas, (self.SCREEN_WIDTH - texto_vidas.get_width() - 10, 10))
            texto_resistencia = font.render("Resistencia: " + str(self.personajes.resistencia), True, (255, 255, 255))
            self.screen.blit(texto_resistencia, (self.SCREEN_WIDTH - texto_resistencia.get_width() - 10, 70))
        elif self.personajes.personaje_actual == 1:
            texto_vidas = font.render("Soulhunter: " + str(self.personajes.vidas), True, (255, 255, 255))
            self.screen.blit(texto_vidas, (self.SCREEN_WIDTH - texto_vidas.get_width() - 10, 10))
            texto_resistencia = font.render("Resistencia: " + str(self.personajes.resistencia), True, (255, 255, 255))
            self.screen.blit(texto_resistencia, (self.SCREEN_WIDTH - texto_resistencia.get_width() - 10, 70))

    def mostrar_mensaje_final(self):
        score = self.personajes.calcular_puntos()
        mensaje = f"Nivel completado. Total de puntos: {score}"
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(mensaje, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(texto, texto_rect)
        pygame.display.update() 
        self.animacion_inicio_finalizado = True
        time.sleep(3)


class Nivel_1:
    def __init__(self):
        self.texto = Texto ()
        self.options = Options()
        self.personajes = Personajes()
        self.velocidad_caida_monedas = 2
        self.monedas = []
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_y = self.posicion_y_inicial
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_1.jpg").convert()
        self.flechas = []
        self.frame_actual = 0
        self.duracion_nivel = self.texto.duracion_nivel
        self.velocidad_animacion = 0.2
        self.flecha_lanzada = False
        self.flecha_posicion = None
        self.velocidad_salto = 25
        self.altura_salto = 200
        self.gravedad = 2

        pygame.mixer.music.load("Music/Main Theme.wav")
        pygame.mixer.music.play(-1)


    def recibir_golpe(self):
        self.personajes.recibir_golpe()

    def resetear_juego(self):
        self.personajes.resetear_juego()
        self.puntaje = self.personajes.calcular_puntos()

    def caer_monedas(self):
        if random.random() < 0.01:  
            nueva_moneda = Moneda()  
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


        
    def dibujar_personaje(self):
        ancho_nuevo = 100
        alto_nuevo = 100
        accion_actual = 'quieto'
        if self.personajes.movimiento_derecha or self.personajes.movimiento_izquierda:
            accion_actual = 'correr'
        if self.personajes.saltar and self.personajes.en_suelo:
            accion_actual = 'saltar'
        if self.personajes.ataque:
            accion_actual = 'atacar'

        if self.personajes.movimiento_derecha and self.personajes.posicion_x < self.SCREEN_WIDTH - ancho_nuevo - self.personajes.velocidad_movimiento:
            self.personajes.posicion_x += self.personajes.velocidad_movimiento
        elif self.personajes.movimiento_izquierda and self.personajes.posicion_x > 0:
            self.personajes.posicion_x -= self.personajes.velocidad_movimiento

        self.personajes.actualizar_rectangulo_personaje()  # Actualizar rectángulo del personaje

        self.frame_actual = (self.frame_actual + 1) % len(self.personajes.obtener_imagen_personaje_actual()[accion_actual])
        imagen_actual = self.personajes.obtener_imagen_personaje_actual()[accion_actual][self.frame_actual]
        imagen_actual = pygame.transform.scale(imagen_actual, (ancho_nuevo, alto_nuevo))

        if self.personajes.movimiento_izquierda:
            imagen_actual = pygame.transform.flip(imagen_actual, True, False)
        self.screen.blit(imagen_actual, (self.personajes.posicion_x, self.posicion_y))

        #rectangulo_personaje = pygame.Rect(self.personajes.posicion_x, self.posicion_y, ancho_nuevo, alto_nuevo)
        

    def actualizar_salto(self):
        if self.personajes.saltar and self.personajes.en_suelo:
            self.personajes.en_suelo = False
            self.altura_inicial = self.posicion_y
            self.velocidad_vertical = -self.velocidad_salto

        if not self.personajes.en_suelo:
            self.velocidad_vertical += self.gravedad
            self.posicion_y += self.velocidad_vertical

            if self.posicion_y >= self.altura_inicial:
                self.posicion_y = self.altura_inicial
                self.personajes.en_suelo = True

    def colision_monedas(self):
        personaje_rect = self.personajes.personaje_rect
        
        for moneda in self.monedas:
            moneda_rect = pygame.Rect(moneda.posicion_actual(), moneda.imagen_actual[0].get_size())
            if personaje_rect.colliderect(moneda_rect):
                self.personajes.puntos += moneda.imagen_actual[2]
                self.monedas.remove(moneda)



    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.dibujar_personaje()
        self.dibujar_monedas()
        self.texto.dibujar_puntaje()
        self.texto.dibujar_tiempo_restante()
        pygame.display.flip()

    def actualizar_tiempo_transcurrido(self):
        self.texto.tiempo_transcurrido += self.clock.tick(60) / 1000.0

        if self.texto.animacion_inicio_finalizado:
            if self.texto.tiempo_transcurrido >= 3.0:
                self.screen.blit(self.fondo, (0, 0))

    

    def run(self):
        while True:
            self.personajes.eventos()
            self.actualizar_tiempo_transcurrido()

            if self.texto.animacion_inicio_finalizado:
                self.actualizar_salto()
                self.caer_monedas()
                self.colision_monedas()
                self.dibujar_elementos()
                

                # Dibujar y actualizar la posición de la flecha
                if self.personajes.ataque and not self.flecha_posicion and self.personajes.personaje_actual == 0:
                    self.flecha_posicion = [self.personajes.posicion_x, self.posicion_y]  # Inicializar la posición de la flecha


                if self.flecha_posicion:
                    x, y = self.flecha_posicion  # Obtener las coordenadas x e y de self.flecha_posicion

                    if self.personajes.direccion_personaje == "derecha":
                        x += self.personajes.velocidad_movimiento * 2  # Mover la flecha hacia la derecha
                    else:
                        x -= self.personajes.velocidad_movimiento * 2  # Mover la flecha hacia la izquierda

                    self.flecha_posicion = [x, y]  # Actualizar la posición de la flecha

                    if self.flecha_posicion[0] > self.SCREEN_WIDTH or self.flecha_posicion[0] < 0:
                        self.flecha_posicion = None  # Reiniciar la posición de la flecha cuando sale de la pantalla

                # Dibujar la flecha si hay una posición válida
                if self.flecha_posicion:
                    flecha_imagen = animaciones_personaje_1['flecha'][0]  # O animaciones_personaje_2, dependiendo de cuál importaste
                    flecha_rect = flecha_imagen.get_rect()
                    flecha_rect.center = (self.flecha_posicion[0], self.flecha_posicion[1])
                    self.screen.blit(flecha_imagen, flecha_rect)

                

                tiempo_restante = self.duracion_nivel - (time.time() - self.texto.tiempo_inicial)
                if tiempo_restante <= 0 or self.personajes.vidas <= 0:
                    self.texto.mostrar_mensaje_final()
                    self.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado

                    break

            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.texto.animacion_inicio_inicial
                if tiempo_transcurrido >= self.texto.animacion_inicio_tiempo:
                    self.texto.animacion_inicio_finalizado = True  # Actualizar animacion_inicio_finalizado
                self.screen.blit(self.texto.texto_inicio, self.texto.texto_inicio_rect)

            pygame.display.update()