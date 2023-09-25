import pygame
import csv
import tabulate
import os
from pygame import mixer
from options import Options
from selector import SeleccionarNiveles
from marcadores import Marcadores
from level_1 import Nivel_1

class Menu:
    volumen = 0.5
    volumen_guardado = volumen

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Huntress and the SoulHunter")
        self.background = pygame.image.load("Backgrounds/Level_1.jpg")
        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.regresar_a_menu = False
        # pygame.mixer.music.load("Music/Main Theme.wav")
        # pygame.mixer.music.play(-1)

    def pausar_musica(self):
        mixer.music.pause()

    def reanudar_musica(self):
        mixer.music.unpause()

    def volver_menu_principal(self):
        self.regresar_a_menu = True
        print("Volviendo al menú principal")

    def ingresar_nombre_jugador(self):
        nombre_jugador = ""

        input_rect = pygame.Rect(300, 200, 200, 36)
        color_fondo_input = pygame.Color('black')
        color_texto = pygame.Color('white')
        font = pygame.font.Font(None, 32)
        input_active = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        input_active = not input_active
                    else:
                        input_active = False
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            return nombre_jugador
                        elif event.key == pygame.K_BACKSPACE:
                            nombre_jugador = nombre_jugador[:-1]
                        else:
                            nombre_jugador += event.unicode

            self.screen.blit(self.background, (0, 0))
            titulo = self.font.render("The Huntress and The SoulHunter", True, (255, 255, 255))
            self.screen.blit(titulo, (self.width // 2 - titulo.get_width() // 2, 50))

            pygame.draw.rect(self.screen, color_fondo_input, input_rect)
            texto_ingresado = font.render(nombre_jugador, True, color_texto)
            self.screen.blit(texto_ingresado, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.flip()

    def iniciar_juego(self):
        
        print("Iniciando juego...")
        nombre_jugador = self.ingresar_nombre_jugador()
        if nombre_jugador:
            file_exists = os.path.isfile('puntajes.csv')  # Verificar si el archivo ya existe

            with open('puntajes.csv', 'a', newline='') as file:
                writer = csv.writer(file)

                # Escribir la primera fila solo si el archivo no existe
                if not file_exists:
                    writer.writerow(["Nombre", "Puntaje", "Ranking"])

                writer.writerow([nombre_jugador, 0, ""])
            self.pausar_musica()
            nivel_1 = Nivel_1(nombre_jugador)  # Crea el objeto Nivel_1 con el nombre del jugador
            nivel_1.run()

    def mostrar_opciones(self):
        opciones = Options()
        opciones.mostrar_opciones()
        opciones.volver_menu_principal()

    def seleccionar_niveles(self):
        seleccionar_niveles = SeleccionarNiveles()
        seleccionar_niveles.seleccionar_niveles()

    def mostrar_puntajes (self):
        marcadores = Marcadores ()
        marcadores.mostrar_marcadores()

    def mostrar_datos_base_de_datos(self):
        with open('puntajes.csv', 'r') as file:
            reader = csv.reader(file)
            datos = list(reader)

        print("Datos:")
        print(tabulate.tabulate(datos, headers=["Nombre", "Puntaje", "Calificación"], tablefmt="grid"))

    def mostrar_menu(self):
        opciones = ["Iniciar Juego", "Seleccionar Nivel", "Opciones", "Marcadores", "Salir"]
        opcion_seleccionada = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                    elif event.key == pygame.K_UP:
                        opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                    elif event.key == pygame.K_RETURN:
                        if opcion_seleccionada == 0:
                            self.iniciar_juego()
                        elif opcion_seleccionada == 1:
                            self.seleccionar_niveles()
                        elif opcion_seleccionada == 2:
                            self.mostrar_opciones()
                        elif opcion_seleccionada == 3:
                            self.mostrar_puntajes()
                        elif opcion_seleccionada == 4:
                            print("Seleccionaste Salir")
                            running = False

            self.screen.blit(self.background, (0, 0))
            titulo = self.font.render("The Huntress and The Soulhunter", True, (255, 255, 255))
            self.screen.blit(titulo, (self.width // 2 - titulo.get_width() // 2, 50))

            for i, opcion in enumerate(opciones):
                color = (255, 255, 255) if i == opcion_seleccionada else (128, 128, 128)
                texto_opcion = self.font.render(opcion, True, color)
                x = self.width // 2 - texto_opcion.get_width() // 2
                y = self.height // 2 - len(opciones) * texto_opcion.get_height() // 2 + i * texto_opcion.get_height()
                self.screen.blit(texto_opcion, (x, y))
            pygame.display.flip()

        return self.regresar_a_menu

    pygame.quit()
