import pygame
from menu import Menu


pygame.init()
pygame.display.set_caption("The Huntress and the SoulHunter")

# Variables iniciales

# Función donde estara la lógica del juego
def main():
    menu = Menu() 
    menu.mostrar_menu()

if __name__ == "__main__":
    main() 

