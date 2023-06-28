import pygame
import sys
import time
from pygame.locals import *
from pygame.transform import flip
from options import Options
from movimientos import animaciones_personaje_1, animaciones_personaje_2


class Personajes:
    def __init__(self):
        self.characters = [animaciones_personaje_1, animaciones_personaje_2]
        self.personaje_actual = 0
        self.vidas = 3
        self.resistencia = 4
        self.cambio_personaje_realizado = False
        self.velocidad_movimiento = 3
        self.movimiento_derecha = False
        self.movimiento_izquierda = False
        self.ataque = False
        self.saltar = False
        self.posicion_x = 100
        self.direccion_personaje = "derecha"
        self.en_suelo = True
        self.sound_huntress_attack = pygame.mixer.Sound("Music/Arrow.wav")
        self.sound_soulhunter_attack = pygame.mixer.Sound("Music/Sword.wav")
        

        
    def eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.movimiento_derecha = True
                    self.direccion_personaje = "derecha"
                elif event.key == K_LEFT:
                    self.movimiento_izquierda = True
                    self.direccion_personaje = "izquierda"
                elif event.key == K_SPACE:
                    self.saltar = True
                elif event.key == K_a:
                    self.ataque = True
                    if self.personaje_actual == 0:
                        self.sound_huntress_attack.play()
                    elif self.personaje_actual == 1:
                        self.sound_soulhunter_attack.play()
                elif event.key == K_c:
                    self.cambiar_personaje()
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.movimiento_derecha = False
                elif event.key == K_LEFT:
                    self.movimiento_izquierda = False
                elif event.key == K_SPACE:
                    self.saltar = False
                elif event.key == K_a:
                    self.ataque = False


    def cambiar_personaje(self):
            self.personaje_actual = (self.personaje_actual + 1) % len(self.characters)
            self.resistencia = 4
            self.cambio_personaje_realizado = True  # Marcar el cambio de personaje como realizado


    def obtener_imagen_personaje_actual(self):
            return self.characters[self.personaje_actual]


    def recibir_golpe(self):
        if self.resistencia > 0:
            self.resistencia -= 1
        if self.resistencia == 0 and not self.cambio_personaje_realizado:
            self.vidas -= 1
            if self.vidas > 0:
                self.cambiar_personaje()
            else:
                self.resetear_juego()

    def resetear_juego(self):
        self.personaje_actual = 0
        self.vidas = 3
        self.resistencia = 4
        self.cambio_personaje_realizado = False

    def calcular_puntos(self):
        puntos_por_vida = 250
        puntos_por_resistencia = 150
        total_puntos = self.vidas * puntos_por_vida + self.resistencia * puntos_por_resistencia
        return total_puntos


class Nivel_2:
    def __init__(self):
        
        self.options = Options()
        self.personajes = Personajes()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.posicion_y_inicial = self.SCREEN_HEIGHT - 100
        self.posicion_y = self.posicion_y_inicial
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fondo = pygame.image.load("Backgrounds/Level_2.jpg").convert()
        self.flechas = []
        self.frame_actual = 0
        self.velocidad_animacion = 0.2
        self.flecha_lanzada = False
        self.flecha_posicion = None
        self.nivel_2 = Nivel_2()
        pygame.mixer.music.load("Music/Main Theme.wav")
        pygame.mixer.music.play(-1)

        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font_inicio = pygame.font.Font(self.font_path, self.font_size)
        self.texto_inicio = self.font_inicio.render("Nivel 1", True, (255, 255, 255))
        self.texto_inicio_rect = self.texto_inicio.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.animacion_inicio_tiempo = 3
        self.animacion_inicio_finalizado = False
        self.animacion_inicio_inicial = time.time()
        self.velocidad_salto = 30
        self.altura_salto = 200
        self.gravedad = 2
        self.puntaje = 0
        self.tiempo_inicial = time.time()
        self.duracion_nivel = 60
        self.tiempo_transcurrido = 0


    def recibir_golpe(self):
        self.personajes.recibir_golpe()

    def resetear_juego(self):
        self.personajes.resetear_juego()
        self.puntaje = self.personajes.calcular_puntos()

    def formato_tiempo(self, tiempo_restante):
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        return f"{minutos:02d}:{segundos:02d}"

    
        
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

    
    


    def dibujar_puntaje(self):
        font = pygame.font.Font(None, 24)
        texto_puntaje = font.render("Puntaje: " + str(self.puntaje), True, (255, 255, 255))
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


    def dibujar_elementos(self):
        self.screen.blit(self.fondo, (0, 0))
        self.dibujar_personaje()
        self.dibujar_puntaje()
        self.dibujar_tiempo_restante()


        pygame.display.flip()


    

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            # Capturar eventos y actualizar estados del personaje
            self.personajes.eventos()

            self.tiempo_transcurrido += self.clock.tick(60) / 1000.0

            if self.animacion_inicio_finalizado:
                if self.tiempo_transcurrido >= 3.0:
                    self.screen.blit(self.fondo, (0, 0))

            if self.animacion_inicio_finalizado:
                # Dibujar elementos en pantalla
                self.dibujar_elementos()

                # Actualizar posición del fondo y personaje
                self.actualizar_salto()
                # Dibujar y actualizar la posición de la flecha
                if self.personajes.ataque and not self.flecha_posicion:
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

                tiempo_restante = self.duracion_nivel - (time.time() - self.tiempo_inicial)
                if tiempo_restante <= 0 or self.personajes.vidas <= 0:
                    self.resetear_juego()
                    nivel_2 = Nivel_2()
                    nivel_2.run()
            else:
                tiempo_actual = time.time()
                tiempo_transcurrido = tiempo_actual - self.animacion_inicio_inicial
                if tiempo_transcurrido >= self.animacion_inicio_tiempo:
                    self.animacion_inicio_finalizado = True
                self.screen.blit(self.texto_inicio, self.texto_inicio_rect)
                
            

            pygame.display.flip()