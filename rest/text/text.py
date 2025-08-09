import pygame
from ..utils.gfx import palette_swap
from ..utils.io import recursive_file_op
from .text_util import load_font_img
from rest.utils.cms import CMSEntity, CMSComponentDefinition
from typing import Dict, List, Optional
from rest import G

class Path(CMSComponentDefinition):
    value: str

class Fonts(CMSComponentDefinition):
    value: Dict

class FontObj(CMSComponentDefinition):
    font_order = [
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        '.','- ',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';','%',
        'о','О'  # Додано кириличні символи
    ]
    base_spacing: int
    line_spacing: int

class FontSize(CMSComponentDefinition):
    width: int
    height: int

class FontCache(CMSComponentDefinition):
    value: Dict

class IsTtf(CMSComponentDefinition):
    value: bool

class TtfFont(CMSComponentDefinition):
    font: pygame.font.Font
    line_height: int
    letter_spacing: Optional[bool]
    space_width: int
    color_cache: Dict

class PngFont(CMSComponentDefinition):
    letters: List
    letter_spacing: List
    line_height: int
    color_cache: Dict
    space_width: int

class Text(CMSComponentDefinition):
    value: str

class TextEntity(CMSEntity):
    def __init__(self, path):
        super().__init__(entity_id='text_obj')
        self.components = {
            'path': Path(value=path),
        }
        self.load()
        
    def load(self):
        self.add_component('fonts', Fonts(recursive_file_op(
            self.get_component('path').value, Font
        )))
        
    def __getitem__(self, key):
        return self.get_component('fonts').value[key]

class PreppedText(CMSEntity):
    def __init__(self, text, size, font):
        super().__init__(entity_id='prepped_text')
        self.components = {
            'text': Text(value=text),
            'font': font,
            'size': FontSize(width=size[0], height=size[1]),
            'cache': FontCache(value={})
        }

    def render(self, surf, loc, color=None, bgcolor=None):
        cache = self.get_component('cache').value
        cache_key = (self.get_component('text').value, color, bgcolor)
        if cache_key in cache:
            cached_surface, cached_loc = cache[cache_key]
            surf.blit(cached_surface, loc)
            return

        render_surface = pygame.Surface(
            (self.get_component('size').width, self.get_component('size').height),
            pygame.SRCALPHA
        )
        font = self.get_component('font')
        text = self.get_component('text').value
        if bgcolor and not font.get_component('is_ttf').value:
            for o in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                font.render(render_surface, text, (o[0], o[1]), color=bgcolor)
        font.render(render_surface, text, (0, 0), color=color)
        
        cache[cache_key] = (render_surface, loc)
        surf.blit(render_surface, loc)

    def __repr__(self):
        text = self.get_component('text').value
        size = self.get_component('size')
        return f'<PreppedText:{size.width}x{size.height}> {text}'.replace('\n', '\\n')

    def __str__(self):
        return self.__repr__()

