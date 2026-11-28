# src/ui/debug.py

import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(info, x = 10, y = 10):
    # Fetch current active screen surface
    display_surface = pygame.display.get_surface()

    # Render string information onto surface
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))

    # Draw dark background rect and text overlay
    pygame.draw.rect(display_surface,'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)

