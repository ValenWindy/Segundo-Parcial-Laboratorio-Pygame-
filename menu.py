import pygame
from pygame import mixer
from options import Options
from selector import SeleccionarNiveles
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
        
        
        pygame.mixer.init()
        mixer.music.load ("Music/Main Theme.wav") 
        mixer.music.play(-1) 
    def volver_menu_principal(self):
        self.regresar_a_menu = True

        print("Volviendo al menú principal")


    def iniciar_juego(self):
        print("Iniciando juego...")
        nivel_1 = Nivel_1() 
        nivel_1.run()

    def mostrar_opciones(self):
        opciones = Options()
        opciones.mostrar_opciones()
        opciones.volver_menu_principal()

    def seleccionar_niveles(self):
        seleccionar_niveles = SeleccionarNiveles()
        regresar_menu_principal = seleccionar_niveles.mostrar_niveles()
        if regresar_menu_principal:
            self.volver_menu_principal()

    def mostrar_menu(self):
        opciones = ["Iniciar Juego", "Seleccionar Nivel", "Opciones", "Salir"]
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
