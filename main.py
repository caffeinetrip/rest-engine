import pygame
from rest import *
from rest.utils.hooks import gen_hook
from settings import settings
from content_data.entities_data import entities
from entities.player import PlayerEntity
from behavior import *

class MyGame(Game):
    def __init__(self):
        super().__init__()
        init(settings)
        
        self.camera = Camera(settings.display_size, slowness=settings.camera_slowness, pos=(5, 0))
        
        self.tilemap = Tilemap()
        self.tilemap.load('content_data/maps/1.pmap', spawn_hook=gen_hook())
        
        self.player = PlayerEntity((100, 150))
        G.object_collections.register(self.player.get_component('object'), 'entities')
        
        self.entities_data = entities

    def load(self):
        self.event_system = G.event_system

    def update(self):
        self.camera.set_target(self.player.get_component('object'))
        self.camera.update()
        
        visible_rect = pygame.Rect(
            self.camera[0] - 16,
            self.camera[1] - 16,
            G.window.surfaces['default'].get_width() + 48,
            G.window.surfaces['default'].get_height() + 48
        )
        
        G.object_collections.update(view_area=visible_rect)
        
        self.player.get_component('object').physics_update(self.tilemap)
        
        self.tilemap.renderz(visible_rect, offset=self.camera)
        G.object_collections.renderz(layer_group='game', camera_offset=self.camera)
        
        pygame.display.set_caption((str(round(G.window.fps, 1))))
        
        G.window.cycle()
        
        G.input.update(self)

if __name__ == "__main__":
    game = MyGame()
    game.run()