class Font(CMSEntity):
    def __init__(self, path, color=(255, 255, 255), is_ttf=False, ttf_size=16):
        super().__init__(entity_id=f'font_{path}')
        
        self.components = {
            'is_ttf': IsTtf(value=is_ttf),
            'font_obj': FontObj(base_spacing=1, line_spacing=2),
            'base_color': color
        }
        
        if is_ttf:
            self.add_component('ttf_font', TtfFont(
                font=pygame.font.Font(path, ttf_size),
                line_height=pygame.font.Font(path, ttf_size).get_height(),
                letter_spacing=None,
                space_width=pygame.font.Font(path, ttf_size).size(' ')[0],
                color_cache={}
            ))
            
        else:
            letters, letter_spacing, line_height = load_font_img(path, color)
            self.add_component('png_font', PngFont(
                letters=letters,
                letter_spacing=letter_spacing,
                line_height=line_height,
                color_cache={color: letters},
                space_width=letter_spacing[0]
            ))
        
    def prep_color(self, color):
        if self.get_component('is_ttf').value:
            return
        
        png_font = self.get_component('png_font')
        new_letters = []
        
        for img in png_font.letters:
            if len(color) > 3:
                img.convert_alpha()
            new_letters.append(palette_swap(img, {self.get_component('base_color'): color}))
            
        png_font.color_cache[color] = new_letters

    def width(self, text):
        
        if self.get_component('is_ttf').value:
            return self.get_component('ttf_font').font.size(text)[0]
        
        text_width = 0
        font_obj = self.get_component('font_obj')
        png_font = self.get_component('png_font')
        
        for char in text:
            if char == ' ':
                text_width += png_font.space_width + font_obj.base_spacing
                
            else:
                try:
                    text_width += png_font.letter_spacing[font_obj.font_order.index(char)] + font_obj.base_spacing
                    
                except (ValueError, KeyError):
                    text_width += png_font.space_width + font_obj.base_spacing
                    
        return text_width

    def prep_text(self, text, line_width=0):
        if not line_width:
            return PreppedText(text, (self.width(text), self.get_component('ttf_font' if self.get_component('is_ttf').value else 'png_font').line_height), self)

        words = []
        word_width = 0
        word = ''
        
        font_obj = self.get_component('font_obj')
        
        for i, char in enumerate(text):
            if char not in ['\n', ' ']:
                if self.get_component('is_ttf').value:
                    word_width += self.get_component('ttf_font').font.size(char)[0] + font_obj.base_spacing
                    
                else:
                    try:
                        word_width += self.get_component('png_font').letter_spacing[font_obj.font_order.index(char)] + font_obj.base_spacing
                        
                    except (ValueError, KeyError):
                        word_width += self.get_component('png_font').space_width + font_obj.base_spacing
                        
                word += char
                
            else:
                words.append((word, word_width))
                words.append((char, self.get_component('ttf_font' if self.get_component('is_ttf').value else 'png_font').space_width + font_obj.base_spacing if char == ' ' else 0))
                word = ''
                word_width = 0
                
        if word != '':
            words.append((word, word_width))

        x = 0
        y = 0
        
        processed_text = ''
        max_width = 0
        
        for word in words:
            if word[0] == '\n':
                y += 1
                x = 0
                
            else:
                if x + word[1] > line_width:
                    processed_text += '\n'
                    x = 0 if word[0] == ' ' else word[1]
                    y += 1
                    
                else:
                    x += word[1]
                    
                if (word[0] != ' ') or (x != 0):
                    processed_text += word[0]
                    
                max_width = max(max_width, x)

        line_height = self.get_component('ttf_font' if self.get_component('is_ttf').value else 'png_font').line_height
        return PreppedText(processed_text, (max_width, line_height + (line_height + self.get_component('font_obj').line_spacing) * y), self)
    
    def renderz(self, text, loc, line_width=0, color=None, offset=(0, 0), group='ui', z=0):
        self.render(G.window, text, (loc[0] - offset[0], loc[1] - offset[1]), line_width=line_width, color=color, blit_kwargs={'group': group, 'z': z})
    
    def renderzb(self, text, loc, line_width=0, color=None, bgcolor=None, offset=(0, 0), group='ui', z=0, hide_chars=0):
        if self.get_component('is_ttf').value:
            for o in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                self.renderz(text, (loc[0] + o[0], loc[1] + o[1]), line_width=line_width, color=bgcolor, offset=offset, group=group, z=z - 1)
                
        else:
            for o in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                self.renderz(text, (loc[0] + o[0], loc[1] + o[1]), line_width=line_width, color=bgcolor, offset=offset, group=group, z=z - 1)
                
        self.renderz(text, loc, line_width=line_width, color=color, offset=offset, group=group, z=z)

    def render(self, surf, text, loc, line_width=0, color=None, blit_kwargs={}):
        
        if not color:
            color = self.get_component('base_color')
            
        if self.get_component('is_ttf').value:
            
            lines = text.split('\n')
            y_offset = 0
            ttf_font = self.get_component('ttf_font')
            
            for line in lines:
                
                if line:
                    text_surface = ttf_font.font.render(line, True, color)
                    surf.blit(text_surface, (loc[0], loc[1] + y_offset), **blit_kwargs)
                    
                y_offset += ttf_font.line_height + self.get_component('font_obj').line_spacing
                
        else:
            png_font = self.get_component('png_font')
            font_obj = self.get_component('font_obj')
            
            if color not in png_font.color_cache:
                self.prep_color(color)
                
            letters = png_font.color_cache[color]
            
            x_offset = 0
            y_offset = 0
            
            if line_width != 0:
                spaces = []
                x = 0
                for i, char in enumerate(text):
                    if char == '\n':
                        continue
                    if char == ' ':
                        spaces.append((x, i))
                        x += png_font.space_width + font_obj.base_spacing
                        
                    else:
                        try:
                            x += png_font.letter_spacing[font_obj.font_order.index(char)] + font_obj.base_spacing
                            
                        except (ValueError, KeyError):
                            x += png_font.space_width + font_obj.base_spacing
                            
                line_offset = 0
                
                for i, space in enumerate(spaces):

                    if (space[0] - line_offset) > line_width:
                        line_offset += spaces[i - 1][0] - line_offset
                        
                        if i != 0:
                            text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]
                            
            for char in text:
                if char not in ['\n', ' ']:
                    try:
                        surf.blit(letters[font_obj.font_order.index(char)], (loc[0] + x_offset, loc[1] + y_offset), **blit_kwargs)
                        x_offset += png_font.letter_spacing[font_obj.font_order.index(char)] + font_obj.base_spacing
                        
                    except (ValueError, KeyError):
                        x_offset += png_font.space_width + font_obj.base_spacing
                        
                elif char == ' ':
                    x_offset += png_font.space_width + font_obj.base_spacing
                    
                else:
                    y_offset += font_obj.line_spacing + png_font.line_height
                    x_offset = 0
