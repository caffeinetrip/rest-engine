import pygame

from ..utils.gfx import palette_swap, clip

def load_font_img(path, font_color=(255, 255, 255)):
    fg_color = (255, 0, 0)
    bg_color = (0, 0, 0)
    font_img = pygame.image.load(path).convert_alpha()
    font_img = palette_swap(font_img, {fg_color: font_color})
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()):
        if font_img.get_at((x, 0))[0] == 127:
            letters.append(clip(font_img, pygame.Rect(last_x, 0, x - last_x, font_img.get_height())))
            letter_spacing.append(x - last_x)
            last_x = x + 1
        x += 1
    for letter in letters:
        letter.set_colorkey(bg_color)
    return letters, letter_spacing, font_img.get_height()
