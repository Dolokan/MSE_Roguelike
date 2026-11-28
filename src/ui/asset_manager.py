# asset_manager.py

from pathlib import Path
import pygame

# Set up base project directory path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
GRAPHICS_DIR = BASE_DIR / "graphics"

SCALEFACTOR = 2.0
ASSETS = {}

def import_image(relative_path):
    # Load single image file
    full_path = GRAPHICS_DIR / relative_path
    img_surf = pygame.image.load(str(full_path)).convert_alpha()
    return pygame.transform.scale_by(img_surf, SCALEFACTOR)

def import_sprite_sheet(columns, rows, relative_path):
    '''imports sprite sheet as 2-dimensional list'''
    # Load sprite sheet into surface list
    full_path = GRAPHICS_DIR / relative_path
    surface_list = []
    sheet = pygame.image.load(str(full_path)).convert_alpha()

    # console output debug info
    name = "/".join(full_path.parts[-3:])

    img_width = sheet.get_size()[0] // columns
    img_height = sheet.get_size()[1] // rows

    count = 0 # debug info
    for ix in range(columns):
        surface_list.append([])
        for iy in range(rows):
            surf = pygame.Surface((img_width,img_height)).convert_alpha()
            surf.fill((0,0,0,0))
            surf.blit(sheet, pygame.math.Vector2(-img_width * ix,-img_height * iy))
            surf = pygame.transform.scale_by(surf, SCALEFACTOR)

            surface_list[ix].append(surf)
            count += 1

    print(f'[INFO] import {name} {columns}x{rows}={count} {img_width}x{img_height}px')
    return surface_list

def load_assets():
    # Load player single sprite or idle sprite
    ASSETS['player_idle'] = import_sprite_sheet(4,1,'Character/NinjaGreen/SeparateAnim/Idle.png')
