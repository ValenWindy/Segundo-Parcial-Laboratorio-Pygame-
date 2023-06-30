import pygame
from menu import Menu
from level_1 import Nivel_1


pygame.init()
pygame.display.set_caption("The Huntress and the SoulHunter")


# Función donde estara la lógica del juego
def main(): 
    nivel_1 = Nivel_1()  
    nivel_1.run()

if __name__ == "__main__":
    main() 

