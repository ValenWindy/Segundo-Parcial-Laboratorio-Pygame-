import pygame
from pygame import mixer
from level_1 import Nivel_1

class SeleccionarNiveles:
    volumen = 0.5  # Valor predeterminado del volumen
    volumen_guardado = volumen  # Variable para almacenar el volumen actual
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Seleccionar Nivel")
        self.background = pygame.image.load("Backgrounds/Level_1.jpg")
        self.font_path = "Constantine.ttf"
        self.font_size = 36
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.regresar_a_menu = False
        

        # Inicializar la música
        pygame.mixer.init()
        mixer.music.load ("Music/Main Theme.wav") 
        mixer.music.play(-1) 

    def volver_menu_principal(self):
        self.regresar_a_menu = True
        print("Volviendo al menú principal") # Volver a reproducir la música al regresar al menú principal


    def mostrar_niveles(self):
        niveles = ["Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Volver al Menú Principal"]
        nivel_seleccionado = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        nivel_seleccionado = (nivel_seleccionado + 1) % len(niveles)
                    elif event.key == pygame.K_UP:
                        nivel_seleccionado = (nivel_seleccionado - 1) % len(niveles)
                    elif event.key == pygame.K_RETURN:
                        if nivel_seleccionado == len(niveles) - 1:
                            self.volver_menu_principal()
                            running = False
                        else:
                            nivel = niveles[nivel_seleccionado]
                            print("Seleccionaste", nivel)
                            if nivel == "Nivel 1":
                                nivel_1 = Nivel_1()  # Crear una instancia de la clase Nivel_1
                                nivel_1.run()
                            # Lógica para cargar el nivel seleccionado

            self.screen.blit(self.background, (0, 0))
            titulo = self.font.render("Seleccionar Nivel", True, (255, 255, 255))
            self.screen.blit(titulo, (self.width // 2 - titulo.get_width() // 2, 50))

            for i, nivel in enumerate(niveles):
                color = (255, 255, 255) if i == nivel_seleccionado else (128, 128, 128)
                texto_nivel = self.font.render(nivel, True, color)
                x = self.width // 2 - texto_nivel.get_width() // 2
                y = self.height // 2 - len(niveles) * texto_nivel.get_height() // 2 + i * texto_nivel.get_height()
                self.screen.blit(texto_nivel, (x, y))
            pygame.display.flip()
        return self.regresar_a_menu
    pygame.quit()
        