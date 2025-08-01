import os, pygame

from rest.utils.io import write_tjson, read_tjson
from rest.utils.gfx import clip
from .asset_utils import load_img_directory
from components.cms_components import Spritesheets

def load_spritesheet_config(path):
    config = read_tjson(path, loose=True) if os.path.isfile(path) else {}
    write_tjson(path, config)
    return config


def parse_spritesheet(surf, split_color=(0, 255, 255)):
    row_start, loc, tiles = None, [0, 0], {}

    for y in range(surf.get_height() - 1):
        curr_color = surf.get_at((1, y))
        next_color = surf.get_at((1, y + 1))
        left_color = surf.get_at((0, y + 1))

        if (curr_color == split_color and next_color != split_color and left_color == split_color): row_start = y

        if (curr_color != split_color and next_color == split_color and left_color == split_color and row_start is not None):
            row_bounds_y, col_start = (row_start, y), None

            for x in range(surf.get_width() - 1):
                curr_color = surf.get_at((x, row_bounds_y[0] + 1))
                next_color = surf.get_at((x + 1, row_bounds_y[0] + 1))

                if (curr_color == split_color and next_color != split_color): col_start = x

                if (curr_color != split_color and next_color == split_color and col_start is not None):
                    col_bounds_x = (col_start, x)

                    if col_start == 0: tile_bounds_y = row_bounds_y
                    else:
                        y2 = row_start
                        while y2 < surf.get_height() - 1:
                            curr_color = surf.get_at((col_start + 1, y2))
                            next_color = surf.get_at((col_start + 1, y2 + 1))
                            if (curr_color != split_color and next_color == split_color): break
                            y2 += 1
                        tile_bounds_y = (row_start, y2)

                    rect = pygame.Rect(col_bounds_x[0] + 1, tile_bounds_y[0] + 1, col_bounds_x[1] - col_bounds_x[0], tile_bounds_y[1] - tile_bounds_y[0])
                    tiles[tuple(loc)] = clip(surf, rect)
                    loc[0] += 1
                    col_start = None

            loc[1], loc[0], row_start = loc[1] + 1, 0, None

    return tiles

def load_spritesheets(path, split_color=(0,255,0), colorkey=(0,0,0)) -> Spritesheets:
    
    spritesheets: Spritesheets = Spritesheets(load_img_directory(path, colorkey)) # type: ignore
    
    for spritesheet in spritesheets.value:
        
        spritesheets.value[spritesheet] = {
            'assets': parse_spritesheet(spritesheets.value[spritesheet], split_color),
            'config': load_spritesheet_config(f'{path}/{spritesheet}.json')
        }
        
        for tile in spritesheets.value[spritesheet]['assets']:
            
            if tile not in spritesheets.value[spritesheet]['config']:
                spritesheets.value[spritesheet]['config'][tile] = {'offset': (0, 0)}
            
            if 'offset' not in spritesheets.value[spritesheet]['config'][tile]:
                spritesheets.value[spritesheet]['config'][tile]['offset'] = (0, 0)
    
    return spritesheets