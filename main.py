import pygame

from rest import *
from rest.utils.hooks import gen_hook

from content_data.entities_data import entities
from entities.player import PlayerEntity

from behavior import *

WINDOW_SIZE = (1020, 660)
DISPLAY_SIZE = (340, 220)
FPS_CAP = 60
TILE_SIZE = (16, 16)
CAMERA_SLOWNESS = 5

class MyGame(Game):
    def __init__(self):
        super().__init__()
        init(
            dimensions=(800, 600),
            caption='Soma Try 1',
            fps_cap=60,
            sound_data_path='content_data/sound_data',
            spritesheet_path='content_data/image_data/spritesheets',
            entities_path='content_data/image_data/entities',
            frag_path='content_data/shaders/shader.frag'
        )
        
        self.camera = Camera(DISPLAY_SIZE, slowness=0.3, pos=(5, 0))
        
        self.tilemap = Tilemap()
        self.tilemap.load('content_data/maps/1.pmap', spawn_hook=gen_hook())
        
        self.background_surface = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        self.display_surface = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        self.ui_surface = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        
        G.renderer.add_surfaces(
            {'background': self.background_surface, 
            'default': self.display_surface, 
            'ui': self.ui_surface})
        
        self.player = PlayerEntity((100, 150))
        G.object_collections.register(self.player.get_component('object'), 'entities')
        
        self.entities_data = entities
        

    def load(self):
        self.event_system = G.event_system

    def update(self):

        self.display_surface.fill((0, 0, 0, 0))
        self.ui_surface.fill((0, 0, 0, 0))
        self.background_surface.fill((0, 0, 0, 0))
        
        self.camera.set_target(self.player.get_component('object'))
        self.camera.update()
        
        visible_rect = pygame.Rect(
            self.camera[0] - 16,
            self.camera[1] - 16,
            self.display_surface.get_width() + 48,
            self.display_surface.get_height() + 48
        )
        
        G.object_collections.update(view_area=visible_rect)
        
        self.player.get_component('object').physics_update(self.tilemap)
        
        self.tilemap.renderz(visible_rect, offset=self.camera)
        G.object_collections.renderz(layer_group='game', camera_offset=self.camera)
        
        pygame.display.set_caption((str(round(G.window.fps, 1))))

        window_surfaces = {'surface': self.display_surface, 'bg_surf': self.background_surface,
                           'ui_surf': self.ui_surface}
        G.window.cycle(window_surfaces)
        
        G.input.update(self)

if __name__ == "__main__":
    game = MyGame()
    game.run()