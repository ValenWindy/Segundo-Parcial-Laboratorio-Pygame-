import pygame
from pygame import mixer
import json

class Options:
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

        # Teclas de jugabilidad
        self.key_mappings = {
            "Derecha": pygame.K_RIGHT,
            "Izquierda": pygame.K_LEFT,
            "Saltar": pygame.K_SPACE,
            "Cambiar Personaje": pygame.K_c,
        }

        # Cargar opciones desde el archivo de configuración
        self.cargar_opciones()

    def volver_menu_principal(self):
        self.regresar_a_menu = True
        print("Volviendo al menú principal")

    def mostrar_opciones(self):
        opciones = ["Cambiar Volumen del Sonido de Fondo", "Mostrar Botones", "Volver al Menú Principal"]
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
                            self.cambiar_volumen_fondo()
                        elif opcion_seleccionada == 1:
                            self.mostrar_botones()
                        elif opcion_seleccionada == 2:
                            self.volver_menu_principal()
                            running = False

            if running:
                self.screen.blit(self.background, (0, 0))
                titulo = self.font.render("Menú Principal", True, (255, 255, 255))
                self.screen.blit(titulo, (self.width // 2 - titulo.get_width() // 2, 50))

                for i, opcion in enumerate(opciones):
                    color = (255, 255, 255) if i == opcion_seleccionada else (128, 128, 128)
                    texto_opcion = self.font.render(opcion, True, color)
                    x = self.width // 2 - texto_opcion.get_width() // 2
                    y = self.height // 2 - len(opciones) * texto_opcion.get_height() // 2 + i * texto_opcion.get_height()
                    self.screen.blit(texto_opcion, (x, y))
                pygame.display.flip()

                if self.regresar_a_menu:
                    self.guardar_opciones()  # Guardar las opciones antes de volver al menú principal
                    break

    def cambiar_volumen_fondo(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.volumen = min(self.volumen + 0.1, 1.0)
                        mixer.music.set_volume(self.volumen)
                    elif event.key == pygame.K_DOWN:
                        self.volumen = max(self.volumen - 0.1, 0.0)
                        mixer.music.set_volume(self.volumen)

            # Mostrar el volumen actual
            texto_volumen = self.font.render("Volumen: {:.1f}".format(self.volumen), True, (255, 255, 255))
            x = self.width // 2 - texto_volumen.get_width() // 2
            y = self.height // 2 - texto_volumen.get_height() // 2
            self.screen.blit(texto_volumen, (x, y))
            pygame.display.flip()

    def mostrar_botones(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Mostrar los botones
            y = self.height // 2 - (len(self.key_mappings) * self.font_size) // 2
            for accion, tecla in self.key_mappings.items():
                texto = self.font.render("{}: {}".format(accion, pygame.key.name(tecla)), True, (255, 255, 255))
                x = self.width // 2 - texto.get_width() // 2
                self.screen.blit(texto, (x, y))
                y += self.font_size
            pygame.display.flip()

    def cargar_opciones(self):
        try:
            with open("opciones.json", "r") as archivo:
                opciones_guardadas = json.load(archivo)
                self.volumen = opciones_guardadas.get("volumen", self.volumen)
                mixer.music.set_volume(self.volumen)
                print("Opciones cargadas:", opciones_guardadas)
        except FileNotFoundError:
            print("No se encontró el archivo de opciones. Se usarán los valores predeterminados.")

    def guardar_opciones(self):
        opciones = {
            "volumen": self.volumen
        }
        with open("opciones.json", "w") as archivo:
            json.dump(opciones, archivo)
        print("Opciones guardadas:", opciones)