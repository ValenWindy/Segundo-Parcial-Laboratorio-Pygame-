import pygame
from menu import Menu
from level_1 import Nivel_1
from level_2 import Nivel_2
from level_3 import Nivel_3
from level_4 import Nivel_4

pygame.init()            
pygame.display.set_caption("The Huntress and the SoulHunter")
def main():

    menu = Menu() 
    menu.mostrar_menu()
if __name__ == "__main__": 
    main() 

