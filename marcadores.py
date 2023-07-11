import pygame
import csv
import os
import time
import tabulate
import pygame_menu
from pygame import mixer

class Marcadores:
    volumen = 0.5  # Valor predeterminado del volumen

    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Opciones")
        self.background = pygame.image.load("Backgrounds/Level_1.jpg")
        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.regresar_a_menu = False

        # Inicializar la música
        pygame.mixer.init()
        mixer.music.load("Music/Main Theme.wav")
        mixer.music.play(-1)

    def volver_menu_principal(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.regresar_a_menu = True
                        print("Volviendo al menú principal")
                        break

    def obtener_calificacion(self, puntaje):
        if puntaje <= 15000:
            return "Rookie"
        elif puntaje <= 25000:
            return "Average"
        else:
            return "Pro"

    def mostrar_datos_csv(self):
        file_path = 'puntajes.csv'
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        print(tabulate.tabulate(data, headers=['Nombre', 'Puntaje', 'Ranking'], tablefmt="grid"))

    def actualizar_puntaje_csv(self, puntaje, ranking, nombre_jugador):
        file_path = 'puntajes.csv'
        fieldnames = ['Nombre', 'Puntaje', 'Ranking']

        # Leer los datos existentes del archivo CSV
        data = []
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=fieldnames)
            for row in reader:
                data.append(row)

        # Actualizar los datos del jugador actual o agregar un nuevo registro si no existe
        found_player = False
        for i, row in enumerate(data):
            if row['Nombre'] == nombre_jugador:
                data[i]['Puntaje'] = str(puntaje)
                data[i]['Ranking'] = ranking
                found_player = True
                break

        if not found_player:
            data.append({'Nombre': nombre_jugador, 'Puntaje': str(puntaje), 'Ranking': ranking})

        # Sobrescribir el archivo CSV con los datos actualizados
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(data)

    def cargar_marcadores(self):
        file_path = 'puntajes.csv'
        if not os.path.isfile(file_path):
            raise FileNotFoundError("El archivo puntajes.csv no se encontró.")

        with open(file_path, newline='', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Omitir la primera fila
            self.marcadores = []

            for fila in lector_csv:
                Nombre, Puntaje, Ranking = fila
                self.marcadores.append({
                    'Nombre': Nombre,
                    'Puntaje': int(Puntaje),
                    'Ranking': Ranking
                })

            return self.marcadores

    def mostrar_marcadores(self):
        try:
            marcadores = self.cargar_marcadores()
        except FileNotFoundError:
            print("El archivo puntajes.csv no se encontró.")
            return [], self.regresar_a_menu

        marcadores_ordenados = sorted(marcadores, key=lambda x: x['Puntaje'], reverse=True)
        marcadores_ordenados = marcadores_ordenados[:10]

        # Crear una superficie de pantalla para dibujar la tabla de marcadores
        surface = pygame.Surface((self.width, self.height))
        surface.blit(self.background, (0, 0))

        fuente_titulo = pygame.font.Font(None, 48)
        titulo = fuente_titulo.render("Marcadores", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.width // 2, 80))
        surface.blit(titulo, titulo_rect)

        fuente_encabezados = pygame.font.Font(None, 28)
        encabezados_nombre = fuente_encabezados.render("Nombre", True, (255, 255, 255))
        encabezados_puntaje = fuente_encabezados.render("Puntaje", True, (255, 255, 255))
        encabezados_ranking = fuente_encabezados.render("Ranking", True, (255, 255, 255))
        
        encabezados_nombre_rect = encabezados_nombre.get_rect(midtop=(self.width // 2 - 100, 180))
        encabezados_puntaje_rect = encabezados_puntaje.get_rect(midtop=(self.width // 2, 180))
        encabezados_ranking_rect = encabezados_ranking.get_rect(midtop=(self.width // 2 + 100, 180))
        
        surface.blit(encabezados_nombre, encabezados_nombre_rect)
        surface.blit(encabezados_puntaje, encabezados_puntaje_rect)
        surface.blit(encabezados_ranking, encabezados_ranking_rect)

        fuente_marcador = pygame.font.Font(None, 28)
        y = 220
        for _, marcador in enumerate(marcadores_ordenados):
            nombre = marcador['Nombre']
            puntaje = marcador['Puntaje']
            ranking = marcador['Ranking']
            
            texto_nombre = fuente_marcador.render(nombre, True, (255, 255, 255))
            texto_nombre_rect = texto_nombre.get_rect(midtop=(self.width // 2 - 100, y))
            surface.blit(texto_nombre, texto_nombre_rect)
            
            texto_puntaje = fuente_marcador.render(str(puntaje), True, (255, 255, 255))
            texto_puntaje_rect = texto_puntaje.get_rect(midtop=(self.width // 2, y))
            surface.blit(texto_puntaje, texto_puntaje_rect)
            
            texto_ranking = fuente_marcador.render(ranking, True, (255, 255, 255))
            texto_ranking_rect = texto_ranking.get_rect(midtop=(self.width // 2 + 100, y))
            surface.blit(texto_ranking, texto_ranking_rect)
            
            y += 30

        self.screen.blit(surface, (0, 0))
        pygame.display.update()

        # Volver al menú principal
        self.regresar_a_menu = True
        self.volver_menu_principal()

        return marcadores_ordenados, self.regresar_a_menu
