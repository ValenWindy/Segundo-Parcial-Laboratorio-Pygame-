import pygame
from menu import Menu

pygame.init()            
pygame.display.set_caption("The Huntress and the SoulHunter")
def main():

    menu = Menu() 
    menu.mostrar_menu()
if __name__ == "__main__": 
    main() 

